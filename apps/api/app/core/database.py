"""
Database configuration and session management for ClauseLens AI API.
Uses SQLAlchemy 2.0 with async support and pgvector for embeddings.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
import asyncpg
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency to get database session.
    Yields a database session and ensures it's closed after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database with tables and extensions."""
    try:
        # Create all tables
        async with engine.begin() as conn:
            # Enable pgvector extension
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


async def close_db():
    """Close database connections."""
    await engine.dispose()
    logger.info("Database connections closed")


# Database health check
async def check_db_health() -> bool:
    """Check if database is healthy and accessible."""
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return False


# Vector similarity search helper
async def vector_similarity_search(
    session: AsyncSession,
    table_name: str,
    embedding_column: str,
    query_embedding: list[float],
    limit: int = 10,
    similarity_threshold: float = 0.7
) -> list[dict]:
    """
    Perform vector similarity search using pgvector.
    
    Args:
        session: Database session
        table_name: Name of the table to search
        embedding_column: Name of the embedding column
        query_embedding: Query embedding vector
        limit: Maximum number of results
        similarity_threshold: Minimum similarity score
    
    Returns:
        List of similar records with similarity scores
    """
    try:
        # Convert embedding to PostgreSQL array format
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        # Perform similarity search using cosine distance
        query = f"""
        SELECT *, 
               1 - ({embedding_column} <=> '{embedding_str}'::vector) as similarity
        FROM {table_name}
        WHERE 1 - ({embedding_column} <=> '{embedding_str}'::vector) > {similarity_threshold}
        ORDER BY {embedding_column} <=> '{embedding_str}'::vector
        LIMIT {limit}
        """
        
        result = await session.execute(query)
        rows = result.fetchall()
        
        return [
            {
                **dict(row._mapping),
                "similarity": float(row.similarity)
            }
            for row in rows
        ]
    except Exception as e:
        logger.error("Vector similarity search failed", error=str(e))
        return []


# Database migration helper
async def run_migrations():
    """Run database migrations using Alembic."""
    try:
        from alembic import command
        from alembic.config import Config
        
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error("Database migration failed", error=str(e))
        raise

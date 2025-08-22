"""
Main API router for ClauseLens AI.
Combines all endpoint modules into a single router.
"""

from fastapi import APIRouter

from app.api.v1 import auth, projects, contracts, analysis, reports, websocket

# Create main API router
api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])

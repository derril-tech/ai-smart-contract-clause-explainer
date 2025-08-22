"""
Logging configuration for ClauseLens AI API.
Uses structlog for structured logging with correlation IDs.
"""

import logging
import sys
from typing import Any, Dict
import structlog
from structlog.stdlib import LoggerFactory

from app.core.config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance.
    
    Args:
        name: Logger name (optional)
    
    Returns:
        Configured structured logger
    """
    return structlog.get_logger(name)


def log_request(request_id: str, method: str, path: str, status_code: int, duration: float) -> None:
    """Log HTTP request information.
    
    Args:
        request_id: Unique request identifier
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration: Request duration in seconds
    """
    logger = get_logger("http")
    logger.info(
        "HTTP request completed",
        request_id=request_id,
        method=method,
        path=path,
        status_code=status_code,
        duration=duration,
    )


def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
    """Log error information with context.
    
    Args:
        error: Exception that occurred
        context: Additional context information
    """
    logger = get_logger("error")
    logger.error(
        "Application error",
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {},
        exc_info=True,
    )


def log_analysis_start(project_id: str, contract_address: str, chain_id: int) -> None:
    """Log analysis start event.
    
    Args:
        project_id: Project identifier
        contract_address: Contract address being analyzed
        chain_id: Blockchain network ID
    """
    logger = get_logger("analysis")
    logger.info(
        "Analysis started",
        project_id=project_id,
        contract_address=contract_address,
        chain_id=chain_id,
    )


def log_analysis_complete(project_id: str, duration: float, findings_count: int) -> None:
    """Log analysis completion event.
    
    Args:
        project_id: Project identifier
        duration: Analysis duration in seconds
        findings_count: Number of findings discovered
    """
    logger = get_logger("analysis")
    logger.info(
        "Analysis completed",
        project_id=project_id,
        duration=duration,
        findings_count=findings_count,
    )


def log_ai_request(model: str, tokens_used: int, cost: float) -> None:
    """Log AI model usage.
    
    Args:
        model: AI model name
        tokens_used: Number of tokens consumed
        cost: Cost in USD
    """
    logger = get_logger("ai")
    logger.info(
        "AI model usage",
        model=model,
        tokens_used=tokens_used,
        cost=cost,
    )


def log_security_event(event_type: str, severity: str, details: Dict[str, Any]) -> None:
    """Log security-related events.
    
    Args:
        event_type: Type of security event
        severity: Event severity level
        details: Event details
    """
    logger = get_logger("security")
    logger.warning(
        "Security event",
        event_type=event_type,
        severity=severity,
        details=details,
    )


def log_performance_metric(metric_name: str, value: float, unit: str = None) -> None:
    """Log performance metrics.
    
    Args:
        metric_name: Name of the metric
        value: Metric value
        unit: Unit of measurement (optional)
    """
    logger = get_logger("performance")
    logger.info(
        "Performance metric",
        metric_name=metric_name,
        value=value,
        unit=unit,
    )

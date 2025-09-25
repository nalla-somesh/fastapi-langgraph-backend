import structlog
import logging
from app.core.config import settings

def setup_logging():
    """Configure structured logging for the application."""
    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG if settings.debug else logging.INFO,
    )
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.JSONRenderer() if not settings.debug else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(name: str = "app"):
    """Get a configured logger instance."""
    return structlog.get_logger(name)
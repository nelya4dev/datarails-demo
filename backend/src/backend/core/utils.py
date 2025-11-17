from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return current UTC time with timezone information.

    This is a drop-in replacement for datetime.now() that always returns
    timezone-aware datetime in UTC. All database timestamps should use this
    function to ensure consistency and prevent timezone bugs.

    Returns:
        Timezone-aware datetime object representing current UTC time.

    Note:
        - Always returns UTC (timezone.utc)
        - Result has tzinfo attribute set (timezone-aware)
        - Compatible with SQLAlchemy DateTime(timezone=True) columns
        - Recommended for all timestamp generation in the application
    """
    return datetime.now(timezone.utc)

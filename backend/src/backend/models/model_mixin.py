from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.utils import utcnow


class TimestampMixin:
    """Mixin that adds automatic timestamp tracking to models.

    Adds two timezone-aware timestamp columns:
    - created_at: Set once on record creation
    - updated_at: Automatically updated on every record modification

    Both timestamps use UTC timezone and are set using utcnow() utility function.

    Use this mixin for any model that needs audit trail timestamps.

    Attributes:
        created_at: Timestamp when record was created (timezone-aware datetime).
            Automatically set on INSERT. Never updated.
        updated_at: Timestamp when record was last modified (timezone-aware datetime).
            Automatically set on INSERT and updated on every UPDATE.

    Note:
        SQLAlchemy's onupdate parameter automatically triggers updated_at
        refresh on any column modification in the model.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow
    )

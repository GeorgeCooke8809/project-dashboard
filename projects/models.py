from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from projects.db import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    datetime_created: Mapped[datetime] = mapped_column(nullable=False)
    # ? favorite: Mapped[bool] = mapped_column(nullable=False)
    # ? datetime_accessed: Mapped[datetime] = mapped_column(nullable=True)
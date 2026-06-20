from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from projects.db import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    datetime_created: Mapped[datetime] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)
    # TODO: Add AI collaboration grade
    # TODO: Add GitHub link
    # ? favorite: Mapped[bool] = mapped_column(nullable=False)
    # ? datetime_accessed: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<{self.id = }, {self.name = }, {self.url = }, {self.description = }, {self.datetime_created = }, {self.active = }>"
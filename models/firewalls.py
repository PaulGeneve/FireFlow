from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db
from typing import List

class Firewalls(db.Model):
    __tablename__ = 'firewalls'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    location: Mapped[str] = mapped_column(nullable=True)
    ip_address: Mapped[str] = mapped_column(nullable=True)
    filtering_policies: Mapped[List['FilteringPolicy']] = relationship(backref='firewall', cascade='all, delete-orphan'
                                                                       , lazy='selectin')

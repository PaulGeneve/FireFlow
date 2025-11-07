from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db
from typing import List
from models.rules import Rules


class FilteringPolicy(db.Model):
    __tablename__ = 'filtering_policy'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    action: Mapped[str] = mapped_column(default='allow')
    enabled: Mapped[bool] = mapped_column(default=True)
    firewall_id: Mapped[int] = mapped_column(db.ForeignKey('firewalls.id', ondelete='CASCADE'))
    rules: Mapped[List['Rules']] = relationship(backref='filtering_policy', cascade='all, delete-orphan',  lazy='select')

    def to_dict(self)-> dict:
        return {
            "id": self.id,
            "name": self.name,
            "rules": [rule.to_dict() for rule in self.rules]
        }
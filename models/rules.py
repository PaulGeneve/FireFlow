from sqlalchemy.orm import Mapped, mapped_column
from extensions import db
from sqlalchemy import ForeignKey


class Rules(db.Model):
    __tablename__ = 'rules'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    source: Mapped[str] = mapped_column(nullable=True)
    destination: Mapped[str] = mapped_column(nullable=True)
    port: Mapped[str] = mapped_column(nullable=True)
    filtering_policy_id: Mapped[int] = mapped_column(ForeignKey('filtering_policy.id', ondelete='CASCADE'))

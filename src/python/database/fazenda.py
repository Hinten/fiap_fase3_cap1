from sqlalchemy import String, Sequence
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base.model import Model


class Fazenda(Model):
    __tablename__ = "FAZENDA"

    id: Mapped[int] = mapped_column(
            Sequence(f"{__tablename__}_seq_id"),
            primary_key=True,
            autoincrement=True,
            nullable=False
        )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(14), nullable=False)

from sqlalchemy import String, ForeignKey, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base.model import Model


class Teste(Model):
    __tablename__ = "TABELA_DE_TESTE_4"

    id: Mapped[int] = mapped_column(
            Sequence(f"{__tablename__}_seq_id"),
            primary_key=True,
            autoincrement=True,
            nullable=False
        )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)


# class Teste2(Model):
#     __tablename__ = "TESTE2"
#
#     nome: Mapped[str] = mapped_column(String(255), nullable=False)
#     teste_id: Mapped[int] = mapped_column(ForeignKey("TESTE.id"), nullable=False)
#
#     # Relacionamento opcional
#     teste: Mapped["Teste"] = relationship("Teste", back_populates="testes")
#

if __name__ == "__main__":
    from src.database.base.database import Database

    Database.init_oracledb_from_file()

    teste1 = Teste(nome="Teste aehuaheuae")
    saved = teste1.save()
    print(f"Teste salvo com ID: {saved.id}")

    pegar_teste = Teste.get_from_id(2)

    print(pegar_teste)

    print(f"Teste pego com ID: {pegar_teste} ${pegar_teste.id} e nome: {pegar_teste.nome}")

    # pegar_teste.nome = 'Teste atualizado'
    #
    # pegar_teste.save()
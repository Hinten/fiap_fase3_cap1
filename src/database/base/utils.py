from sqlalchemy.sql.ddl import CreateTable

from src.database.base.database import Database
from src.database.base.model import Model


def gerar_ddl(output_file: str):
    """
    ATENÇÃO: PARA FUNCIONAR TEM QUE IMPORTAR AS CLASSES QUE HERDAM DE MODEL NO MESMO ARQUIVO
    Gera um arquivo DDL com as definições de tabelas do SQLAlchemy.
    :param output_file: Caminho do arquivo onde o DDL será salvo.
    """
    with open(output_file, "w") as file:
        for table in Model.metadata.sorted_tables:
            ddl = str(CreateTable(table).compile(Database.engine))
            file.write(f"{ddl};\n\n")

def gerar_mer(output_file: str):
    """
    ATENÇÃO: PARA FUNCIONAR TEM QUE IMPORTAR AS CLASSES QUE HERDAM DE MODEL NO MESMO ARQUIVO
    Gera um MER por escrito com base nas tabelas do SQLAlchemy.
    :param output_file: Caminho do arquivo onde o MER será salvo.
    """
    with open(output_file, "w") as file:
        for table in Model.metadata.sorted_tables:
            file.write(f"Entidade: {table.name}\n")
            file.write("Atributos:\n")
            for column in table.columns:
                file.write(f"  - {column.name} ({column.type})\n")
            if table.primary_key:
                pk = ", ".join([col.name for col in table.primary_key.columns])
                file.write(f"Chave Primária: {pk}\n")
            if table.foreign_keys:
                file.write("Relacionamentos:\n")
                for fk in table.foreign_keys:
                    parent_table = fk.column.table
                    relationship_type = "um para muitos"

                    #todo implementar implementar 1to1 e m2m

                    file.write(f"  - {parent_table.name} ({fk.column.name} - {fk.column.type}) [{relationship_type}]\n")
            file.write("\n")


# if __name__ == "__main__":
#     from src.database.base.database import Database
#     from src.database.base.model import Model
#     #para isso aqui funcionar tem que importar as classes que herdam de Model
#     from src.database.teste import *
#
#
#     Database.init_oracledb_from_file()
#     gerar_ddl('teste.ddl')
#     gerar_mer('mer.txt')
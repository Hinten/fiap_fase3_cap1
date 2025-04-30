from sqlalchemy.schema import CreateTable
from src.python.database.base.model import Model
from src.python.database.base.oracle import DB
import os

from src.python.database.dynamic_import import import_models


def generate_ddl(output_dir="generated"):
    """
    Gera os comandos SQL (DDL) para criar as tabelas baseadas nos models.
    Salva o resultado em um arquivo DDL.
    """
    import_models()
    os.makedirs(output_dir, exist_ok=True)
    ddl_path = os.path.join(output_dir, "schema.ddl")

    with open(ddl_path, "w", encoding="utf-8") as file:
        for table in Model.metadata.sorted_tables:
            ddl_statement = str(CreateTable(table).compile(DB.engine))
            file.write(f"{ddl_statement};\n\n")

    print(f"Arquivo DDL gerado em: {ddl_path}")


def generate_mer() -> str:
    """
    Retorna um MER simplificado baseado nos models e relacionamentos declarados.
    """
    import_models()
    mer_output = "\nModelo de Entidade-Relacionamento:\n\n"

    for table in Model.metadata.tables.values():
        mer_output += f"Tabela: {table.name}\n"
        for column in table.columns:
            col_info = f"  - {column.name} ({column.type})"
            if column.primary_key:
                col_info += " [PK]"
            if column.foreign_keys:
                foreign_table = list(column.foreign_keys)[0].column.table.name
                col_info += f" [FK -> {foreign_table}]"
            mer_output += col_info + "\n"
        mer_output += "\n"

    return mer_output

if __name__ == "__main__":
    DB.init_from_env()
    generate_ddl()
    print(generate_mer())

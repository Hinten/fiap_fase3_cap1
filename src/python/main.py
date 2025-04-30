import logging
from src.python.database.base.oracle import DB
from database.setup import create_all_tables, drop_all_tables
from database.utils import generate_mer
from logs.logger import config_logger


def main():
    config_logger()
    logger = logging.getLogger(__name__)
    logger.info("Iniciando o sistema...")
    DB.init_from_env()

    try:
        logger.info("Criando tabelas no banco, se necessário...")
        create_all_tables()

        generate_mer()

        logger.info("Conexão com o banco de dados bem-sucedida.")
        logger.info("Tabelas criadas/verificadas com sucesso.")

    except Exception as e:
        logger.exception("Erro ao iniciar o sistema ou conectar ao banco de dados.")
        raise e

    logger.info("Sistema finalizado.")

if __name__ == "__main__":
    main()

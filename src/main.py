from logs.logger import configLogger
from src.database.base.database import Database
from src.database.base.model import Model


def main():

    configLogger()
    Database.init_oracledb()
    Model._create_all_tables()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import logging

class ColorFormatter(logging.Formatter):
    # Mapear níveis de log para cores ANSI
    LEVEL_COLORS = {
        logging.DEBUG: "\033[34m",    # Azul
        logging.INFO: "\033[32m",     # Verde
        logging.WARNING: "\033[33m",  # Amarelo
        logging.ERROR: "\033[31m",    # Vermelho
        logging.CRITICAL: "\033[35m"  # Magenta
    }
    RESET_COLOR = "\033[0m"  # Resetar cor

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, self.RESET_COLOR)
        formatted_message = super().format(record)
        return f"{color}{formatted_message}{self.RESET_COLOR}"

def configLogger(file_name: str = 'app.log', level: int = logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(level)

    format_string = '[%(levelname)s] %(asctime)s %(filename)s: %(message)s'

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = ColorFormatter(format_string)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(file_handler)

if __name__ == '__main__':
    configLogger()
    logging.info('This is an info message')
    logging.debug('This is a debug message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')
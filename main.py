from Python_Bot import main

from telegram.error import __all__  as tel_error

from sqlite3 import Error as sql_error
import logging


if __name__ == "__main__":

    try:

        main()

    except tele_error as e:

        logging.error(f"An error ocurred:{e}")

    except sql_error as e:

        logging.error(f"An error occured:{e}")

    except Exception as e:

        logging.error(f"An error ocurred:{e}")
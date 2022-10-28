import os
import mysql.connector
from dotenv import load_dotenv

class Database:
    """Management of actions with the database"""

    def __init__(self):
        """Initialisation of the database

        Raises:
            Exception: Sent to main script
        """
        try:
            load_dotenv()
            host = f"{os.getenv('DB_HOST')}"
            db = f"{os.getenv('DB_DATABASE')}"
            user = f"{os.getenv('DB_USER')}"
            password = f"{os.getenv('DB_PASSWORD')}"
            port = int(f"{os.getenv('DB_PORT')}")

            config = {
                'host': host,
                'database': db,
                'user': user,
                'password': password,
                'port': port,
                'connection_timeout': 30
            }

            self.connection = mysql.connector.connect( **config )

        except Exception as error:
            raise Exception(f"EXCEPTION MYSQL - {error}") from error

    def closeConnection(self):
        """Close the Mysql Connection"""
        self.connection.close()

    def getCursor(self, prepared=False):
        """Get the mysql cursor

        Args:
            prepared (bool, optional): Set to prepared request Defaults to False.

        Returns:
            cursor: mysql cursor
        """
        return self.connection.cursor(prepared=prepared)

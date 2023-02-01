#!/usr/bin/env python3
"""Personal data"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    '''returns the log message obfuscated'''
    for pii in fields:
        message = re.sub(fr'{pii}=.+?{separator}',
                         f'{pii}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''constructor'''
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''to filter values in incoming log records'''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    '''returns a logging.Logger object'''
    logObj = logging.getLogger("user_data")
    logObj.setLevel(logging.INFO)
    logObj.propagate = False
    Handle = logging.StreamHandler()
    Handle.setFormater(RedactingFormatter(list(PII_FIELDS)))
    logObj.addHandler(Handle)
    return logObj


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''returns a connector to the database'''
    username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    dbname = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(user=username, password=password,
                                   host=host, database=dbname)


def main():
    '''retrieve & display all rows in the users table'''
    conn = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * from users")
    fields = [user[0] for user in cursor.description]
    print(fields)
    log = get_logger()
    for c in cursor:
        row = ''.join(f'{f}={str(r)}; ' for r, f in zip(c, fields))
        log.info(c)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

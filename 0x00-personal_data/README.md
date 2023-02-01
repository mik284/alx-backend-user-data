# 0x00. Personal data

## Resources
Read or watch:

* [What Is PII, non-PII, and Personal Data?](https://piwik.pro/blog/what-is-pii-personal-data/)
* [logging documentation](https://docs.python.org/3/library/logging.html)
* [bcrypt package](https://github.com/pyca/bcrypt/)
* [Logging to Files, Setting Levels, and Formatting](https://www.youtube.com/watch?v=-ARI4Cz-awo)

# Tasks

## [0. Regex-ing](./filtered_logger.py)
Write a function called `filter_datum` that returns the log message obfuscated:

* Arguments:

    `fields`: a list of strings representing all fields to obfuscate

    `redaction`: a string representing by what the field will be obfuscated

    `message`: a string representing the log line

    `separator`: a string representing by which character is separating all fields in the log line (`message`)

* The function should use a regex to replace occurrences of certain field values.

* `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.
```
bob@dylan:~$ ./main-0.py
name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
```

## [1. Log formatter](./filtered_logger.py)
Copy the ... code into `filtered_logger.py`

Update the class to accept a list of strings `fields` constructor argument.

Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for fields in `fields` should be filtered.

DO NOT extrapolate `FORMAT` manually. The `format` method should be less than 5 lines long.
```
bob@dylan:~$ ./main-1.py
[HOLBERTON] my_logger INFO 2019-11-19 18:24:25,105: name=Bob; email=***; ssn=***; password=***;
```

## [2. Create logger](./filtered_logger.py)
Use [user_data.csv](./user_data.csv) for this task

Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object.

The logger should be named `"user_data"` and only log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as formatter.

Create a tuple `PII_FIELDS` constant at the root of the module containing the fields from `user_data.csv` that are considered PII. `PII_FIELDS` can contain only 5 fields - choose the right list of fields that can are considered  PIIs or information that you must hide in your logs. Use it to parameterize the formatter.

Tips:

[What Is PII, non-PII, and personal data?](https://piwik.pro/blog/what-is-pii-personal-data/)

[Uncovering Password Habits](https://digitalguardian.com/blog/uncovering-password-habits-are-users-password-security-habits-improving-infographic)
```
bob@dylan:~$ ./main-2.py
<class 'logging.Logger'>
PII_FIELDS: 5
```

## [3. Connect to secure database](./filtered_logger.py)
Database credentials should NEVER be stored in code or checked into version control. One secure option is to store them as environment variable on the application server.

In this task, you will connect to a secure `holberton` database to read a `users` table. The database is protected by a username and password that are set as environment variables on the server named `PERSONAL_DATA_DB_USERNAME` (set the default ), `PERSONAL_DATA_DB_PASSWORD` (set the default as an empty string) and `PERSONAL_DATA_DB_HOST` (set the default ).

The database name is stored in `PERSONAL_DATA_DB_NAME`.

Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection` object).

* Use the `os` module to obtain credentials from the environment
* Use the module `mysql-connector-python` to connect to the MySQL database (`pip3 install mysql-connector-python`)
```
bob@dylan:~$ cat main-0.sql | mysql -uroot -p
Enter password: 
bob@dylan:~$ 
bob@dylan:~$ echo "SELECT COUNT(*) FROM users;" | mysql -uroot -p my_db
Enter password: 
2
bob@dylan:~$ PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./main-3.py
2
```

## [4. Read and filter data](./filtered_logger.py)
Implement a `main` function that takes no arguments and returns nothing.

The function will obtain a database connection using `get_db` and retrieve all rows in the `users` table and display each row under a filtered format like this:

        [HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***; ssn=***; password=***; ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b; last_login=2019-11-14T06:16:24; user_agent=Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN);

Filtered fields:
```
 * name
 * email
 * phone
 * ssn
 * password
```

Only your `main` function should run when the module is executed.
```
bob@dylan:~$ cat main.sql | mysql -uroot -p
bob@dylan:~$ echo "SELECT COUNT(*) FROM users;" | mysql -uroot -p my_db
Enter password: 
2
bob@dylan:~$ PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./filtered_logger.py
[HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***; ssn=***; password=***; ip=60ed:c396:2ff:244:bbd0:9208:26f2:93ea; last_login=2019-11-14 06:14:24; user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36;
[HOLBERTON] user_data INFO 2019-11-19 18:37:59,621: name=***; email=***; phone=***; ssn=***; password=***; ip=f724:c5d1:a14d:c4c5:bae2:9457:3769:1969; last_login=2019-11-14 06:16:19; user_agent=Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I9100 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30;
```

## [5. Encrypting passwords](./encrypt_password.py)
User passwords should NEVER be stored in plain text in a database.

Implement a `hash_password` function that expects one string argument name `password` and returns a salted, hashed password, which is a byte string.

Use the `bcrypt` package to perform the hashing (with `hashpw`).
```
bob@dylan:~$ ./main-4.py
b'$2b$12$Fnjf6ew.oPZtVksngJjh1.vYCnxRjPm2yt18kw6AuprMRpmhJVxJO'
b'$2b$12$xSAw.bxfSTAlIBglPMXeL.SJnzme3Gm0E7eOEKOVV2OhqOakyUN5m'
```

## [6. Check valid password](./encrypt_password.py)
Implement an `is_valid` function that expects 2 arguments and returns a boolean.

Arguments:

* `hashed_password: bytes` type
* `password`: string type

Use `bcrypt` to validate that the provided password matches the hashed password.
```
bob@dylan:~$ ./main.py
b'$2b$12$Fnjf6ew.oPZtVksngJjh1.vYCnxRjPm2yt18kw6AuprMRpmhJVxJO'
True
```
localhostas rootas importantas 
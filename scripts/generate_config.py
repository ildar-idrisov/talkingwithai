import configparser
import os

config = configparser.ConfigParser()


def _generate_config():
    db_name = os.getenv('DATABASE_NAME')
    config.add_section('postgres')
    config.set('postgres', 'username', db_name)
    config.set('postgres', 'password', db_name)
    config.set('postgres', 'host', 'postgres')
    config.set('postgres', 'port', '5432')
    config.set('postgres', 'dbname', db_name)

    with open('/talkingwithai/etc/config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    _generate_config()

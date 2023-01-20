from configparser import ConfigParser

import psycopg2


def get_db_parameters_from_config(section_name: str) -> dict:
    """
    Generate dictionary with DB credentials from config
    """
    database = {}

    for parameter, value in config.items(section_name):
        database[parameter] = value

    return database


def get_tables_table_names_from_outer_db(config_section_name: str) -> list:
    """
    Get list of tables names from outer Postgres Server
    """
    parameters = get_db_parameters_from_config(config_section_name)
    connection = psycopg2.connect(**parameters)
    cursor = connection.cursor()
    cursor.execute(
        """SELECT table_name FROM information_schema.tables
         WHERE table_schema = 'public';"""
    )
    execution_from_db = cursor.fetchall()
    connection.close()

    table_names = [table_name for table_name, *_ in execution_from_db]
    return table_names


def main() -> None:
    parameters = get_db_parameters_from_config("MAIN DB")
    connection = psycopg2.connect(**parameters)
    cursor = connection.cursor()
    cursor.close()
    print(get_tables_table_names_from_outer_db(config_section_name="MAIN DB"))


if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')
    main()

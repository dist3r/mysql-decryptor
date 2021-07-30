import argparse
import configparser

from mysqldecryptor.crypto import decrypt
from mysqldecryptor.database import connect_to_database, read_from_table, close_connection, write_to_table
from mysqldecryptor.util import ExtendedDefault


def get_arguments():
    config = configparser.ConfigParser()
    config.read('.mysqldecryptor.conf')

    parser = argparse.ArgumentParser(
        prog='mysqldecryptor',
        description=''
    )

    parser.add_argument(
        '--src-username',
        action=ExtendedDefault,
        env_var='SRC_USERNAME',
        conf_parser=config,
        conf_section='source',
        conf_option='username',
        is_list=False,
        metavar='USERNAME',
        help=''
    )

    parser.add_argument(
        '--src-password',
        action=ExtendedDefault,
        env_var='SRC_PASSWORD',
        conf_parser=config,
        conf_section='source',
        conf_option='password',
        is_list=False,
        metavar='PASSWORD',
        help=''
    )

    parser.add_argument(
        '--src-hostname',
        action=ExtendedDefault,
        env_var='SRC_HOSTNAME',
        conf_parser=config,
        conf_section='source',
        conf_option='hostname',
        is_list=False,
        metavar='HOSTNAME',
        help=''
    )

    parser.add_argument(
        '--src-port',
        action=ExtendedDefault,
        env_var='SRC_PORT',
        conf_parser=config,
        conf_section='source',
        conf_option='port',
        is_list=False,
        metavar='PORT',
        help=''
    )

    parser.add_argument(
        '--src-database',
        action=ExtendedDefault,
        env_var='SRC_DATABASE',
        conf_parser=config,
        conf_section='source',
        conf_option='database',
        is_list=False,
        metavar='DATABASE',
        help=''
    )

    parser.add_argument(
        '--dst-username',
        action=ExtendedDefault,
        env_var='DST_USERNAME',
        conf_parser=config,
        conf_section='destination',
        conf_option='username',
        is_list=False,
        metavar='USERNAME',
        help=''
    )

    parser.add_argument(
        '--dst-password',
        action=ExtendedDefault,
        env_var='DST_PASSWORD',
        conf_parser=config,
        conf_section='destination',
        conf_option='password',
        is_list=False,
        metavar='PASSWORD',
        help=''
    )

    parser.add_argument(
        '--dst-hostname',
        action=ExtendedDefault,
        env_var='DST_HOSTNAME',
        conf_parser=config,
        conf_section='destination',
        conf_option='hostname',
        is_list=False,
        metavar='HOSTNAME',
        help=''
    )

    parser.add_argument(
        '--dst-port',
        action=ExtendedDefault,
        env_var='DST_PORT',
        conf_parser=config,
        conf_section='destination',
        conf_option='port',
        is_list=False,
        metavar='PORT',
        help=''
    )

    parser.add_argument(
        '--dst-database',
        action=ExtendedDefault,
        env_var='DST_DATABASE',
        conf_parser=config,
        conf_section='destination',
        conf_option='database',
        is_list=False,
        metavar='DATABASE',
        help=''
    )

    parser.add_argument(
        '--encryption-passphrase',
        action=ExtendedDefault,
        env_var='ENCRYPTION_PASSPHRASE',
        conf_parser=config,
        conf_section='encryption',
        conf_option='passphrase',
        is_list=False,
        metavar='PASSPHRASE',
        help=''
    )

    parser.add_argument(
        '--encryption-iv',
        action=ExtendedDefault,
        env_var='ENCRYPTION_IV',
        conf_parser=config,
        conf_section='encryption',
        conf_option='initialization_vector',
        is_list=False,
        metavar='INITIALIZATION VECTOR',
        help=''
    )

    parser.add_argument(
        '--table',
        action=ExtendedDefault,
        env_var='TABLE',
        conf_parser=config,
        conf_section='database',
        conf_option='table',
        is_list=False,
        metavar='TABLE_NAME',
        help=''
    )

    parser.add_argument(
        '--plaintext-columns',
        nargs='+',
        action=ExtendedDefault,
        env_var='PLAINTEXT_COLUMNS',
        conf_parser=config,
        conf_section='database',
        conf_option='plaintext_columns',
        is_list=True,
        metavar='PLAINTEXT_COLUMNS_NAMES',
        help=''
    )

    parser.add_argument(
        '--encrypted-columns',
        nargs='+',
        action=ExtendedDefault,
        env_var='ENCRYPTED_COLUMNS',
        conf_parser=config,
        conf_section='database',
        conf_option='encrypted_columns',
        is_list=True,
        metavar='ENCRYPTED_COLUMNS_NAMES',
        help=''
    )

    return parser.parse_args()


def decrypt_columns(data, encrypted_columns_names, passphrase, initialization_vector):
    for row in data:
        for name in encrypted_columns_names:
            row[name] = decrypt(row[name], passphrase, initialization_vector)


def main():
    args = get_arguments()

    columns_names = args.plaintext_columns + args.encrypted_columns

    src_database_connection = connect_to_database(args.src_username, args.src_password, args.src_hostname,
                                                  args.src_port, args.src_database)
    rows = read_from_table(src_database_connection, args.table, columns_names)
    close_connection(src_database_connection)

    decrypt_columns(rows, args.encrypted_columns, args.encryption_passphrase, args.encryption_iv)

    dst_database_connection = connect_to_database(args.dst_username, args.dst_password, args.dst_hostname,
                                                  args.dst_port, args.dst_database)
    write_to_table(dst_database_connection, rows, args.table, columns_names)
    close_connection(dst_database_connection)

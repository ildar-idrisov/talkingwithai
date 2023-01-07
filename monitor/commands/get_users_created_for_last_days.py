import logging
import argparse

from db.models import User
from db.session import DB

logging.disable()


if __name__ == '__main__':
    DB.init_database_interface()
    parser = argparse.ArgumentParser(prog=__file__, description='Returns the count of users created for last X days')
    parser.add_argument('-d', '--days', type=int, help='Days count')
    args = parser.parse_args()
    print(
        f'Users count created for last {args.days} days:',
        User.get_users_created_for_last_days(args.days)
    )

import logging
import argparse

from db.models import Message
from db.session import DB

logging.disable()


if __name__ == '__main__':
    DB.init_database_interface()
    parser = argparse.ArgumentParser(prog=__file__, description='Returns the count of active users for last X days')
    parser.add_argument('-d', '--days', type=int, help='Days count')
    args = parser.parse_args()
    print(
        f'Active users count for last {args.days} days:',
        Message.get_active_users_for_last_days(args.days)
    )

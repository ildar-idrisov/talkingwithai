import logging
import argparse

from db.models import Message
from db.session import DB

logging.disable()


if __name__ == '__main__':
    DB.init_database_interface()
    parser = argparse.ArgumentParser(prog=__file__, description='Returns the count of user messages for last X minutes')
    parser.add_argument('-m', '--minutes', type=int, help='Minutes count')
    args = parser.parse_args()
    print(
        f'Users messages count for last {args.minutes} minutes:',
        Message.messages_count_for_last_x_minutes(args.minutes)
    )

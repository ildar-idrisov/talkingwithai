from flask import Flask, render_template, request

from db.models import Message, User
from db.session import DB

app = Flask(__name__)
DB.init_database_interface()


@app.route("/", methods=['GET'])
def main():
    DB.validate_database()

    form_data = request.args
    try:
        last_x_messages_count_minutes = int(form_data.get('last_x_messages_count', 10))  # 10 minutes by default
        active_users_count_days = int(form_data.get('active_users_count', 30))  # 30 days
        new_users_count_days = int(form_data.get('new_users_count', 30))  # 30 days
    except TypeError:
        raise ValueError('Unexpected form params')

    res_last_x_messages_count = Message.messages_count_for_last_x_minutes(last_x_messages_count_minutes)
    res_active_users_count = Message.get_active_users_for_last_days(active_users_count_days)
    res_new_users_count = User.get_users_created_for_last_days(new_users_count_days)

    return render_template(
        'index.html',
        results={
            'last_x_messages_count': res_last_x_messages_count,
            'active_users_count': res_active_users_count,
            'new_users_count': res_new_users_count,
        },
        form_values={
            'last_x_messages_count': last_x_messages_count_minutes,
            'active_users_count': active_users_count_days,
            'new_users_count': new_users_count_days,
        }
    )

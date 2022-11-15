from flask import Flask, render_template

from db.models import User
from db.session import DB

app = Flask(__name__)
DB.init_database_interface()


@app.route("/")
def main():
    DB.validate_database()
    session = DB.session()
    users = session.query(User).all()
    return render_template('index.html', users=users)

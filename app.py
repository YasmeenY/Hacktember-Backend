from config import app, db, api, bcrypt
from models import db, User

@app.route("/")
def Home():
    return "Home Route"


if __name__ == '__main__':
    app.run(port=5555, debug=True)
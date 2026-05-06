from flask import Flask
from models import db
from routes import init_routes

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

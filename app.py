from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random

app = Flask(__name__) #app name 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database file
db = SQLAlchemy(app)
faker = Faker()

#models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.cli.command("generate_fake_data")
def generate_fake_data():
    with app.app_context():
        for _ in range(10):
            name = faker.name()
            email = faker.email()
            address = faker.address()
            user = User(name=name, email=email, address=address)
            db.session.add(user)
        db.session.commit()

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'address': user.address
        }
        result.append(user_data)
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5504)

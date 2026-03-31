from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

app = Flask(__name__)



@app.route('/')
def home():
    return "API funcionando viva cristo rey"


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()





class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    telefono = Column(String)
Base.metadata.create_all(engine)



@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data.get("name"),
        status=data.get("status"),
        telefono=data.get("telefono")
    )
    session.add(new_user)
    session.commit()
    return jsonify({"mensaje": "Usuario creado con exito jupi"}), 201




@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "status": u.status,
            "telefono": u.telefono
        })
    return jsonify(result)



@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "No encontrado el usuario may"}), 404
    session.delete(user)
    session.commit()
    return jsonify({"mensaje": "Usuario erradicado "}), 200
if __name__ == "__main__":
    app.run()
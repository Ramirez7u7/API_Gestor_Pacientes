from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "API funcionando viva cristo rey"



DATABASE_URL = os.getenv("DATABASE_URL")


print("===================================")
print("DATABASE_URL ORIGINAL:", DATABASE_URL)
print("===================================")


if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


print("===================================")
print("DATABASE_URL FINAL:", DATABASE_URL)
print("===================================")



engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
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
    session = Session()
    data = request.get_json()

    print("DATA RECIBIDA:", data)

    new_user = User(
        name=data.get("name"),
        status=data.get("status"),
        telefono=data.get("telefono")
    )

    session.add(new_user)
    session.commit()
    print("USUARIO CREADO ID:", new_user.id)

    session.close()

    return jsonify({"mensaje": "Usuario creado"}), 201


@app.route('/users', methods=['GET'])
def get_users():
    session = Session()

    users = session.query(User).all()

    print("USUARIOS EN BD:", users)

    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "status": u.status,
            "telefono": u.telefono
        })

    session.close()
    return jsonify(result)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()

    user = session.get(User, user_id)

    if not user:
        session.close()
        return jsonify({"error": "No encontrado"}), 404

    session.delete(user)
    session.commit()
    session.close()

    return jsonify({"mensaje": "Eliminado"}), 200


if __name__ == "__main__":
    app.run()
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password1@localhost:3306/Apka_PZ'
db = SQLAlchemy(app)

swagger = Swagger(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    pesel = db.Column(db.String(11), unique=True, nullable=False)
    matura_points = db.Column(db.Integer, nullable=False)

    @validates('pesel')
    def validate_pesel(self, key, pesel):
        if not pesel:
            raise ValueError("PESEL cannot be empty.")
        if len(pesel) != 11:
            raise ValueError("PESEL must be exactly 11 characters.")
        if not pesel.isdigit():
            raise ValueError("PESEL must contain only digits.")
        return pesel

    def __repr__(self):
        return f'<User {self.name} {self.surname}>'



#kod cezara przesuniecie 43 

def encrypt_caesar(plaintext, shift):
    encrypted_text = ""

    for char in plaintext:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            is_upper = char.isupper()

            # Shift the character
            shifted_char = chr((ord(char) + shift - ord('A' if is_upper else 'a')) % 26 + ord('A' if is_upper else 'a'))

            encrypted_text += shifted_char
        else:
            # If the character is not a letter, leave it unchanged
            encrypted_text += char

    return encrypted_text


def decrypt_caesar(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char.isdigit():
            # Dekodowanie cyfry z przesunięciem 43 w cyklach 0-9
            shifted_char = str((int(char) - shift) % 10)
            decrypted_text += shifted_char
        else:
            decrypted_text += char
    return decrypted_text



@app.route('/api/post_User', methods=['POST'])
def post_User():
    """
    Dodaje użytkownika
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: The user to create.
        required: true
        schema:
          type: object
          required:
            - pesel
          properties:
            name:
              type: string
            surname:
              type: string
            pesel:
              type: string
            matura_points:
              type: integer
    responses:
      200:
        description: Wartości zostały pomyślnie otrzymane
    """
    try:
        data = request.get_json()
        decrypted_pesel = decrypt_caesar(data['pesel'], 43)
        new_user = User(
            name=data['name'],
            surname=data['surname'],
            pesel=decrypted_pesel,
            matura_points=data['matura_points']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='Values received and stored successfully!'), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400

@app.route('/api/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Aktualizuje dane użytkownika na podstawie podanego ID.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: Unikalne ID użytkownika do aktualizacji.
      - in: body
        name: body
        required: true
        description: Pola użytkownika do aktualizacji.
        schema:
          type: object
          properties:
            name:
              type: string
            surname:
              type: string
            pesel:
              type: string
            matura_points:
              type: integer
    responses:
      200:
        description: Dane użytkownika zaktualizowane pomyślnie.
      404:
        description: Użytkownik nie został znaleziony.
    """
    user_to_update = User.query.get(user_id)
    if not user_to_update:
        return jsonify(error='User not found'), 404
    
    data = request.get_json()
    try:
        if 'name' in data:
            user_to_update.name = data['name']
        if 'surname' in data:
            user_to_update.surname = data['surname']
        if 'pesel' in data:
            user_to_update.pesel = data['pesel']
        if 'matura_points' in data:
            user_to_update.matura_points = data['matura_points']
        
        db.session.commit()
        return jsonify(message='User updated successfully'), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400

@app.route('/api/update_user_by_pesel/<pesel>', methods=['PUT'])
def update_user_by_pesel(pesel):
    """
    Aktualizuje dane użytkownika na podstawie podanego numeru PESEL.
    ---
    parameters:
      - name: pesel
        in: path
        type: string
        required: true
        description: PESEL użytkownika do aktualizacji.
      - in: body
        name: body
        required: true
        description: Pola użytkownika do aktualizacji.
        schema:
          type: object
          properties:
            name:
              type: string
            surname:
              type: string
            matura_points:
              type: integer
    responses:
      200:
        description: Dane użytkownika zaktualizowane pomyślnie.
      404:
        description: Użytkownik nie został znaleziony.
    """
    decrypted_pesel = decrypt_caesar(pesel, 43)
    user_to_update = User.query.filter_by(pesel=decrypted_pesel).first()
    if not user_to_update:
        return jsonify(error='User not found'), 404

    data = request.get_json()
    try:
        if 'name' in data:
            user_to_update.name = data['name']
        if 'surname' in data:
            user_to_update.surname = data['surname']
        if 'matura_points' in data:
            user_to_update.matura_points = data['matura_points']

        db.session.commit()
        return jsonify(message='User updated successfully'), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400

@app.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Usuwa użytkownika na podstawie podanego ID.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: Unikalne ID użytkownika do usunięcia.
    responses:
      200:
        description: Użytkownik usunięty pomyślnie.
      404:
        description: Użytkownik nie został znaleziony.
    """
    try:
        user_to_delete = User.query.get(user_id)
        if user_to_delete is None:
            return jsonify(error='User not found'), 404

        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify(message='User deleted successfully'), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400

@app.route('/api/delete_user_by_pesel/<pesel>', methods=['DELETE'])
def delete_user_by_pesel(pesel):
    """
    Usuwa użytkownika na podstawie podanego numeru PESEL.
    ---
    parameters:
      - name: pesel
        in: path
        type: string
        required: true
        description: PESEL użytkownika do usunięcia.
    responses:
      200:
        description: Użytkownik usunięty pomyślnie.
      404:
        description: Użytkownik nie został znaleziony.
    """
    try:
        decrypted_pesel = decrypt_caesar(pesel, 43)
        user_to_delete = User.query.filter_by(pesel=decrypted_pesel).first()
        if user_to_delete is None:
            return jsonify(error='User not found'), 404

        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify(message='User deleted successfully'), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400
    
@app.route('/api/user/<int:user_id>', methods=['GET'])
def show_user(user_id):
    """
    Wyświetla dane użytkownika na podstawie podanego ID.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: Unikalne ID użytkownika.
    responses:
      200:
        description: Dane użytkownika.
      404:
        description: Użytkownik nie został znaleziony.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify(error='User not found'), 404

    user_data = {
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'pesel': user.pesel,
        'matura_points': user.matura_points
    }
    return jsonify(user_data), 200


@app.route('/api/users', methods=['GET'])
def show_all_users():
    """
    Wyświetla dane wszystkich użytkowników.
    ---
    responses:
      200:
        description: Lista wszystkich użytkowników.
    """
    users = User.query.all()
    users_data = [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'pesel': user.pesel,
        'matura_points': user.matura_points
    } for user in users]
    return jsonify(users_data), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='192.168.1.109', port=5000)

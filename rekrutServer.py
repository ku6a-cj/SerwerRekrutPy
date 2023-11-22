from flask import Flask, request, jsonify
#kod cezara przesuniecie 43 

app = Flask(__name__)

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
    # To decrypt, use a negative shift
    return encrypt_caesar(ciphertext, -shift)

@app.route('/api/receive_values', methods=['POST'])
def receive_values():
    try:
        data = request.get_json()
        value1 = data['value1']
        value2 = data['value2']
        value3 = data['value3']
        value4 = data['value4']
        print(f"Received values POST: Name:{value1}, Surname:{value2}, Pesel:{value3}, Matura Points:{value4}")
        return jsonify(message='Values received successfully!')
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify(error='Invalid data format'), 400


@app.route('/api/receive_values', methods=['PUT'])
def receive_values1():
    try:
        data = request.get_json()
        value1 = data['value1']
        value2 = data['value2']
        value3 = data['value3']
        value4 = data['value4']

        print(f"Received values PUT:  Name:{value1}, Surname:{value2}, Pesel:{value3}, Matura Points:{value4}")
        return jsonify(message='Values received successfully!')
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify(error='Invalid data format'), 400


@app.route('/api/receive_values', methods=['DELETE'])
def receive_values2():
    try:
        data = request.get_json()
        value1 = data['value1']
        value2 = data['value2']
        value3 = data['value3']
        value4 = data['value4']

        print(f"Received values DELETE:  Name:{value1}, Surname:{value2}, Pesel:{value3}, Matura Points:{value4}")
        return jsonify(message='Values received successfully!')
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify(error='Invalid data format'), 400


if __name__ == '__main__':
    app.run(debug=True)
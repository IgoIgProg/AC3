from flask import Flask, jsonify, request
import pyodbc


app = Flask(__name__)

# Configuração da conexão com o banco de dados
server = 'localhost'
database = 'AC'
username = 'Drogo'
password = 'password'
cnxn = pyodbc.connect(f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Rota GET para buscar todos os clientes
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM clientes')
    rows = cursor.fetchall()
    clientes = []
    for row in rows:
        cliente = {
            'id': row[0],
            'nome': row[1],
            'email': row[2]
        }
        clientes.append(cliente)
    return jsonify(clientes), 200

# Rota POST para cadastrar um novo cliente
@app.route('/api/clientes', methods=['POST'])
def add_cliente():
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", nome, email)
    cnxn.commit()
    return jsonify({'mensagem': 'Cliente adicionado com sucesso'}), 201

# Rota DELETE para excluir um cliente pelo id
@app.route('/api/clientes/<int:id>', methods=['DELETE'])
def remove_cliente(id):
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", id)
    cnxn.commit()
    if cursor.rowcount > 0:
        return jsonify({'mensagem': 'Cliente removido com sucesso'}), 200
    else:
        return jsonify({'error': 'Cliente não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)

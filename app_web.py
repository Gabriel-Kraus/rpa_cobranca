from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cobranca.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    valor = request.form['valor']
    vencimento = request.form['vencimento']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insere o Cliente
    cursor.execute('INSERT INTO clientes (nome, email, telefone, endereco) VALUES (?, ?, ?, ?)',
                   (nome, email, telefone, endereco))
    cliente_id = cursor.lastrowid

    # Insere a Fatura vinculada
    cursor.execute('INSERT INTO faturas (cliente_id, valor, vencimento) VALUES (?, ?, ?)',
                   (cliente_id, valor, vencimento))

    conn.commit()
    conn.close()

    return render_template('index.html', msg="Cliente e fatura cadastrados com sucesso!")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
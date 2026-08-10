from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = 'projeto_escola'

def conectar():
    banco = sqlite3.connect('database.db')
    banco.row_factory = sqlite3.Row
    return banco

banco_inicial = conectar()
banco_inicial.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, email TEXT UNIQUE NOT NULL, senha TEXT NOT NULL)')
banco_inicial.execute('CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, descricao TEXT, status TEXT DEFAULT "pendente", usuario_id INTEGER, FOREIGN KEY(usuario_id) REFERENCES usuarios(id))')
banco_inicial.commit()
banco_inicial.close()

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_criptografada = generate_password_hash(senha)

        try:
            banco = conectar()
            banco.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha_criptografada))
            banco.commit()
            banco.close()
            return redirect('/login')
        except:
            return "Erro: Esse email já existe."

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        banco = conectar()
        usuario = banco.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        banco.close()

        if usuario and check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = usuario['id']
            session['nome'] = usuario['nome']
            return redirect('/')
        else:
            return "Email ou senha errados."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect('/login')

    try:
        resposta = requests.get("https://api.adviceslip.com/advice").json()
        conselho = resposta['slip']['advice']
    except:
        conselho = "Bora estudar!"

    return render_template('index.html', conselho=conselho)

@app.route('/api/tarefas')
def api_tarefas():
    if 'usuario_id' not in session:
        return jsonify([])

    status = request.args.get('status', 'todas')
    banco = conectar()

    if status == 'todas':
        tarefas = banco.execute('SELECT * FROM tarefas WHERE usuario_id = ?', (session['usuario_id'],)).fetchall()
    else:
        tarefas = banco.execute('SELECT * FROM tarefas WHERE usuario_id = ? AND status = ?', (session['usuario_id'], status)).fetchall()
    
    banco.close()

    lista_tarefas = []
    for t in tarefas:
        lista_tarefas.append({
            'id': t['id'],
            'titulo': t['titulo'],
            'descricao': t['descricao'],
            'status': t['status']
        })
        
    return jsonify(lista_tarefas)

@app.route('/nova_tarefa', methods=['POST'])
def nova_tarefa():
    if 'usuario_id' not in session:
        return redirect('/login')

    titulo = request.form['titulo']
    descricao = request.form['descricao']

    banco = conectar()
    banco.execute('INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, "pendente", ?)', (titulo, descricao, session['usuario_id']))
    banco.commit()
    banco.close()

    return redirect('/')

@app.route('/excluir/<int:id>')
def excluir(id):
    if 'usuario_id' not in session:
        return redirect('/login')

    banco = conectar()
    banco.execute('DELETE FROM tarefas WHERE id = ? AND usuario_id = ?', (id, session['usuario_id']))
    banco.commit()
    banco.close()

    return redirect('/')

@app.route('/editar_status/<int:id>', methods=['POST'])
def editar_status(id):
    if 'usuario_id' not in session:
        return redirect('/login')

    novo_status = request.form['status']
    
    banco = conectar()
    banco.execute('UPDATE tarefas SET status = ? WHERE id = ? AND usuario_id = ?', (novo_status, id, session['usuario_id']))
    banco.commit()
    banco.close()

    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/api/grafico')
def api_grafico():
    if 'usuario_id' not in session:
        return jsonify({})

    banco = conectar()
    pendentes = banco.execute('SELECT COUNT(*) FROM tarefas WHERE status="pendente" AND usuario_id=?', (session['usuario_id'],)).fetchone()[0]
    andamento = banco.execute('SELECT COUNT(*) FROM tarefas WHERE status="em andamento" AND usuario_id=?', (session['usuario_id'],)).fetchone()[0]
    concluidas = banco.execute('SELECT COUNT(*) FROM tarefas WHERE status="concluída" AND usuario_id=?', (session['usuario_id'],)).fetchone()[0]
    banco.close()

    return jsonify({
        'pendentes': pendentes,
        'andamento': andamento,
        'concluidas': concluidas
    })

if __name__ == '__main__':
    app.run(debug=True)
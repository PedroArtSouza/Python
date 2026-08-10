from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import requests # Para a API externa

app = Flask(__name__)
# Professor pediu pra configurar a SECRET_KEY
app.secret_key = 'chave_super_secreta_do_3_ano'

# Função pra conectar no banco SQLite3
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Cria as tabelas se não existirem logo que o código rodar
def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    status TEXT DEFAULT 'pendente',
                    usuario_id INTEGER,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id))''')
    conn.commit()
    conn.close()

init_db()

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        # O professor pediu pra usar hash na senha!
        senha_hash = generate_password_hash(senha)
        
        try:
            conn = get_db()
            conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha_hash))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except:
            return "Erro: Email já cadastrado."
            
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        # Valida o hash da senha
        if user and check_password_hash(user['senha'], senha):
            session['usuario_id'] = user['id']
            session['nome'] = user['nome']
            return redirect(url_for('index'))
        else:
            return "Email ou senha incorretos."
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- ROTAS DO PAINEL E TAREFAS ---

@app.route('/')
def index():
    # Protegendo a rota com session
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    # API Externa: pegando um conselho aleatório pra colocar no topo da página
    conselho = "Foque nos estudos!"
    try:
        resposta = requests.get("https://api.adviceslip.com/advice").json()
        conselho = resposta['slip']['advice']
    except:
        pass # Se der erro na internet, ignora

    return render_template('index.html', conselho=conselho)

# Rota que retorna JSON para atualizar a lista sem recarregar a página (exigência da página 2)
@app.route('/api/tarefas')
def get_tarefas():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autorizado'})
        
    status = request.args.get('status', 'todas')
    conn = get_db()
    
    if status == 'todas':
        tarefas = conn.execute('SELECT * FROM tarefas WHERE usuario_id = ?', (session['usuario_id'],)).fetchall()
    else:
        tarefas = conn.execute('SELECT * FROM tarefas WHERE usuario_id = ? AND status = ?', (session['usuario_id'], status)).fetchall()
    conn.close()
    
    # Converte as linhas do banco pra dicionário pra virar JSON
    lista = [{'id': t['id'], 'titulo': t['titulo'], 'descricao': t['descricao'], 'status': t['status']} for t in tarefas]
    return jsonify(lista)

@app.route('/nova_tarefa', methods=['POST'])
def nova_tarefa():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    
    conn = get_db()
    conn.execute('INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)', 
                 (titulo, descricao, 'pendente', session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/excluir/')
def excluir(id):
    if 'usuario_id' not in session: return redirect(url_for('login'))
    
    conn = get_db()
    conn.execute('DELETE FROM tarefas WHERE id = ? AND usuario_id = ?', (id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/editar_status/', methods=['POST'])
def editar_status(id):
    if 'usuario_id' not in session: return redirect(url_for('login'))
    
    novo_status = request.form['status']
    conn = get_db()
    conn.execute('UPDATE tarefas SET status = ? WHERE id = ? AND usuario_id = ?', (novo_status, id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- DASHBOARD (Gráfico) ---

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    return render_template('dashboard.html')

# Retorna os dados em JSON para o Chart.js ler
@app.route('/api/grafico')
def api_grafico():
    if 'usuario_id' not in session: return jsonify({})
    
    conn = get_db()
    pendentes = conn.execute("SELECT COUNT(*) FROM tarefas WHERE status='pendente' AND usuario_id=?", (session['usuario_id'],)).fetchone()[0]
    andamento = conn.execute("SELECT COUNT(*) FROM tarefas WHERE status='em andamento' AND usuario_id=?", (session['usuario_id'],)).fetchone()[0]
    concluidas = conn.execute("SELECT COUNT(*) FROM tarefas WHERE status='concluída' AND usuario_id=?", (session['usuario_id'],)).fetchone()[0]
    conn.close()
    
    return jsonify({
        'pendentes': pendentes,
        'andamento': andamento,
        'concluidas': concluidas
    })

if __name__ == '__main__':
    # Professor pediu DEBUG=False em produção, mas pra testar na nossa máquina tem que ser True
    app.run(debug=True)
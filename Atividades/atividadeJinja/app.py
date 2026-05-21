from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def atv1():
    name = "Pedro"
    return render_template('index.html', name=name)
    
@app.route('/atv2')
def atv2():
    name2 = "Lucas"
    idade = 26
    return render_template('atv2.html', name2 = name2, idade = idade) 

@app.route('/atv3')
def atv3():
    usuario_dados = {
        "nome" : "Ana",
        "email" : "ana@email.com",
    }
    
    return render_template('atv3.html', usuario = usuario_dados)

@app.route('/atv4')
def atv4():
    lista_alunos = [
        "Riki",
        "Kai",
        "kenma",
        "Cleiton",
    ]
    
    return render_template('atv4.html', alunos = lista_alunos)

@app.route('/atv5')
def atv5():
    notas_alunos = [
        {"nome" : "Lucas", "nota" : 10},
        {"nome" : "Pedro", "nota": 7},
        {"nome" : "Ian", "nota": 5},
    ]
    
    return render_template("atv5.html", boletim = notas_alunos)

if __name__ == "__main__":
    app.run(debug = True)
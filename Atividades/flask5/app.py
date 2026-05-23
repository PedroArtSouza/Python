from flask import Flask, request, render_template

app = Flask(__name__)

lista_login_perm = {
    "pedro" : "22400400",
    "janaina" : "cotemig2026",
    "dolga" : "cotemig2026",
    "antonio" : "cotemig2026",
}



@app.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        usuario_dig = request.form.get('usuario')
        senha_dig = request.form.get('senha')
        
        acesso_liberado = False
        
        for usuario, senha in lista_login_perm.items():
            if usuario_dig == usuario and senha_dig == senha:
                acesso_liberado = True
                break
            
        
        if acesso_liberado == True:
            return f"<h1>Bem vindo {usuario_dig}</h1>"
        
        else:
            return f"<h1>Acesso negado.<br>Usuario ou senha incorreta</h1>"
    
    return render_template('index.html')
                    
    

if __name__ == "__main__":
    app.run(debug=True)
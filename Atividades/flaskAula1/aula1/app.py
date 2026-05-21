from flask import Flask

app = Flask(__name__)

@app.route("/home")
def home():
    return '''
    <h1>Explicação decorator flask<h1>
    
    <br>
    
    <h2>O que é um decorator em Python?<h2>
    
    <p>Um decorator (decorador) é uma função que recebe outra função como argumento, estende ou modifica o comportamento dessa 
    função sem alterar o código-fonte original dela, e retorna uma nova função modificada. Em Python, eles são identificados pelo símbolo 
    @ colocado acima da definição de uma função.
    <p>
    
    <h2>Para que ele serve?<h2>
    
    <p>Os decorators servem para reutilização de código e separação de conceitos. 
    Eles permitem aplicar uma mesma lógica a várias funções diferentes de forma limpa. 
    Exemplos de uso comum:
    - Controlar acesso (verificar se usuário está logado antes de abrir uma página).
    - Medir o tempo de execução de funções (logs e monitoramento).Validar dados de entrada.
    - Registrar caminhos e URLs (como faz o Flask).
    <p>
    
    <h2>Como ele é utilizado no Flask (O caso do @app.route)<h2>
    
    <p>No Flask, o @app.route("/caminho") é um decorator que gerencia o roteamento da aplicação.
    1 - O problema sem decorator: O Flask precisaria de uma lista manual gigante mapeando cada URL para cada função criada por você.
    2 - A solução com decorator: Quando você coloca @app.route("/decorator") acima de uma função, você está dizendo explicitamente ao Flask: "Guarde esta função na sua memória. 
    Quando um usuário acessar o endereço /decorator no navegador, execute esta função e envie o retorno dela para a tela".<p>
'''

if __name__ == "__main__":
    app.run(debug = True)
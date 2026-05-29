# Importa a biblioteca 'math' do Python para podermos usar funções matemáticas complexas, como raiz quadrada e logaritmo.
import math
# Importa do Flask as ferramentas para renderizar o HTML (render_template) e pegar os dados do formulário (request).
from flask import render_template, request

def calcular():
    # 1. INICIALIZAÇÃO DE VARIÁVEIS
    # Declaramos essas variáveis vazias logo de cara para garantir que elas existam na memória.
    # Isso evita aquele "UnboundLocalError" que travava a aplicação caso o código não entrasse em nenhum 'if'.
    etapas = ""
    resultado = ""
    
    # 2. CAPTURA DOS DADOS OBRIGATÓRIOS
    # Todo cálculo precisa de pelo menos um número e uma operação. 
    # O 'float()' converte o texto que vem do HTML em um número decimal (com vírgula).
    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]

    # 3. VERIFICAÇÃO INTELIGENTE DE VARIÁVEIS (Evita pedir o que não precisa)
    
    # Se a operação NÃO for raiz quadrada (sqrt) e NÃO for logaritmo (log), obrigatoriamente precisamos do num2.
    if operacao not in ["sqrt", "log"]:
        # Pegamos o valor com '.get()' para não dar erro se o campo não existir, e usamos '.strip()' para remover espaços em branco invisíveis.
        num2_valor = request.form.get("num2", "").strip()
        
        # Se o num2_valor estiver vazio (o usuário não digitou nada), a gente devolve a tela com um aviso.
        if not num2_valor:
            return render_template("index.html", etapas="Informe o segundo número para esta operação.", resultado="")
        
        # Se passou pela verificação, convertemos para número decimal.
        num2 = float(num2_valor)
        
    # Se a operação for Bhaskara, a gente também precisa do num3 (o coeficiente 'c').
    if operacao == "bhaskara":
        num3_valor = request.form.get("num3", "").strip()
        
        # Mesmo esquema de segurança: se estiver vazio, devolve um aviso e para a execução.
        if not num3_valor:
            return render_template("index.html", etapas="Informe o terceiro número para esta operação.", resultado="")
        
        # Convertemos para número decimal.
        num3 = float(num3_valor)

    # 4. O CORAÇÃO DA CALCULADORA (Lógica Matemática)
    # Aqui o Python decide qual conta fazer baseado na 'operacao' que veio do <select> do HTML.

    if operacao == "+":
        resultado = num1 + num2
        # A letra 'f' antes das aspas (f-string) permite colocar as variáveis diretamente dentro do texto usando chaves {}.
        etapas = f"{num1} + {num2} = {resultado}"
        
    elif operacao == "-":
        resultado = num1 - num2
        etapas = f"{num1} - {num2} = {resultado}"
        
    elif operacao == "*":
        resultado = num1 * num2
        etapas = f"{num1} * {num2} = {resultado}"
        
    elif operacao == "/":
        # Verificação de segurança: a matemática não permite dividir por zero.
        if num2 == 0:
            resultado = "Erro"
            etapas = "Não é possível dividir por zero."
        else:
            resultado = num1 / num2
            etapas = f"{num1} / {num2} = {resultado}"
            
    elif operacao == "**":
        # No Python, dois asteriscos (**) significam potência (ex: num1 elevado a num2).
        resultado = num1 ** num2
        etapas = f"{num1} ^ {num2} = {resultado}"

    elif operacao == "sqrt":
        # Verificação: Não existe raiz real de número negativo.
        if num1 < 0:
            resultado = "Erro"
            etapas = "Não existe raiz real de número negativo."
        else:
            resultado = math.sqrt(num1) # Usa a biblioteca math para calcular a raiz
            etapas = f"√{num1} = {resultado}"
            
    elif operacao == "log":
        # Verificação: Só existe logaritmo de números estritamente maiores que zero.
        if num1 <= 0:
            resultado = "Erro"
            etapas = "O número para logaritmo deve ser maior que zero."
        else:
            resultado = math.log10(num1) # Calcula o logaritmo na base 10
            etapas = f"log10({num1}) = {resultado}"
            
    elif operacao == "bhaskara":
        # Fórmula do Delta (b² - 4ac). Aqui num1 = a, num2 = b, num3 = c.
        delta = (num2 ** 2) - (4 * num1 * num3)
        
        # Verificação 1: Se 'a' for zero, não é uma equação do segundo grau.
        if num1 == 0:
            resultado = "Erro"
            etapas = "O coeficiente 'a' (num1) deve ser diferente de zero."
        # Verificação 2: Se o Delta for negativo, não temos raízes reais.
        elif delta < 0:
            resultado = "Sem raízes reais"
            etapas = "A equação não possui raízes reais (delta negativo)."
        # Se passou pelos erros, fazemos o cálculo final de Bhaskara.
        else:
            # Guardamos as duas respostas dentro de uma lista [x1, x2]
            resultado = [
                (-num2 + math.sqrt(delta)) / (2 * num1), # Cálculo do x1 (+)
                (-num2 - math.sqrt(delta)) / (2 * num1)  # Cálculo do x2 (-)
            ]
            # Imprimimos acessando a posição 0 (x1) e a posição 1 (x2) da lista.
            etapas = f"Raízes encontradas: x1 = {resultado[0]}, x2 = {resultado[1]}"

    # 5. RETORNO PARA O USUÁRIO
    # Pega o arquivo 'index.html', e injeta as variáveis 'etapas' e 'resultado' 
    # nos espaços com {{ }} que você preparou lá no front-end.
    return render_template('index.html', etapas=etapas, resultado=resultado)
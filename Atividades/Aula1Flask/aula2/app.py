from flask import Flask

app = Flask(__name__)

@app.route("/")
def curriculo():
    return '''
    <h1>Currículo Profissional<h1>

    <br>

    <h2>Informações Pessoais<h2>
    <p>Nome: {{ nome }}<p>
    <p>Cargo Alvo: {{ cargo }}<p>
    <p>Contato: {{ email }} | {{ telefone }}<p>
    <p>Localização: {{ cidade }} - {{ estado }}<p>

    <br>

    <h2>Resumo Profissional<h2>
    <p>{{ resumo }}<p>

    <br>

    <h2>Experiência Profissional<h2>
    {% for exp in experiencias %}
    <p>- {{ exp.cargo }} na empresa {{ exp.empresa }} ({{ exp.inicio }} até {{ exp.fim }})<p>
    <p>Descrição das atividades: {{ exp.descricao }}<p>
    <br>
    {% else %}
    <p>Buscando inserção no mercado de trabalho.<p>
    {% endfor %}

    <br>

    <h2>Formação Acadêmica<h2>
    {% for curso in formacoes %}
    <p>- {{ curso.nome_curso }} pela instituição {{ curso.instituicao }} (Conclusão: {{ curso.ano_conclusao }})<p>
    {% endfor %}

    <br>

    <h2>Habilidades Técnicas e Competências<h2>
    <p>Tecnologias e conhecimentos práticos dominados:<p>
    {% for habilidade in habilidades %}
    <p>* {{ habilidade }}<p>
    {% endfor %}
'''

if __name__ == "__main__":
    app.run(debug = True)
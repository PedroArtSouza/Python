from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Jinja2')
def page1():
    return render_template("jinja2.html")

@app.route('/exemplo_flask')
def page2():
    return render_template("p3.html")

@app.route('/exemplo_Jinja2')
def page3():
    return render_template("p4.html")

if __name__ == "__main__":
    app.run(debug = True)
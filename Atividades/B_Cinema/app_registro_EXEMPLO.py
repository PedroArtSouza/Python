from flask import Blueprints, render_template
from controllers.cinema_controller import cinema_bp

cinema_bp = Blueprints('cinema', __name__)
# BLUEPRINT cinema — importar + registrar no app.py
@cinema_bp.route('/cinema')
def index():
    return render_template('layout.html')
# layout.html: url_for('cinema.index') → apelido "cinema" + função "index"
    
app.register_blueprint(cinema_bp)

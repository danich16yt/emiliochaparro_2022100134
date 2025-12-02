from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui-cambiar-en-produccion'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contraseña@localhost/ganaderia_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# Modelos
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    lotes = db.relationship('Lote', backref='categoria', lazy=True)

class Lote(db.Model):
    __tablename__ = 'lotes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    peso_promedio = db.Column(db.Float)
    edad_aproximada = db.Column(db.String(50))
    raza = db.Column(db.String(100))
    precio = db.Column(db.Decimal(10, 2), nullable=False)
    imagen = db.Column(db.String(200))
    detalles = db.Column(db.Text)
    ubicacion = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)

class Consulta(db.Model):
    __tablename__ = 'consultas'
    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    horario_llamada = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text)
    fecha_consulta = db.Column(db.DateTime, default=datetime.utcnow)
    atendida = db.Column(db.Boolean, default=False)

# Rutas públicas
@app.route('/')
def index():
    categorias = Categoria.query.all()
    lotes_destacados = Lote.query.filter_by(activo=True).order_by(Lote.fecha_publicacion.desc()).limit(6).all()
    return render_template('index.html', categorias=categorias, lotes_destacados=lotes_destacados)

@app.route('/categoria/<int:categoria_id>')
def categoria(categoria_id):
    cat = Categoria.query.get_or_404(categoria_id)
    lotes = Lote.query.filter_by(categoria_id=categoria_id, activo=True).all()
    categorias = Categoria.query.all()
    return render_template('categoria.html', categoria=cat, lotes=lotes, categorias=categorias)

@app.route('/consulta', methods=['POST'])
def nueva_consulta():
    try:
        consulta = Consulta(
            nombre_apellido=request.form.get('nombre_apellido'),
            correo=request.form.get('correo'),
            celular=request.form.get('celular'),
            horario_llamada=request.form.get('horario_llamada'),
            mensaje=request.form.get('mensaje', '')
        )
        db.session.add(consulta)
        db.session.commit()
        flash('¡Gracias por tu consulta! Nos contactaremos contigo pronto.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al enviar la consulta. Por favor intenta nuevamente.', 'error')
    
    return redirect(url_for('index'))

# Rutas de administración (básicas)
@app.route('/dashboard')
def dashboard():
    total_lotes = Lote.query.filter_by(activo=True).count()
    total_consultas = Consulta.query.filter_by(atendida=False).count()
    lotes_recientes = Lote.query.order_by(Lote.fecha_publicacion.desc()).limit(10).all()
    consultas_pendientes = Consulta.query.filter_by(atendida=False).order_by(Consulta.fecha_consulta.desc()).limit(10).all()
    categorias = Categoria.query.all()
    
    return render_template('dashboard.html', 
                         total_lotes=total_lotes,
                         total_consultas=total_consultas,
                         lotes_recientes=lotes_recientes,
                         consultas_pendientes=consultas_pendientes,
                         categorias=categorias)

@app.route('/dashboard/consulta/<int:id>/atender', methods=['POST'])
def marcar_atendida(id):
    consulta = Consulta.query.get_or_404(id)
    consulta.atendida = True
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
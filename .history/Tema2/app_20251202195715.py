from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui-cambiar-en-produccion'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contraseña@localhost/ganaderia_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para consultas
class Consulta(db.Model):
    __tablename__ = 'consultas'
    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    horario_llamada = db.Column(db.String(50), nullable=False)
    fecha_consulta = db.Column(db.DateTime, default=datetime.utcnow)

# Datos precargados de categorías
CATEGORIAS = [
    {
        'id': 1,
        'nombre': 'Ternero/a',
        'descripcion': 'Bovino joven, generalmente al pie de la madre'
    },
    {
        'id': 2,
        'nombre': 'Novillito',
        'descripcion': 'Macho castrado de destete hasta aproximadamente los dos años'
    },
    {
        'id': 3,
        'nombre': 'Novillo',
        'descripcion': 'Macho castrado de más de dos años'
    },
    {
        'id': 4,
        'nombre': 'Vaquillona',
        'descripcion': 'Hembra desde el destete hasta su primera parición'
    },
    {
        'id': 5,
        'nombre': 'Vaca',
        'descripcion': 'Hembra adulta'
    },
    {
        'id': 6,
        'nombre': 'Toro',
        'descripcion': 'Macho entero (no castrado)'
    }
]

# Datos precargados de lotes
LOTES = [
    {
        'id': 1,
        'nombre': 'Lote Terneros Brahman',
        'categoria_id': 1,
        'categoria': 'Ternero/a',
        'cantidad': 50,
        'imagen': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=500',
        'detalles': 'Terneros raza Brahman, excelente genética, aptos para engorde o cría. Vacunados y desparasitados.',
        'precio': 2500000
    },
    {
        'id': 2,
        'nombre': 'Lote Novillitos Angus',
        'categoria_id': 2,
        'categoria': 'Novillito',
        'cantidad': 30,
        'imagen': 'https://images.unsplash.com/photo-1560493676-04071c5f467b?w=500',
        'detalles': 'Novillitos Angus de 18 meses, peso promedio 350kg. Ideales para terminación en feedlot.',
        'precio': 4200000
    },
    {
        'id': 3,
        'nombre': 'Lote Novillos Hereford',
        'categoria_id': 3,
        'categoria': 'Novillo',
        'cantidad': 40,
        'imagen': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=500',
        'detalles': 'Novillos Hereford de 30 meses, peso promedio 480kg. Listos para faena o engorde.',
        'precio': 5800000
    },
    {
        'id': 4,
        'nombre': 'Lote Vaquillonas Bradford',
        'categoria_id': 4,
        'categoria': 'Vaquillona',
        'cantidad': 25,
        'imagen': 'https://images.unsplash.com/photo-1588692426717-9930a0b3a443?w=500',
        'detalles': 'Vaquillonas Bradford de 24 meses, preñadas. Excelente para iniciar producción lechera o cárnica.',
        'precio': 5500000
    },
    {
        'id': 5,
        'nombre': 'Lote Vacas Holando',
        'categoria_id': 5,
        'categoria': 'Vaca',
        'cantidad': 20,
        'imagen': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=500',
        'detalles': 'Vacas Holando en producción, promedio 25 litros diarios. Excelente salud y genética.',
        'precio': 7000000
    },
    {
        'id': 6,
        'nombre': 'Lote Toros Nelore',
        'categoria_id': 6,
        'categoria': 'Toro',
        'cantidad': 5,
        'imagen': 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=500',
        'detalles': 'Toros Nelore de 3 años, excelente conformación. Aptos para servicio en rodeos de cría.',
        'precio': 12000000
    }
]

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/inicio')
def inicio():
    return render_template('index.html', categorias=CATEGORIAS, lotes=LOTES)

@app.route('/categoria/<int:categoria_id>')
def categoria(categoria_id):
    categoria = next((c for c in CATEGORIAS if c['id'] == categoria_id), None)
    if not categoria:
        return redirect(url_for('inicio'))
    
    lotes = [l for l in LOTES if l['categoria_id'] == categoria_id]
    return render_template('categoria.html', categoria=categoria, lotes=lotes, categorias=CATEGORIAS)

@app.route('/consulta', methods=['POST'])
def nueva_consulta():
    try:
        consulta = Consulta(
            nombre_apellido=request.form.get('nombre_apellido'),
            correo=request.form.get('correo'),
            celular=request.form.get('celular'),
            horario_llamada=request.form.get('horario_llamada')
        )
        db.session.add(consulta)
        db.session.commit()
        flash('Gracias por tu consulta. Nos contactaremos contigo pronto.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al enviar la consulta. Intenta nuevamente.', 'error')
    
    return redirect(url_for('inicio') + '#contacto')

@app.route('/dashboard')
def dashboard():
    consultas = Consulta.query.order_by(Consulta.fecha_consulta.desc()).all()
    return render_template('dashboard.html', consultas=consultas)

if __name__ == '__main__':
    app.run(debug=True)
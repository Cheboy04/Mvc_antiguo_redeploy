from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'ventas.db'

def init_db():
    """Inicializar la base de datos con las tablas necesarias"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Crear tabla Vendedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Crear tabla Reglas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reglas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            porcentaje_minimo REAL NOT NULL,
            porcentaje_maximo REAL NOT NULL,
            comision REAL NOT NULL
        )
    ''')
    
    # Crear tabla Ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendedor_id INTEGER NOT NULL,
            fecha DATE NOT NULL,
            monto REAL NOT NULL,
            comision REAL DEFAULT 0,
            regla_aplicada_id INTEGER,
            FOREIGN KEY (vendedor_id) REFERENCES vendedores (id),
            FOREIGN KEY (regla_aplicada_id) REFERENCES reglas (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def cargar_datos_ejemplo():
    """Cargar datos de ejemplo en la base de datos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM vendedores")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Insertar vendedores
    vendedores = [
        ('Juan Pérez', 'juan@empresa.com'),
        ('María García', 'maria@empresa.com'),
        ('Carlos López', 'carlos@empresa.com')
    ]
    cursor.executemany("INSERT INTO vendedores (nombre, email) VALUES (?, ?)", vendedores)
    
    # Insertar reglas de comisión
    reglas = [
        ('Básica', 0, 1000, 0.05),
        ('Intermedia', 1001, 5000, 0.08),
        ('Avanzada', 5001, 10000, 0.12),
        ('Premium', 10001, 999999, 0.15)
    ]
    cursor.executemany("INSERT INTO reglas (nombre, porcentaje_minimo, porcentaje_maximo, comision) VALUES (?, ?, ?, ?)", reglas)
    
    # Insertar ventas de ejemplo
    ventas = [
        (1, '2024-01-15', 2500),
        (2, '2024-01-20', 8000),
        (1, '2024-02-05', 1200),
        (3, '2024-02-12', 15000),
        (2, '2024-02-18', 3500)
    ]
    cursor.executemany("INSERT INTO ventas (vendedor_id, fecha, monto) VALUES (?, ?, ?)", ventas)
    
    # Calcular comisiones para todas las ventas
    cursor.execute("SELECT id, monto FROM ventas")
    ventas_actuales = cursor.fetchall()
    
    for venta_id, monto in ventas_actuales:
        cursor.execute("""
            SELECT id, comision FROM reglas 
            WHERE ? BETWEEN porcentaje_minimo AND porcentaje_maximo
        """, (monto,))
        regla = cursor.fetchone()
        
        if regla:
            regla_id, comision_porcentaje = regla
            comision = monto * comision_porcentaje
            cursor.execute("""
                UPDATE ventas 
                SET comision = ?, regla_aplicada_id = ? 
                WHERE id = ?
            """, (comision, regla_id, venta_id))
    
    conn.commit()
    conn.close()

def calcular_comision(monto):
    """Calcular comisión basada en el monto de venta"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nombre, comision FROM reglas 
        WHERE ? BETWEEN porcentaje_minimo AND porcentaje_maximo
    """, (monto,))
    
    regla = cursor.fetchone()
    conn.close()
    
    if regla:
        return {
            'comision': monto * regla[2],
            'regla_id': regla[0],
            'regla_nombre': regla[1]
        }
    return {'comision': 0, 'regla_id': None, 'regla_nombre': None}

# Rutas de la aplicación
@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/ventas/filtrar', methods=['POST'])
def filtrar_ventas():
    """Filtrar ventas por rango de fechas"""
    try:
        data = request.get_json()
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({'error': 'Fechas requeridas'}), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                v.id,
                v.fecha,
                v.monto,
                v.comision,
                vend.nombre as vendedor_nombre,
                r.nombre as regla_nombre
            FROM ventas v
            JOIN vendedores vend ON v.vendedor_id = vend.id
            LEFT JOIN reglas r ON v.regla_aplicada_id = r.id
            WHERE v.fecha BETWEEN ? AND ?
            ORDER BY v.fecha DESC
        """, (fecha_inicio, fecha_fin))
        
        ventas = []
        for row in cursor.fetchall():
            ventas.append({
                'id': row[0],
                'fecha': row[1],
                'monto': row[2],
                'comision': row[3],
                'vendedor_nombre': row[4],
                'regla_nombre': row[5] or 'N/A'
            })
        
        # Calcular totales
        cursor.execute("""
            SELECT 
                COUNT(*) as cantidad,
                SUM(monto) as total_ventas,
                SUM(comision) as total_comisiones
            FROM ventas 
            WHERE fecha BETWEEN ? AND ?
        """, (fecha_inicio, fecha_fin))
        
        totales = cursor.fetchone()
        conn.close()
        
        return jsonify({
            'ventas': ventas,
            'totales': {
                'cantidad': totales[0],
                'total_ventas': totales[1] or 0,
                'total_comisiones': totales[2] or 0
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/datos/cargar', methods=['POST'])
def cargar_datos():
    """Cargar datos de ejemplo"""
    try:
        cargar_datos_ejemplo()
        return jsonify({'mensaje': 'Datos cargados exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ventas/agregar', methods=['POST'])
def agregar_venta():
    """Agregar una nueva venta"""
    try:
        data = request.get_json()
        vendedor_id = data.get('vendedor_id')
        fecha = data.get('fecha')
        monto = data.get('monto')
        
        if not all([vendedor_id, fecha, monto]):
            return jsonify({'error': 'Todos los campos son requeridos'}), 400
        
        # Calcular comisión
        resultado_comision = calcular_comision(monto)
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO ventas (vendedor_id, fecha, monto, comision, regla_aplicada_id)
            VALUES (?, ?, ?, ?, ?)
        """, (vendedor_id, fecha, monto, resultado_comision['comision'], resultado_comision['regla_id']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'mensaje': 'Venta agregada exitosamente'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vendedores', methods=['GET'])
def obtener_vendedores():
    """Obtener lista de vendedores"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, email FROM vendedores ORDER BY nombre")
        vendedores = [{'id': row[0], 'nombre': row[1], 'email': row[2]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(vendedores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Inicializar base de datos
    init_db()
    cargar_datos_ejemplo()
    
    # Ejecutar aplicación
    app.run(debug=True, host='0.0.0.0', port=5000) 
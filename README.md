# 🏢 Sistema de Comisiones de Ventas - Flask MVC

## 📹 Video Explicativo
**Tutorial: Filtrado por fechas y cálculo de comisiones con Flask MVC**

En este video se explica paso a paso cómo crear un proyecto Flask MVC desde cero, implementando un sistema de comisiones de ventas con filtrado por fechas y cálculo automático de comisiones basado en reglas de negocio.

🔗 **Link del Video:** https://youtu.be/lY4HlocDEd8

## 📋 Descripción del Proyecto

Este proyecto implementa un **Sistema de Comisiones de Ventas** utilizando el framework **Flask** con patrón arquitectónico **MVC (Model-View-Controller)**. El sistema permite:

- ✅ Filtrar ventas por rango de fechas
- ✅ Calcular comisiones automáticamente basadas en reglas de negocio
- ✅ Gestionar 3 tablas relacionadas: Vendedores, Ventas y Reglas
- ✅ API REST para operaciones principales
- ✅ Base de datos SQLite integrada
- ✅ Interfaz moderna y responsiva

## 🏗️ Arquitectura MVC Implementada

### 📊 Model (Modelo)
- **Base de Datos**: SQLite con 3 tablas relacionadas
- **Lógica de Negocio**: Funciones para cálculo de comisiones
- **Entidades**: Vendedores, Ventas y Reglas de comisión

### 🎨 View (Vista)
- **Templates**: HTML con Jinja2
- **Estilos**: CSS moderno y responsivo
- **JavaScript**: Interactividad del lado cliente

### 🎮 Controller (Controlador)
- **Flask Routes**: Manejo de rutas y peticiones
- **API REST**: Endpoints para operaciones principales
- **JavaScript**: Coordinación entre interfaz y servidor

## 🚀 Funcionalidades Principales

### 1. Filtrado por Fechas
- Selección de rango de fechas (inicio y fin)
- Validación automática de fechas
- Filtrado en tiempo real con AJAX

### 2. Cálculo de Comisiones
- **Regla Básica**: 5% para ventas hasta $1,000
- **Regla Intermedia**: 8% para ventas $1,001-$5,000
- **Regla Avanzada**: 12% para ventas $5,001-$10,000
- **Regla Premium**: 15% para ventas superiores a $10,000

### 3. API REST
- `GET /api/vendedores` - Listar vendedores
- `POST /api/ventas/filtrar` - Filtrar ventas por fechas
- `POST /api/ventas/agregar` - Agregar nueva venta
- `POST /api/datos/cargar` - Cargar datos de ejemplo

### 4. Gestión de Datos
- Carga automática de datos de ejemplo
- Persistencia en SQLite
- Relaciones entre tablas

## 📁 Estructura del Proyecto

```
Minicore/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── ventas.db             # Base de datos SQLite
├── templates/
│   └── index.html        # Plantilla principal
├── static/
│   ├── styles.css        # Estilos CSS
│   └── script.js         # JavaScript del cliente
└── README.md             # Documentación
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Templates**: Jinja2
- **API**: REST con JSON
- **Responsive Design**: CSS Grid y Flexbox

## 🎯 Cómo Usar el Sistema

### Instalación y Configuración

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

3. **Abrir en navegador**:
   ```
   http://localhost:5000
   ```

### Uso del Sistema

1. **Seleccionar fechas**: Elige el rango de fechas a filtrar
2. **Filtrar ventas**: Haz clic en "Filtrar Ventas"
3. **Ver resultados**: Revisa la tabla y el resumen de comisiones
4. **Agregar ventas**: Usa el formulario para agregar nuevas ventas

## 📊 Base de Datos

El sistema utiliza SQLite con 3 tablas relacionadas:

- **Vendedores**: Información de vendedores (id, nombre, email)
- **Ventas**: Registros de ventas con comisiones (id, vendedor_id, fecha, monto, comision, regla_aplicada_id)
- **Reglas**: Reglas de comisión por rangos (id, nombre, porcentaje_minimo, porcentaje_maximo, comision)

Las tablas están relacionadas mediante foreign keys para mantener la integridad de los datos.

## 👨‍💻 Información de Contacto

- **Nombre:** Xavier Gordillo
- **Email:** [xavier.gordillo@udla.edu.ec]
- **Universidad:** UDLA
- **Curso:** Ingeniería Web


## 🚀 Comandos Útiles

### Desarrollo
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en modo desarrollo
python app.py
```

Este proyecto es parte del curso de Ingeniería Web en la UDLA. Código educativo para fines de aprendizaje.
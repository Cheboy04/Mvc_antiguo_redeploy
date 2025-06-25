// ===== CONTROLADOR DEL LADO CLIENTE =====
class VentasController {
    constructor() {
        this.initializeElements();
        this.initializeEventListeners();
        this.cargarVendedores();
        this.setDefaultDates();
    }

    initializeElements() {
        // Filtros
        this.fechaInicioInput = document.getElementById('fechaInicio');
        this.fechaFinInput = document.getElementById('fechaFin');
        this.filtrarBtn = document.getElementById('filtrarBtn');
        
        // Tabla y resumen
        this.ventasBody = document.getElementById('ventasBody');
        this.resumenComisiones = document.getElementById('resumenComisiones');
        this.totalVentasElement = document.getElementById('totalVentas');
        this.totalComisionesElement = document.getElementById('totalComisiones');
        this.cantidadVentasElement = document.getElementById('cantidadVentas');
        
        // Formulario nueva venta
        this.formNuevaVenta = document.getElementById('formNuevaVenta');
        this.vendedorSelect = document.getElementById('vendedorSelect');
        this.fechaVentaInput = document.getElementById('fechaVenta');
        this.montoVentaInput = document.getElementById('montoVenta');
    }

    initializeEventListeners() {
        // Eventos de filtrado
        this.filtrarBtn.addEventListener('click', () => this.filtrarVentas());
        
        // Evento de formulario
        this.formNuevaVenta.addEventListener('submit', (e) => this.agregarVenta(e));
    }

    setDefaultDates() {
        // Establecer fechas por defecto (último mes)
        const hoy = new Date();
        const haceUnMes = new Date();
        haceUnMes.setMonth(hoy.getMonth() - 1);
        
        this.fechaInicioInput.value = haceUnMes.toISOString().split('T')[0];
        this.fechaFinInput.value = hoy.toISOString().split('T')[0];
    }

    // ===== MÉTODOS DE COMUNICACIÓN CON API =====

    async hacerRequest(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error en request:', error);
            this.mostrarMensaje(`Error: ${error.message}`, 'error');
            throw error;
        }
    }

    // ===== MÉTODOS DE VENTAS =====

    async filtrarVentas() {
        const fechaInicio = this.fechaInicioInput.value;
        const fechaFin = this.fechaFinInput.value;

        if (!this.validarFechas(fechaInicio, fechaFin)) {
            return;
        }

        try {
            this.mostrarCarga(true);
            
            const data = await this.hacerRequest('/api/ventas/filtrar', {
                method: 'POST',
                body: JSON.stringify({
                    fecha_inicio: fechaInicio,
                    fecha_fin: fechaFin
                })
            });

            this.mostrarVentas(data.ventas);
            this.mostrarResumen(data.totales);
            
            if (data.ventas.length > 0) {
                this.mostrarMensaje(`Se encontraron ${data.ventas.length} ventas`, 'success');
            } else {
                this.mostrarMensaje('No se encontraron ventas en el rango seleccionado', 'info');
            }
            
        } catch (error) {
            this.mostrarMensaje('Error al filtrar ventas', 'error');
        } finally {
            this.mostrarCarga(false);
        }
    }

    async agregarVenta(event) {
        event.preventDefault();
        
        const vendedorId = this.vendedorSelect.value;
        const fecha = this.fechaVentaInput.value;
        const monto = parseFloat(this.montoVentaInput.value);

        if (!vendedorId || !fecha || !monto) {
            this.mostrarMensaje('Por favor, completa todos los campos', 'error');
            return;
        }

        try {
            this.mostrarCarga(true);
            
            await this.hacerRequest('/api/ventas/agregar', {
                method: 'POST',
                body: JSON.stringify({
                    vendedor_id: parseInt(vendedorId),
                    fecha: fecha,
                    monto: monto
                })
            });

            this.mostrarMensaje('Venta agregada exitosamente', 'success');
            this.formNuevaVenta.reset();
            
            // Recargar ventas si hay filtros activos
            if (this.fechaInicioInput.value && this.fechaFinInput.value) {
                await this.filtrarVentas();
            }
            
        } catch (error) {
            this.mostrarMensaje('Error al agregar venta', 'error');
        } finally {
            this.mostrarCarga(false);
        }
    }

    async cargarVendedores() {
        try {
            const vendedores = await this.hacerRequest('/api/vendedores');
            this.vendedorSelect.innerHTML = '<option value="">Seleccionar vendedor...</option>';
            
            vendedores.forEach(vendedor => {
                const option = document.createElement('option');
                option.value = vendedor.id;
                option.textContent = vendedor.nombre;
                this.vendedorSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error al cargar vendedores:', error);
        }
    }

    // ===== MÉTODOS DE VISTA =====

    mostrarVentas(ventas) {
        if (ventas.length === 0) {
            this.ventasBody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 40px; color: #666;">
                        No se encontraron ventas en el rango seleccionado
                    </td>
                </tr>
            `;
            return;
        }

        this.ventasBody.innerHTML = ventas.map(venta => `
            <tr>
                <td>${venta.id}</td>
                <td>${venta.vendedor_nombre}</td>
                <td>${this.formatearFecha(venta.fecha)}</td>
                <td>$${venta.monto.toFixed(2)}</td>
                <td>$${venta.comision.toFixed(2)}</td>
                <td>${venta.regla_nombre}</td>
            </tr>
        `).join('');
    }

    mostrarResumen(totales) {
        this.totalVentasElement.textContent = `$${totales.total_ventas.toFixed(2)}`;
        this.totalComisionesElement.textContent = `$${totales.total_comisiones.toFixed(2)}`;
        this.cantidadVentasElement.textContent = totales.cantidad;
        this.resumenComisiones.style.display = 'block';
    }

    formatearFecha(fecha) {
        return new Date(fecha).toLocaleDateString('es-ES');
    }

    mostrarMensaje(mensaje, tipo = 'info') {
        // Crear elemento de mensaje
        const mensajeElement = document.createElement('div');
        mensajeElement.className = `mensaje mensaje-${tipo}`;
        mensajeElement.textContent = mensaje;
        
        // Insertar al inicio del contenedor
        const container = document.querySelector('.container');
        container.insertBefore(mensajeElement, container.firstChild);
        
        // Remover después de 3 segundos
        setTimeout(() => {
            mensajeElement.remove();
        }, 3000);
    }

    mostrarCarga(mostrar) {
        if (mostrar) {
            this.filtrarBtn.disabled = true;
            this.filtrarBtn.textContent = '⏳ Cargando...';
        } else {
            this.filtrarBtn.disabled = false;
            this.filtrarBtn.textContent = '🔍 Filtrar Ventas';
        }
    }

    validarFechas(fechaInicio, fechaFin) {
        if (!fechaInicio || !fechaFin) {
            this.mostrarMensaje('Por favor, selecciona ambas fechas', 'error');
            return false;
        }

        if (fechaInicio > fechaFin) {
            this.mostrarMensaje('La fecha de inicio debe ser anterior a la fecha de fin', 'error');
            return false;
        }

        return true;
    }
}

// ===== INICIALIZACIÓN DE LA APLICACIÓN =====
document.addEventListener('DOMContentLoaded', function() {
    // Crear instancia del controlador
    const controller = new VentasController();
    
    console.log('🚀 Sistema de Comisiones Flask iniciado correctamente');
    console.log('📊 Patrón MVC implementado:');
    console.log('   - Model: Flask + SQLite (maneja datos y lógica de negocio)');
    console.log('   - View: Templates HTML + CSS (maneja la interfaz de usuario)');
    console.log('   - Controller: Flask Routes + JavaScript (coordina modelo y vista)');
}); 
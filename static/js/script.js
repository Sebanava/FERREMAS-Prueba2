// Scripts personalizados para FERREMAS

// Funciones para el carrito de compras
document.addEventListener('DOMContentLoaded', function() {
    // Cerrar alertas automáticamente después de 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Validar formularios
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Función para actualizar cantidad en el carrito
function actualizarCantidad(productoId, accion) {
    const inputCantidad = document.getElementById('cantidad-' + productoId);
    let cantidad = parseInt(inputCantidad.value);
    
    if (accion === 'aumentar') {
        cantidad += 1;
    } else if (accion === 'disminuir' && cantidad > 1) {
        cantidad -= 1;
    }
    
    inputCantidad.value = cantidad;
}

// Función para mostrar detalles de pedido
function mostrarDetallesPedido(pedidoId) {
    // Esta función sería implementada con más detalle en una versión completa
    alert('Detalles del pedido ' + pedidoId);
}
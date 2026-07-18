// Variables CONST, las que nunca cambiaran en el proyecto
const formulario = document.querySelector("#formularioContacto");
const nombre = document.querySelector("#nombre");
const correo = document.querySelector("#correo");
const tipoSolicitud = document.querySelector("#tipoSolicitud");
const mensaje = document.querySelector("#mensaje");
const mensajeFormulario = document.querySelector("#mensajeFormulario");

// Funcion para validar el EMAIL que se introdujo 
function validarEmail(email) {
    return email.includes("@") && email.includes("."); // Nos aseguramos que el correo contenga @ y .
}

// Funcion para mostrar el mensaje, el cual tiene la syntaxis de darnos el "mensaje" con un respectivo color en caso de exito o fallo
function mostrarMensaje(texto, color) {
    mensajeFormulario.textContent = texto;
    mensajeFormulario.style.color = color;

}

// Detectamos el tipo de solicitud que requiere el User y si coloco algun tipo de solicitud en el "Textarea"
function detectarTipo() {
    const textoMensaje = mensaje.value.toLowerCase();
    if (textoMensaje.includes("compra")) { // Utilizamos "IF" para marcar una condicional
        tipoSolicitud.value = "compra";
    }
    else if (textoMensaje.includes("venta")) { // "ELSE IF" para decir "Si no, si" en esta condicional
        tipoSolicitud.value = "venta";
    }
    else { // "ELSE" para decir "Si no" o "En caso de lo contrario" en esta condicion anidada
        tipoSolicitud.value = "consulta";
    }
}

// Limpiamos el formulario para quitar los datos de los campos
function limpiarFormulario(){ 
    formulario.reset();
}

// Aca agregamos una funcion para validar si el formulario esta completo con todos sus campos obligatorios o no
function validarFormulario(evento) {
    evento.preventDefault();
    if ( // // Si los campos nombre, correo y mensaje estan vacios
        nombre.value.trim() === "" ||
        correo.value.trim() === "" ||
        mensaje.value.trim() === ""
    ) {
        mostrarMensaje("Todos los campos son obligatorios", "red");
        return;
    }

    
    if (!validarEmail(correo.value)) { // Condicional para ver si el User escribio un correo valido 
        mostrarMensaje("Ingrese un correo válido", "red");
        return;
    }

    // EN CASO DE FORMULARIO CORRECTO
    mostrarMensaje("Formulario enviado correctamente", "green");
    limpiarFormulario();
}


// Eventos previamente creados
formulario.addEventListener("submit", validarFormulario);
mensaje.addEventListener("input", detectarTipo);
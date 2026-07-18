// Variables constante para el boton de "Cambiar Tema" y "Fecha Actual"
const botonTema = document.querySelector("#modoOscuro");
const fecha = document.querySelector("#fechaActual");

// Creamos la funcion que hara cambiar el tema o el fondo de nuestra pagina 
function cambiarTema() {
    document.body.classList.toggle("bg-dark");
    document.body.classList.toggle("text-dark");
}

// Agregamos un EventListener para escuchar el evento cuando demos "click" en el boton
botonTema.addEventListener("click", cambiarTema);

// Creamos la funcion para mostrar la fecha actual 
function mostrarFecha() {
    const hoy = new Date();
    fecha.textContent = hoy.toLocaleDateString();
}

// Inicializamos el evento 
mostrarFecha();
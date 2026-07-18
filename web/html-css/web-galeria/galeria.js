// Creamos las variables constantes, es decir, las que son fijas y no cambiaran (CONST)
const modal = document.querySelector("#modal");
const imagenModal = document.querySelector("#imagenModal");
const tituloModal = document.querySelector("#tituloModal");
const textoModal = document.querySelector("#textoModal");
const cerrar = document.querySelector("#cerrarModal");

// Agregamos la funcion "abrirModal" para que al hacer click se abran los detalles de la obra
function abrirModal(imagen, titulo, texto) {
    imagenModal.src = imagen;
    tituloModal.textContent = titulo;
    textoModal.textContent = texto;
    modal.classList.remove("modal-oculto");
}

// Funcion "cerrarModal" para hacer justamente eso, cerrar los detalles
function cerrarModal() {
    modal.classList.add("modal-oculto");
}

// Agregamos esta funcion para eliminar de la grilla la imagen que seleccionemos
function eliminarImagen(idCard) {
    const card = document.querySelector(idCard);
    card.remove();
}

// Esta funcion escucha los eventos, especificamente el "click" que hacemos en la "X"
function eventosModal() {
    cerrar.addEventListener("click", cerrarModal);
}

// Esta es la funcion mas importante y dinamica, la que se encargara de escuchar los "clicks" en los botones que hemos creado
function eventosBotones() {

    // DETALLE Y CIERRE NUMERO 1
    document.querySelector("#detalle1").addEventListener("click", function() {
        abrirModal(
            "Imagenes/imagen_uno.jpg",
            "Explosión de Color",
            "Obra abstracta contemporánea llena de emociones y colores."
        );
    });

    document.querySelector("#eliminar1").addEventListener("click", function() {
        eliminarImagen("#card1");
    });


    
    // DETALLE Y CIERRE NUMERO 2
    document.querySelector("#detalle2").addEventListener("click", function() {
        abrirModal(
            "Imagenes/imagen_dos.jpg",
            "Geometría Creativa",
            "Composición conceptual moderna inspirada en formas abstractas."
        );
    });

    document.querySelector("#eliminar2").addEventListener("click", function() {
        eliminarImagen("#card2");
    });



    // DETALLE Y CIERRE NUMERO 3
    document.querySelector("#detalle3").addEventListener("click", function() {
        abrirModal(
            "Imagenes/imagen_tres.jpg",
            "Arte Experimental",
            "Obra de estilo experimental con contrastes intensos y formas simbólicas."
        );
    });

    document.querySelector("#eliminar3").addEventListener("click", function() {
        eliminarImagen("#card3");
    });


    // DETALLE Y CIERRE NUMERO 4
    document.querySelector("#detalle4").addEventListener("click", function() {
        abrirModal(
            "Imagenes/imagen_cuatro.jpg",
            "Expresion Contemporanea",
            "Una obra llena de colores y expresion artistica contemporanea"
        );
    });

    document.querySelector("#eliminar4").addEventListener("click", function() {
        eliminarImagen("#card4");
    });



    // DETALLE Y CIERRE NUMERO 5
    document.querySelector("#detalle5").addEventListener("click", function() {
        abrirModal(
            "Imagenes/imagen_cinco.jpg",
            "Conexion Ancestral",
            "Representacion artistica inspirada en nuestras raices y pasado cultural"
        );
    });

    document.querySelector("#eliminar5").addEventListener("click", function() {
        eliminarImagen("#card5");
    });



    // DETALLE Y CIERRE NUMERO 6 
    document.querySelector("#detalle6").addEventListener("click", function() {
        abrirModal(
            "Imagenes/imagen_seis.jpg",
            "Sociedad en Ruinas",
            "Escena abstracta que refleja el deterioro y caos de una sociedad moderna, un reflejo de la actualidad."
        );
    });

    document.querySelector("#eliminar6").addEventListener("click", function() {
        eliminarImagen("#card6");
    });
}

// Inicializamos los eventos previamente especificados mas arriba como "function"
eventosModal();
eventosBotones();
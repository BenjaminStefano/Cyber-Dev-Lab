let usuarios = [];
 
// Definimos variables constantes
const formulario = document.getElementById("formulario");
const listaUsuarios = document.getElementById("listaUsuarios");
 
// Agregamos el listener de un Evento
formulario.addEventListener("submit", agregarUsuario);
 

// Programamos la funcion "agregarUsuario", para tener las validaciones y datos correctos
function agregarUsuario(evento) {
 
    evento.preventDefault();
 
    let usuario = {
        nombre: document.getElementById("nombre").value.trim(),
        apellido: document.getElementById("apellido").value.trim(),
        fechaNacimiento: document.getElementById("fechaNacimiento").value,
        correo: document.getElementById("correo").value.trim(),
        cargo: document.getElementById("cargo").value,
        fechaIngreso: document.getElementById("fechaIngreso").value
    };
 
    // Validamos el hecho de que todos los campos esten completos
    if (
        !usuario.nombre ||
        !usuario.apellido ||
        !usuario.fechaNacimiento ||
        !usuario.correo ||
        !usuario.cargo ||
        !usuario.fechaIngreso
    ) {
        // En caso de no tener completos los campos, se envia una Alerta
        alert("Debe completar todos los campos.");
        return;
    }

    // Validamos que el Usuario/Empleado no se haya agregado anteriormente o que no sea existente
    let existe = usuarios.some(
        usuarioExistente =>
        usuarioExistente.correo.toLowerCase() ===
        usuario.correo.toLowerCase()
    );

    // Si existe, enviamos una alerta al User
    if(existe){
        alert("Ya existe un trabajador con ese correo");
        return;
    }

    // Validamos que la edad mínima sea de 18 años al ingresar
    let fechaNacimiento = new Date(usuario.fechaNacimiento);
    let fechaIngreso = new Date(usuario.fechaIngreso);
    let fechaMinimaIngreso = new Date(fechaNacimiento);

    fechaMinimaIngreso.setFullYear(
        fechaMinimaIngreso.getFullYear() >= 18
    );

    if (fechaIngreso < fechaMinimaIngreso) {
        alert(
            "La fecha de ingreso debe ser posterior a los 18 años de edad"
        );
        return;
    }

    if (confirm("¿Agregar usuario?")) {
        usuarios.push(usuario);
        mostrarUsuarios();
        formulario.reset();
        alert("Usuario agregado correctamente");
        }
    }

 

// Programamos la Funcion "mostrarUsuarios" para que los Empleados se muestren dentro de nuestra Lista 
function mostrarUsuarios() {

    if (usuarios.length === 0) {
    listaUsuarios.innerHTML = `
        <div class="col-12 text-center">
            <p> No hay empleados registrados </p>
        </div>
    `;
    return;
    }
 
    listaUsuarios.innerHTML = "";
 
    for(let i = 0; i < usuarios.length; i++){
 
        listaUsuarios.innerHTML += `
            <div class="col-md-4">
            <div class="card premium-card">
            <div class="card-body">
 
            <h5>${usuarios[i].nombre} ${usuarios[i].apellido}</h5>
            <p>${usuarios[i].correo}</p>
            <p>${usuarios[i].cargo}</p>

            <button
                class="btn-eliminar"     
                onclick="eliminarUsuario(${i})">
                Eliminar
            </button>

            </div>
            </div>
            </div>
                    `;
    }
}

// Funcion para eliminar el Empleado en caso de que lo necesitemos 
function eliminarUsuario(indice) {
    if(confirm("¿Deseas eliminar este trabajador?")){
        usuarios.splice(indice, 1);
        mostrarUsuarios();
    }
}

// Mostrar estado inicial de la lista
mostrarUsuarios();
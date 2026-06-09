const GRAPHQL_URL = "/graphql";

async function ejecutarGraphQL(query, variables = {}) {
    const response = await fetch(GRAPHQL_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json; charset=utf-8" },
        body: JSON.stringify({ query, variables }),
    });
    return response.json();
}

function mostrarResultado(elemento, contenido, tipo = "") {
    elemento.className = `resultado ${tipo}`.trim();
    elemento.innerHTML = contenido;
}

function formatearErrorGraphQL(payload) {
    if (payload.errors?.length) {
        return payload.errors.map((error) => error.message).join("\n");
    }
    return "Ocurrió un error inesperado";
}

function renderInventario(data) {
    if (!data.items.length) {
        return `<strong>${data.almacen.nombre}</strong> (ID ${data.almacen.id})<br>
                Dirección: ${data.almacen.direccion}<br><br>
                No hay productos registrados en esta sede.`;
    }

    const filas = data.items
        .map(
            (item) => `
            <tr>
                <td>${item.producto.id}</td>
                <td>${item.producto.nombre}</td>
                <td>${item.producto.categoria}</td>
                <td>$${Number(item.producto.precioUnitario).toFixed(2)}</td>
                <td>${item.cantidad}</td>
            </tr>`
        )
        .join("");

    return `
        <strong>${data.almacen.nombre}</strong> (ID ${data.almacen.id})<br>
        Dirección: ${data.almacen.direccion}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Producto</th>
                    <th>Categoría</th>
                    <th>Precio</th>
                    <th>Cantidad</th>
                </tr>
            </thead>
            <tbody>${filas}</tbody>
        </table>`;
}

function crearOpcionesAlmacen(almacenes, incluirPlaceholder = true) {
    const opciones = incluirPlaceholder
        ? ['<option value="">Seleccione un almacén...</option>']
        : [];

    almacenes.forEach((almacen) => {
        opciones.push(
            `<option value="${almacen.id}">ID ${almacen.id} — ${almacen.nombre}</option>`
        );
    });

    return opciones.join("");
}

function actualizarSelectsAlmacen(almacenes) {
    const consultaSelect = document.getElementById("sede-id");
    const registroSelect = document.getElementById("registro-almacen-id");
    const consultaActual = consultaSelect.value;
    const registroActual = registroSelect.value;

    consultaSelect.innerHTML = crearOpcionesAlmacen(almacenes, almacenes.length === 0);
    registroSelect.innerHTML = crearOpcionesAlmacen(almacenes);

    if (consultaActual) {
        consultaSelect.value = consultaActual;
    } else if (almacenes.length) {
        consultaSelect.value = String(almacenes[0].id);
    }

    if (registroActual) {
        registroSelect.value = registroActual;
    }
}

const QUERY_ALMACENES = `
    query Almacenes {
        almacenes {
            id
            nombre
            direccion
        }
    }
`;

const QUERY_INVENTARIO = `
    query InventarioPorSede($sedeId: Int!) {
        inventarioPorSede(sedeId: $sedeId) {
            almacen {
                id
                nombre
                direccion
            }
            items {
                cantidad
                producto {
                    id
                    nombre
                    categoria
                    precioUnitario
                }
            }
        }
    }
`;

const MUTATION_ALMACEN = `
    mutation RegistrarAlmacen($datos: RegistroAlmacenInput!) {
        registrarAlmacen(datos: $datos) {
            mensaje
            almacen {
                id
                nombre
                direccion
            }
        }
    }
`;

const MUTATION_REGISTRAR = `
    mutation RegistrarProducto($datos: RegistroInventarioInput!) {
        registrarProducto(datos: $datos) {
            mensaje
            cantidad
            producto {
                id
                nombre
            }
            almacen {
                id
                nombre
            }
        }
    }
`;

async function cargarAlmacenes() {
    const payload = await ejecutarGraphQL(QUERY_ALMACENES);

    if (payload.errors) {
        document.getElementById("sede-id").innerHTML =
            '<option value="">No se pudieron cargar los almacenes</option>';
        document.getElementById("registro-almacen-id").innerHTML =
            '<option value="">No se pudieron cargar los almacenes</option>';
        return [];
    }

    const almacenes = payload.data.almacenes;
    actualizarSelectsAlmacen(almacenes);
    return almacenes;
}

document.getElementById("form-consulta").addEventListener("submit", async (event) => {
    event.preventDefault();
    const sedeId = Number(document.getElementById("sede-id").value);
    const resultado = document.getElementById("resultado-consulta");

    if (!sedeId) {
        mostrarResultado(resultado, "Seleccione una sede de almacén.", "error");
        return;
    }

    mostrarResultado(resultado, "Consultando inventario...");

    try {
        const payload = await ejecutarGraphQL(QUERY_INVENTARIO, { sedeId });

        if (payload.errors) {
            mostrarResultado(resultado, formatearErrorGraphQL(payload), "error");
            return;
        }

        mostrarResultado(
            resultado,
            renderInventario(payload.data.inventarioPorSede),
            "success"
        );
    } catch (error) {
        mostrarResultado(resultado, error.message, "error");
    }
});

document.getElementById("form-almacen").addEventListener("submit", async (event) => {
    event.preventDefault();
    const resultado = document.getElementById("resultado-almacen");

    const datos = {
        almacenId: Number(document.getElementById("almacen-id").value),
        nombre: document.getElementById("almacen-nombre").value.trim(),
        direccion: document.getElementById("almacen-direccion").value.trim(),
    };

    mostrarResultado(resultado, "Guardando almacén...");

    try {
        const payload = await ejecutarGraphQL(MUTATION_ALMACEN, { datos });

        if (payload.errors) {
            mostrarResultado(resultado, formatearErrorGraphQL(payload), "error");
            return;
        }

        const data = payload.data.registrarAlmacen;
        mostrarResultado(
            resultado,
            `${data.mensaje}\n\nID: ${data.almacen.id}\nNombre: ${data.almacen.nombre}\nDirección: ${data.almacen.direccion}`,
            "success"
        );

        await cargarAlmacenes();
        document.getElementById("sede-id").value = String(data.almacen.id);
        document.getElementById("registro-almacen-id").value = String(data.almacen.id);
    } catch (error) {
        mostrarResultado(resultado, error.message, "error");
    }
});

document.getElementById("form-registro").addEventListener("submit", async (event) => {
    event.preventDefault();
    const resultado = document.getElementById("resultado-registro");
    const almacenId = Number(document.getElementById("registro-almacen-id").value);

    if (!almacenId) {
        mostrarResultado(
            resultado,
            "Seleccione un almacén. Si no existe, regístrelo primero en la sección anterior.",
            "error"
        );
        return;
    }

    const datos = {
        productoNombre: document.getElementById("producto-nombre").value.trim(),
        productoDescripcion: document.getElementById("producto-descripcion").value.trim() || null,
        productoPrecioUnitario: Number(document.getElementById("producto-precio").value),
        productoCategoria: document.getElementById("producto-categoria").value.trim(),
        almacenId,
        cantidadInicial: Number(document.getElementById("cantidad-inicial").value),
    };

    mostrarResultado(resultado, "Registrando producto...");

    try {
        const payload = await ejecutarGraphQL(MUTATION_REGISTRAR, { datos });

        if (payload.errors) {
            mostrarResultado(resultado, formatearErrorGraphQL(payload), "error");
            return;
        }

        const data = payload.data.registrarProducto;
        mostrarResultado(
            resultado,
            `${data.mensaje}\n\nProducto: ${data.producto.nombre} (ID ${data.producto.id})\nAlmacén: ${data.almacen.nombre} (ID ${data.almacen.id})\nCantidad: ${data.cantidad}`,
            "success"
        );
        event.target.reset();
        document.getElementById("registro-almacen-id").value = String(almacenId);
        document.getElementById("cantidad-inicial").value = "0";
    } catch (error) {
        mostrarResultado(resultado, error.message, "error");
    }
});

cargarAlmacenes();

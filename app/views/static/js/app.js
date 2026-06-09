const GRAPHQL_URL = "/graphql";

async function ejecutarGraphQL(query, variables = {}) {
    const response = await fetch(GRAPHQL_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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

document.getElementById("form-consulta").addEventListener("submit", async (event) => {
    event.preventDefault();
    const sedeId = Number(document.getElementById("sede-id").value);
    const resultado = document.getElementById("resultado-consulta");
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

document.getElementById("form-registro").addEventListener("submit", async (event) => {
    event.preventDefault();
    const resultado = document.getElementById("resultado-registro");

    const datos = {
        productoNombre: document.getElementById("producto-nombre").value.trim(),
        productoDescripcion: document.getElementById("producto-descripcion").value.trim() || null,
        productoPrecioUnitario: Number(document.getElementById("producto-precio").value),
        productoCategoria: document.getElementById("producto-categoria").value.trim(),
        almacenId: Number(document.getElementById("almacen-id").value),
        almacenNombre: document.getElementById("almacen-nombre").value.trim(),
        almacenDireccion: document.getElementById("almacen-direccion").value.trim(),
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
        document.getElementById("almacen-id").value = datos.almacenId;
    } catch (error) {
        mostrarResultado(resultado, error.message, "error");
    }
});

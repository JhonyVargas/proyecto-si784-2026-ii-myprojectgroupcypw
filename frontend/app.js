// Panel de pruebas de NotaryVerify.
// Consume directamente la API REST del backend (FastAPI) descrita en el FD03.
// No requiere build ni dependencias: HTML + CSS + JavaScript plano.

const $ = (selector) => document.querySelector(selector);

function apiBase() {
  return $("#api-base").value.replace(/\/$/, "");
}

function mostrarResultado(elemento, contenido, tipo = "info") {
  elemento.textContent = typeof contenido === "string" ? contenido : JSON.stringify(contenido, null, 2);
  elemento.classList.remove("resultado--ok", "resultado--error");
  if (tipo === "ok") elemento.classList.add("resultado--ok");
  if (tipo === "error") elemento.classList.add("resultado--error");
}

async function llamarApi(ruta, opciones = {}) {
  const respuesta = await fetch(`${apiBase()}${ruta}`, opciones);
  const contentType = respuesta.headers.get("content-type") || "";
  const cuerpo = contentType.includes("application/json") ? await respuesta.json() : await respuesta.text();
  if (!respuesta.ok) {
    const detalle = typeof cuerpo === "object" && cuerpo.detail ? cuerpo.detail : cuerpo;
    throw new Error(typeof detalle === "string" ? detalle : JSON.stringify(detalle));
  }
  return cuerpo;
}

async function comprobarApi() {
  const badge = $("#estado-api");
  try {
    await llamarApi("/");
    badge.textContent = "conectado";
    badge.className = "badge badge--ok";
  } catch (error) {
    badge.textContent = "sin conexión";
    badge.className = "badge badge--error";
  }
}

// ---------------------------------------------------------------------
// 1. Simulador de Identidad
// ---------------------------------------------------------------------

$("#form-consentimiento").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = Object.fromEntries(new FormData(evento.target));
  try {
    const resultado = await llamarApi("/identidades/consentimientos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_participante: datos.id_participante }),
    });
    mostrarResultado($("#resultado-identidad"), resultado, "ok");
  } catch (error) {
    mostrarResultado($("#resultado-identidad"), `Error: ${error.message}`, "error");
  }
});

$("#form-identidad").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const formData = new FormData(evento.target);
  // El backend espera un booleano explícito para confirmo_dato_ficticio.
  formData.set("confirmo_dato_ficticio", evento.target.confirmo_dato_ficticio.checked ? "true" : "false");
  try {
    const identidad = await llamarApi("/identidades", { method: "POST", body: formData });
    mostrarResultado($("#resultado-identidad"), identidad, "ok");
    $("#input-id-identidad").value = identidad.id;
  } catch (error) {
    mostrarResultado($("#resultado-identidad"), `Error: ${error.message}`, "error");
  }
});

// ---------------------------------------------------------------------
// 2. Credenciales QR/RFID
// ---------------------------------------------------------------------

$("#form-credencial").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = Object.fromEntries(new FormData(evento.target));
  try {
    const credencial = await llamarApi("/credenciales", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_identidad: datos.id_identidad, tipo: "QR" }),
    });
    mostrarResultado($("#resultado-credencial"), credencial, "ok");
    $("#input-id-credencial").value = credencial.id;
    $("#input-codigo-credencial").value = credencial.codigo;

    const imagenQr = $("#imagen-qr");
    imagenQr.src = `${apiBase()}/credenciales/${credencial.codigo}/qr`;
    imagenQr.hidden = false;
  } catch (error) {
    mostrarResultado($("#resultado-credencial"), `Error: ${error.message}`, "error");
  }
});

$("#form-revocar").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = Object.fromEntries(new FormData(evento.target));
  try {
    const credencial = await llamarApi(`/credenciales/${datos.id_credencial}/revocar`, {
      method: "POST",
    });
    mostrarResultado($("#resultado-credencial"), credencial, "ok");
  } catch (error) {
    mostrarResultado($("#resultado-credencial"), `Error: ${error.message}`, "error");
  }
});

// ---------------------------------------------------------------------
// 3. Verificación multicapa (CU-03)
// ---------------------------------------------------------------------

let idSesionActual = null;

$("#form-iniciar-sesion").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = Object.fromEntries(new FormData(evento.target));
  try {
    const sesion = await llamarApi("/verificaciones", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ codigo_credencial: datos.codigo_credencial }),
    });
    idSesionActual = sesion.id;
    $("#texto-id-sesion").textContent = sesion.id;
    $("#panel-sesion").hidden = sesion.estado !== "EN_CURSO";
    mostrarResultado($("#resultado-verificacion"), sesion, sesion.resultado === "IDENTIDAD_VERIFICADA" ? "ok" : "info");
  } catch (error) {
    mostrarResultado($("#resultado-verificacion"), `Error: ${error.message}`, "error");
  }
});

$("#boton-rostro").addEventListener("click", async () => {
  const archivo = $("#input-rostro").files[0];
  if (!archivo || !idSesionActual) return;
  const formData = new FormData();
  formData.append("imagen", archivo);
  try {
    const sesion = await llamarApi(`/verificaciones/${idSesionActual}/rostro`, {
      method: "POST",
      body: formData,
    });
    mostrarResultado($("#resultado-verificacion"), sesion, sesion.resultado ? "error" : "info");
  } catch (error) {
    mostrarResultado($("#resultado-verificacion"), `Error: ${error.message}`, "error");
  }
});

$("#boton-prueba-vida").addEventListener("click", async () => {
  const archivo = $("#input-prueba-vida").files[0];
  if (!archivo || !idSesionActual) return;
  const accion = $("#select-accion").value;
  const formData = new FormData();
  formData.append("imagen", archivo);
  try {
    const sesion = await llamarApi(
      `/verificaciones/${idSesionActual}/prueba-vida?accion=${encodeURIComponent(accion)}`,
      { method: "POST", body: formData }
    );
    mostrarResultado(
      $("#resultado-verificacion"),
      sesion,
      sesion.resultado === "IDENTIDAD_VERIFICADA" ? "ok" : "error"
    );
  } catch (error) {
    mostrarResultado($("#resultado-verificacion"), `Error: ${error.message}`, "error");
  }
});

$("#form-tramite").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  if (!idSesionActual) {
    mostrarResultado($("#resultado-tramite"), "Primero ejecute una verificación.", "error");
    return;
  }
  const escenario = $("#select-escenario").value;
  try {
    const tramite = await llamarApi(
      `/tramites?id_sesion=${idSesionActual}&escenario=${escenario}`,
      { method: "POST" }
    );
    mostrarResultado($("#resultado-tramite"), tramite, "ok");
  } catch (error) {
    mostrarResultado($("#resultado-tramite"), `Error: ${error.message}`, "error");
  }
});

// ---------------------------------------------------------------------
// 4. Bitácora de auditoría
// ---------------------------------------------------------------------

$("#boton-verificar-cadena").addEventListener("click", async () => {
  try {
    const resultado = await llamarApi("/auditoria/verificar-cadena");
    mostrarResultado($("#resultado-cadena"), resultado, resultado.valida ? "ok" : "error");
  } catch (error) {
    mostrarResultado($("#resultado-cadena"), `Error: ${error.message}`, "error");
  }
});

$("#boton-listar-eventos").addEventListener("click", async () => {
  try {
    const eventos = await llamarApi("/auditoria/eventos");
    const tabla = $("#tabla-eventos");
    const cuerpo = tabla.querySelector("tbody");
    cuerpo.innerHTML = "";
    eventos.forEach((evento) => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${evento.secuencia}</td>
        <td>${evento.id_sesion ?? "—"}</td>
        <td>${evento.tipo_evento}</td>
        <td>${evento.hash_evento_anterior.slice(0, 12)}…</td>
        <td>${evento.hash_evento_actual.slice(0, 12)}…</td>
        <td>${new Date(evento.timestamp).toLocaleString()}</td>
      `;
      cuerpo.appendChild(fila);
    });
    tabla.hidden = eventos.length === 0;
  } catch (error) {
    mostrarResultado($("#resultado-cadena"), `Error: ${error.message}`, "error");
  }
});

comprobarApi();

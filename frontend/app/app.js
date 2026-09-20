/* ═══════════════════════════════════════════════════════════════════
 * NotaryVerify — Estación de Verificación
 *
 * Interfaz de operador con captura biométrica en vivo. Consume la misma API
 * que el panel de pruebas (../index.html), pero presenta el flujo como una
 * secuencia de pantallas y toma las imágenes del vídeo en lugar de pedir
 * archivos al usuario.
 * ═══════════════════════════════════════════════════════════════════ */

const API = "http://127.0.0.1:8000";

const $ = (sel) => document.querySelector(sel);

/* Estado de la sesión en curso. */
const sesion = { id: null, codigo: null, accion: null };

/* Las etiquetas de giro se refieren a la izquierda/derecha DE LA PERSONA.
 * El backend mide el desplazamiento horizontal de la nariz respecto al centro
 * del rostro, por lo que la imagen enviada no debe ir espejada. */
const ACCIONES = {
  PARPADEO: {
    titulo: "Cierre los ojos",
    orden: "Cierre los ojos",
    detalle: "Manténgalos cerrados hasta que desaparezca el contador.",
  },
  GIRO_IZQUIERDA: {
    titulo: "Gire la cabeza a su izquierda",
    orden: "Gire a su izquierda",
    detalle: "Mantenga el giro hasta que desaparezca el contador.",
  },
  GIRO_DERECHA: {
    titulo: "Gire la cabeza a su derecha",
    orden: "Gire a su derecha",
    detalle: "Mantenga el giro hasta que desaparezca el contador.",
  },
};

const RESULTADOS = {
  IDENTIDAD_VERIFICADA: {
    clase: "veredicto--ok", glifo: "✓", titulo: "Identidad verificada",
    motivo: "El compareciente superó los tres controles configurados.",
  },
  VERIFICACION_RECHAZADA: {
    clase: "veredicto--mal", glifo: "✕", titulo: "Verificación rechazada",
    motivo: "No se cumplieron las condiciones exigidas por el motor de reglas.",
  },
  ROSTRO_NO_COINCIDENTE: {
    clase: "veredicto--mal", glifo: "✕", titulo: "Rostro no coincidente",
    motivo: "El rostro capturado no corresponde a la referencia registrada para esta credencial.",
  },
  PRUEBA_DE_VIDA_FALLIDA: {
    clase: "veredicto--mal", glifo: "✕", titulo: "Prueba de vida fallida",
    motivo: "No se detectó la acción solicitada. Podría tratarse de una fotografía o de una reproducción en pantalla.",
  },
  CREDENCIAL_NO_REGISTRADA: {
    clase: "veredicto--mal", glifo: "✕", titulo: "Credencial no registrada",
    motivo: "El código presentado no corresponde a ninguna credencial emitida.",
  },
  CREDENCIAL_REVOCADA: {
    clase: "veredicto--mal", glifo: "✕", titulo: "Credencial revocada",
    motivo: "La credencial fue revocada y no habilita ninguna verificación.",
  },
  MULTIPLES_INTENTOS_FALLIDOS: {
    clase: "veredicto--mal", glifo: "!", titulo: "Múltiples intentos fallidos",
    motivo: "La identidad quedó bloqueada tras acumular rechazos consecutivos.",
  },
  VERIFICACION_REQUIERE_REVISION: {
    clase: "veredicto--revision", glifo: "?", titulo: "Requiere revisión",
    motivo: "El resultado no es concluyente. Debe revisarlo un administrador.",
  },
};

/* ═════════════════ Utilidades de interfaz ═════════════════ */

function irA(idPantalla, numeroPaso) {
  document.querySelectorAll(".pantalla").forEach((p) =>
    p.classList.toggle("pantalla--activa", p.id === idPantalla));

  document.querySelectorAll(".paso").forEach((p) => {
    const n = Number(p.dataset.paso);
    p.classList.toggle("paso--activo", n === numeroPaso);
    p.classList.toggle("paso--hecho", n < numeroPaso);
  });
}

function mostrarError(selector, mensaje) {
  const el = $(selector);
  el.textContent = mensaje;
  el.hidden = !mensaje;
}

function limpiarErrores() {
  ["#error-credencial", "#error-rostro", "#error-vida"].forEach((s) => mostrarError(s, ""));
}

function ocupado(selectorBoton, activo) {
  const boton = $(selectorBoton);
  boton.classList.toggle("boton--cargando", activo);
  boton.disabled = activo;
}

/* ═════════════════ Cliente de la API ═════════════════ */

async function pedir(ruta, opciones = {}) {
  let respuesta;
  try {
    respuesta = await fetch(API + ruta, opciones);
  } catch {
    throw new Error("No se pudo contactar con la API. Verifique que el backend esté en ejecución.");
  }

  const cuerpo = await respuesta.json().catch(() => null);

  if (!respuesta.ok) {
    const detalle = cuerpo?.detail;
    if (typeof detalle === "string") throw new Error(detalle);
    if (Array.isArray(detalle)) throw new Error(detalle.map((d) => d.msg).join(" · "));
    throw new Error(`La API respondió con el código ${respuesta.status}.`);
  }
  return cuerpo;
}

async function comprobarApi() {
  const caja = $("#conexion");
  try {
    const estado = await pedir("/");
    caja.className = "conexion conexion--ok";
    $("#texto-api").textContent = estado.estado === "operativo" ? "API conectada" : estado.estado;
  } catch {
    caja.className = "conexion conexion--mal";
    $("#texto-api").textContent = "API no disponible";
  }
}

/* ═════════════════ Cámara ═════════════════ */

let flujoCamara = null;

async function abrirCamara(idVideo, idCaido, idMotivo) {
  const video = $(idVideo);

  if (!navigator.mediaDevices?.getUserMedia) {
    caerCamara(idCaido, idMotivo,
      "Este navegador no permite el acceso a la cámara. Use Chrome, Edge o Firefox actualizados.");
    return false;
  }

  try {
    if (!flujoCamara || !flujoCamara.active) {
      flujoCamara = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      });
    }
    video.srcObject = flujoCamara;
    $(idCaido).hidden = true;
    await video.play().catch(() => {});
    return true;
  } catch (error) {
    const motivos = {
      NotAllowedError: "Se denegó el permiso de cámara. Autorícelo desde el icono de la barra de direcciones y recargue la página.",
      NotFoundError: "No se detectó ninguna cámara conectada al equipo.",
      NotReadableError: "La cámara está siendo utilizada por otra aplicación.",
      SecurityError: "El navegador bloquea la cámara en este origen. Debe servirse desde localhost o mediante HTTPS.",
    };
    caerCamara(idCaido, idMotivo, motivos[error.name] || `No se pudo abrir la cámara (${error.name}).`);
    return false;
  }
}

function caerCamara(idCaido, idMotivo, mensaje) {
  $(idCaido).hidden = false;
  $(idMotivo).textContent = mensaje;
}

function cerrarCamara() {
  if (!flujoCamara) return;
  flujoCamara.getTracks().forEach((t) => t.stop());
  flujoCamara = null;
}

/* Captura el fotograma actual SIN espejar: la vista previa está invertida solo
 * por CSS, para que resulte natural al operador. */
function capturarFotograma(idVideo) {
  const video = $(idVideo);
  if (!video.videoWidth) {
    throw new Error("La cámara aún no entrega imagen. Espere un instante e inténtelo de nuevo.");
  }
  const lienzo = $("#lienzo");
  lienzo.width = video.videoWidth;
  lienzo.height = video.videoHeight;
  lienzo.getContext("2d").drawImage(video, 0, 0);

  return new Promise((resolver, rechazar) => {
    lienzo.toBlob(
      (blob) => (blob ? resolver(blob) : rechazar(new Error("No se pudo procesar la imagen capturada."))),
      "image/jpeg",
      0.92,
    );
  });
}

function comoFormulario(blob, nombre) {
  const datos = new FormData();
  datos.append("imagen", blob, nombre);
  return datos;
}

/* ═════════════════ Paso 1 · Credencial ═════════════════ */

$("#boton-iniciar").addEventListener("click", iniciarVerificacion);
$("#entrada-codigo").addEventListener("keydown", (e) => {
  if (e.key === "Enter") iniciarVerificacion();
});

async function iniciarVerificacion() {
  const codigo = $("#entrada-codigo").value.trim().toUpperCase();
  limpiarErrores();

  if (!codigo) {
    mostrarError("#error-credencial", "Introduzca el código de la credencial.");
    return;
  }

  ocupado("#boton-iniciar", true);

  try {
    const nueva = await pedir("/verificaciones", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ codigo_credencial: codigo }),
    });

    sesion.id = nueva.id;
    sesion.codigo = codigo;
    sesion.accion = null;

    /* Una credencial no registrada o revocada cierra la sesión de inmediato:
     * el backend ya emitió el veredicto, así que se salta al resultado sin
     * llegar a abrir la cámara. */
    if (nueva.estado === "COMPLETADA") {
      pintarResultado(nueva);
      return;
    }

    irA("pantalla-rostro", 2);
    await abrirCamara("#video-rostro", "#sin-camara-rostro", "#motivo-camara-rostro");
  } catch (error) {
    mostrarError("#error-credencial", error.message);
  } finally {
    ocupado("#boton-iniciar", false);
  }
}

/* ═════════════════ Paso 2 · Rostro ═════════════════ */

$("#boton-capturar-rostro").addEventListener("click", async () => {
  limpiarErrores();
  try {
    const blob = await capturarFotograma("#video-rostro");
    await enviarRostro(blob);
  } catch (error) {
    mostrarError("#error-rostro", error.message);
  }
});

$("#archivo-rostro").addEventListener("change", async (e) => {
  const archivo = e.target.files[0];
  if (!archivo) return;
  limpiarErrores();
  try {
    await enviarRostro(archivo);
  } catch (error) {
    mostrarError("#error-rostro", error.message);
  }
});

async function enviarRostro(blob) {
  ocupado("#boton-capturar-rostro", true);
  try {
    const estado = await pedir(`/verificaciones/${sesion.id}/rostro`, {
      method: "POST",
      body: comoFormulario(blob, "rostro.jpg"),
    });

    /* Si el rostro no coincide, el backend cierra la sesión sin llegar a la
     * prueba de vida. */
    if (estado.estado === "COMPLETADA") {
      pintarResultado(estado);
      return;
    }

    sortearAccion();
    irA("pantalla-vida", 3);
    await abrirCamara("#video-vida", "#sin-camara-vida", "#motivo-camara-vida");
  } finally {
    ocupado("#boton-capturar-rostro", false);
  }
}

/* ═════════════════ Paso 3 · Prueba de vida ═════════════════ */

function sortearAccion() {
  const claves = Object.keys(ACCIONES);
  let nueva;
  do {
    nueva = claves[Math.floor(Math.random() * claves.length)];
  } while (claves.length > 1 && nueva === sesion.accion);

  sesion.accion = nueva;
  $("#texto-accion").textContent = ACCIONES[nueva].titulo;
  $("#detalle-accion").textContent = ACCIONES[nueva].detalle;
}

$("#boton-otra-accion").addEventListener("click", sortearAccion);

$("#boton-ejecutar-vida").addEventListener("click", async () => {
  limpiarErrores();
  ocupado("#boton-ejecutar-vida", true);

  try {
    await cuentaAtras();
    const blob = await capturarFotograma("#video-vida");
    ocultarCuenta();
    await enviarPruebaVida(blob);
  } catch (error) {
    ocultarCuenta();
    mostrarError("#error-vida", error.message);
  } finally {
    ocupado("#boton-ejecutar-vida", false);
  }
});

$("#archivo-vida").addEventListener("change", async (e) => {
  const archivo = e.target.files[0];
  if (!archivo) return;
  limpiarErrores();
  try {
    await enviarPruebaVida(archivo);
  } catch (error) {
    mostrarError("#error-vida", error.message);
  }
});

/* Perímetro del anillo: 2·π·r con r = 52 (ver estilos.css). */
const PERIMETRO = 2 * Math.PI * 52;

function cuentaAtras() {
  return new Promise((resolver) => {
    const caja = $("#cuenta");
    const avance = $("#cuenta-avance");
    const cifra = $("#cuenta-cifra");
    const orden = $("#cuenta-orden");

    const TOTAL = 3;
    let restante = TOTAL;

    caja.hidden = false;
    orden.hidden = true;
    cifra.hidden = false;
    avance.style.transition = "none";
    avance.style.strokeDashoffset = "0";
    cifra.textContent = restante;

    /* Fuerza un reflujo para que la transición del anillo arranque desde el
     * valor recién fijado y no se pierda el primer tramo. */
    void avance.getBoundingClientRect();
    avance.style.transition = "stroke-dashoffset 1s linear";

    const paso = () => {
      restante -= 1;
      avance.style.strokeDashoffset = String((PERIMETRO * (TOTAL - restante)) / TOTAL);

      if (restante > 0) {
        cifra.textContent = restante;
        cifra.style.animation = "none";
        void cifra.getBoundingClientRect();
        cifra.style.animation = "";
        return;
      }

      clearInterval(reloj);
      /* Al llegar a cero se muestra la orden en palabras y se concede un
       * margen para que la persona complete la acción antes del disparo. */
      cifra.hidden = true;
      orden.hidden = false;
      orden.textContent = ACCIONES[sesion.accion].orden;
      setTimeout(resolver, 900);
    };

    const reloj = setInterval(paso, 1000);
  });
}

function ocultarCuenta() {
  const caja = $("#cuenta");
  caja.hidden = true;
  $("#cuenta-orden").hidden = true;
  $("#cuenta-cifra").hidden = false;
}

async function enviarPruebaVida(blob) {
  const estado = await pedir(
    `/verificaciones/${sesion.id}/prueba-vida?accion=${encodeURIComponent(sesion.accion)}`,
    { method: "POST", body: comoFormulario(blob, "prueba-vida.jpg") },
  );
  pintarResultado(estado);
}

/* ═════════════════ Paso 4 · Resultado ═════════════════ */

function pintarResultado(estado) {
  cerrarCamara();

  const info = RESULTADOS[estado.resultado] || {
    clase: "veredicto--revision", glifo: "?",
    titulo: estado.resultado || "Sin resultado",
    motivo: "El sistema no devolvió un resultado reconocido.",
  };

  const panel = $("#veredicto");
  panel.className = `panel panel--veredicto ${info.clase}`;
  $("#sello-glifo").textContent = info.glifo;
  $("#veredicto-titulo").textContent = info.titulo;
  $("#veredicto-motivo").textContent = info.motivo;

  pintarFactores(estado);
  pintarDetalle(estado);
  irA("pantalla-resultado", 4);
}

function pintarFactores(estado) {
  const credencialOk = !["CREDENCIAL_NO_REGISTRADA", "CREDENCIAL_REVOCADA"].includes(estado.resultado);

  const filas = [
    {
      etiqueta: "Credencial",
      estado: credencialOk ? "ok" : "mal",
      valor: credencialOk ? "válida" : "no válida",
    },
    {
      etiqueta: "Reconocimiento facial",
      estado: estado.rostro_coincide === true ? "ok" : estado.rostro_coincide === false ? "mal" : "nd",
      valor: estado.confianza_facial != null
        ? `confianza ${Number(estado.confianza_facial).toFixed(2)}`
        : "no evaluado",
    },
    {
      etiqueta: "Prueba de vida",
      estado: estado.prueba_vida_superada === true ? "ok" : estado.prueba_vida_superada === false ? "mal" : "nd",
      valor: estado.prueba_vida_superada == null
        ? "no evaluada"
        : (ACCIONES[sesion.accion]?.orden.toLowerCase() || sesion.accion || "—"),
    },
  ];

  const glifos = { ok: "✓", mal: "✕", nd: "–" };

  $("#factores").innerHTML = filas.map((f) => `
    <li data-estado="${f.estado}" data-icono="${glifos[f.estado]}">
      ${f.etiqueta}<span>${f.valor}</span>
    </li>`).join("");
}

function pintarDetalle(estado) {
  const campos = [
    ["Sesión", estado.id],
    ["Credencial", sesion.codigo || "—"],
    ["Estado", estado.estado],
    ["Resultado", estado.resultado || "—"],
    ["Inicio", formatearFecha(estado.fecha_inicio)],
    ["Fin", formatearFecha(estado.fecha_fin)],
  ];
  $("#detalle-lista").innerHTML = campos
    .map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`)
    .join("");
}

function formatearFecha(iso) {
  if (!iso) return "—";
  const f = new Date(iso);
  return Number.isNaN(f.getTime()) ? iso : f.toLocaleString("es-PE");
}

/* ═════════════════ Reinicio ═════════════════ */

$("#boton-nueva").addEventListener("click", reiniciar);
document.querySelectorAll("[data-volver]").forEach((b) => b.addEventListener("click", reiniciar));

function reiniciar() {
  cerrarCamara();
  ocultarCuenta();
  limpiarErrores();
  sesion.id = null;
  sesion.codigo = null;
  sesion.accion = null;
  $("#entrada-codigo").value = "";
  irA("pantalla-credencial", 1);
  $("#entrada-codigo").focus();
}

window.addEventListener("beforeunload", cerrarCamara);

/* ═════════════════ Arranque ═════════════════ */

irA("pantalla-credencial", 1);
comprobarApi();
setInterval(comprobarApi, 15000);

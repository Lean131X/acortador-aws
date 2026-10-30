// ip elastica de la EC2 donde corre la API
const API_URL = "http://52.206.183.98:8000";

const formulario = document.getElementById("formulario");
const inputUrl = document.getElementById("url");
const textoError = document.getElementById("error");
const resultado = document.getElementById("resultado");
const enlaceCorto = document.getElementById("enlaceCorto");
const btnCopiar = document.getElementById("btnCopiar");
const mensajeCopiado = document.getElementById("mensajeCopiado");

function urlValida(texto) {
  try {
    const url = new URL(texto);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch (e) {
    return false;
  }
}

formulario.addEventListener("submit", async function (e) {
  e.preventDefault();
  textoError.textContent = "";
  mensajeCopiado.textContent = "";
  resultado.classList.add("oculto");

  const url = inputUrl.value.trim();

  if (!urlValida(url)) {
    textoError.textContent = "La URL no es válida, tiene que empezar con http:// o https://";
    return;
  }

  try {
    const respuesta = await fetch(API_URL + "/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ original_url: url })
    });

    if (!respuesta.ok) {
      textoError.textContent = "El servidor no aceptó la URL (error " + respuesta.status + ")";
      return;
    }

    const datos = await respuesta.json();
    enlaceCorto.value = datos.short_url;
    resultado.classList.remove("oculto");
  } catch (error) {
    // si la EC2 esta apagada o no responde cae aqui
    textoError.textContent = "No se pudo conectar con el servidor, intenta más tarde";
  }
});

// navigator.clipboard no funciona en http, por eso uso execCommand
btnCopiar.addEventListener("click", function () {
  enlaceCorto.select();
  document.execCommand("copy");
  mensajeCopiado.textContent = "¡Copiado!";
});
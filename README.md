# EzEat — Explora tu restaurante

Landing 3D interactiva construida con Three.js. Restaurante isométrico con 5 zonas
(Comedor, Cocina, Inventario, Oficina, Delivery), personajes 3D reales animados,
coreografía automática "restaurante vivo", y un tour cinemático guiado.

## Archivo principal

- `index.html` — página completa, autocontenida (HTML + CSS + JS + modelos 3D
  embebidos en base64). Ábrelo directo en cualquier navegador, no necesita build
  ni servidor.

## Cómo previsualizar localmente

Simplemente abre `index.html` en tu navegador. Si prefieres un servidor local
(recomendado para evitar restricciones de algunos navegadores con archivos locales):

```bash
python3 -m http.server 8000
# luego abre http://localhost:8000
```

## Hospedar gratis con GitHub Pages

1. Ve a **Settings → Pages** en este repositorio en GitHub.
2. En "Source", selecciona la rama `main` y la carpeta `/ (root)`.
3. Guarda. En un par de minutos tu página estará en algo como
   `https://tu-usuario.github.io/nombre-del-repo/`.

## Historial

Cada cambio importante a la página se sube como un commit aparte con un mensaje
descriptivo, para poder regresar a cualquier versión anterior si algo se rompe.

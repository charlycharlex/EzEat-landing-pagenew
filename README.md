# EzEat — Explora tu restaurante

Experiencia 3D interactiva: un restaurante isométrico con cinco zonas (Comedor, Cocina,
Inventario, Oficina y Delivery) que el visitante recorre para entender qué hace EzEat en
cada parte de la operación.

Pensada para integrarse al sitio actual (ezeat.com.mx) como la parte interactiva. **No
sustituye a la landing**: el contenido de venta y el posicionamiento en buscadores siguen
viviendo en el sitio principal.

---

## Qué es, en términos prácticos

- **Un solo archivo**: [`index.html`](index.html) (~780 KB). HTML, CSS, JavaScript, modelos
  3D y texturas, todo dentro.
- **Sin compilación**: no hay npm, ni bundler, ni framework. Se abre y funciona.
- **Sin backend**: no guarda ni envía datos. El único enlace externo es el formulario de
  contacto.

Para probarla: abrir `index.html` en el navegador, o servirla con cualquier servidor
estático.

---

## Dependencias externas (CDN)

| Qué | De dónde |
|---|---|
| three.js r128 y GSAP 3.12 | `cdnjs.cloudflare.com` |
| Cargadores y post-proceso de three.js | `cdn.jsdelivr.net` |
| Decodificador Draco (`.wasm`) | `cdn.jsdelivr.net` |

**Si el sitio tiene Content-Security-Policy**, hay que permitir esos dos dominios en
`script-src`, y `cdn.jsdelivr.net` también en `connect-src` (el decodificador de Draco se
baja por fetch). La alternativa es auto-hospedar esos archivos y cambiar las rutas de los
`<script>` (líneas 268-279).

Si algo de eso no carga, la página **no se queda colgada**: muestra un mensaje pidiendo
recargar. Lo mismo si el navegador no soporta WebGL o si pierde el contexto 3D.

---

## Cómo integrarla

**Opción A — ruta propia (recomendada).** Publicarla en algo como `ezeat.com.mx/explora` y
mandar ahí desde el sitio. Conserva la experiencia a pantalla completa y los 780 KB los
descarga solo quien decide entrar.

**Opción B — dentro de una página, en un `<iframe>`.** Funciona: la escena ocupa el 100%
del iframe. La desventaja es que el peso lo cargan todos los visitantes de esa página.

**Lo que no está listo:** meterla como una sección más de una página con scroll. La página
usa `position:fixed` y `overflow:hidden` en `html, body`, así que requeriría ajustes.

**Pendiente en las dos opciones:** no hay enlace de regreso al sitio. Hoy el logo solo
reinicia la vista de la cámara (`#brandReset`).

---

## Qué se toca para configurar

| Qué | Dónde |
|---|---|
| Destino de "Agendar demo" | `CONTACT_URL`, línea ~2142. El panel le agrega `?interes=<zona>` |
| El mismo botón del encabezado | línea ~227 |
| Todos los textos, viñetas y alertas de IA | objeto `ZONES`, línea ~299 |
| Posición de cámara de cada zona | `camPos` y `camTarget` dentro de `ZONES` |
| Recursos 3D en base64 | `ASSETS_B64` (línea ~1633) y `MASCOT_B64` (línea ~642) |

El JavaScript está dividido en secciones numeradas con comentarios (1 zonas, 2 escena,
3 helpers, 4 construcción de cada zona, 5 cámara, 6 clics, 7 panel, 8 menú, 9 hero,
10 alertas, 11 flujo de datos, 11.5 coreografía automática, 11.6 recorrido guiado,
12 loop de dibujo, 13 arranque).

---

## Recursos 3D

Todos van incrustados en base64 para que el archivo sea autónomo.

- **Remy**: modelado en Blender. Fuente en [`fuentes/Remy_animable.blend`](fuentes/).
  Exportado a glTF con compresión Draco: 851 KB sin comprimir contra 94 KB con.
- **Isla de cocina y personajes**: recursos de Kenney (licencia CC0).
- **Texturas**: JPEG cuando no usan transparencia, PNG cuando sí. El cargador reconoce
  cuál es por la firma del archivo.

Para regenerar los modelos después de editarlos en Blender, hay dos scripts en
[`fuentes/`](fuentes/) que se corren desde la terminal, sin abrir la ventana de Blender.
El README de esa carpeta trae los comandos.

**Advertencia para quien toque esto:** comprimir los modelos de los *personajes* con Draco
los deja invisibles (el esqueleto sobrevive, la malla no, al clonarlos con `SkeletonUtils`).
Están sin comprimir a propósito; solo ahorraban ~100 KB.

---

## Rendimiento

- En pantallas de 720px o menos: resolución de dibujo a 1.5x y mapa de sombras a la mitad.
- El brillo (bloom) y el suavizado de bordes solo se activan si cargan los scripts de
  post-proceso; si no, dibuja sin ellos.
- Respeta `prefers-reduced-motion`: con esa opción activada, las animaciones se acortan.

---

## Pendientes conocidos

Ninguno rompe la página, pero conviene tenerlos en el radar:

1. **No mide nada.** No hay Google Analytics ni equivalente. Los puntos naturales para
   instrumentar son `focusZone()` (qué zona abren), `playShowcaseTour()` (recorrido) y el
   clic en `#pDemo` (la conversión).
2. **No hay enlaces directos a una zona.** Algo como `?zona=cocina` le serviría a ventas
   para mandar el módulo exacto que le interesa a cada prospecto.
3. **Accesibilidad.** Los botones flotantes ("Ver flujo de datos" y "Ver cómo se conecta
   todo") son `div`, no `button`, y no hay navegación por teclado.
4. **Sin contenido para buscadores.** Es una decisión consciente: el SEO lo cubre el sitio
   principal. Si algún día se publica sola, necesitaría contenido en HTML.
5. **El personaje "Remy"** está claramente inspirado en el de *Ratatouille* (Disney/Pixar).
   En una página comercial eso es un riesgo de propiedad intelectual. Vale la pena darle
   identidad propia, o revisarlo con quien lleve el tema legal, antes de publicar.

---

## Historial

Cada cambio importante va en un commit aparte con su mensaje, para poder regresar a
cualquier versión anterior. `git log --oneline` da el recorrido completo.

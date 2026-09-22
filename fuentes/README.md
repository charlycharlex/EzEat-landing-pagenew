# Fuentes 3D

Archivos originales y scripts para regenerar los modelos que van incrustados en
`index.html`. Solo hacen falta si se va a **editar** un modelo; para trabajar en la página
no se necesitan.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `Remy_animable.blend` | Remy modelado y con esqueleto (31 huesos) más su animación idle |
| `exportar_glb.py` | Exporta un `.blend` a `.glb` comprimido, listo para la web |
| `recomprimir_glb.py` | Comprime un `.glb` que ya existe, sin pasar por el `.blend` |

## Cómo se usan

Los dos scripts corren Blender desde la terminal, sin abrir la ventana. Requiere Blender
instalado (se probó con 5.2).

**Exportar Remy después de editarlo:**

```bash
blender -b fuentes/Remy_animable.blend --python fuentes/exportar_glb.py -- salida.glb 0 0.4 1 2 0.12
```

Los números, en orden: nivel de subdivisión (0), cuánto reducir la malla (0.4 = se queda
con el 40%), si incluye animación (1 = sí), cada cuántos cuadros la muestrea (2) y cuánto
reducir la cuchara (0.12, que es aparte porque venía con mucho más detalle del necesario).

Para que aplique la compresión Draco hay que poner la variable de entorno `DRACO=1`.

**Comprimir un modelo que ya está en `.glb`:**

```bash
blender -b --python fuentes/recomprimir_glb.py -- entrada.glb salida.glb 7 12
```

El 7 es el nivel de compresión y el 12 la precisión de las posiciones. Este es el que se
usó con la isla de la cocina: la bajó de 447 KB a 119 KB.

## Cómo se mete el resultado a la página

El `.glb` se convierte a base64 y se reemplaza la línea correspondiente dentro del objeto
`ASSETS_B64` de `index.html`. En Windows:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("salida.glb")) | Set-Clipboard
```

## Cuidado con los personajes

Los modelos de los personajes (`character`, `idle`, `run`) **no deben comprimirse con
Draco**. Se probó: el esqueleto sobrevive pero la malla se rompe al clonarla con
`SkeletonUtils`, y los personajes salen invisibles. Solo ahorraba unos 100 KB.

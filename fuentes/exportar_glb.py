import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
out_path = argv[0]
subsurf_level = int(argv[1]) if len(argv) > 1 else 0
decimate_ratio = float(argv[2]) if len(argv) > 2 else 1.0
with_anim = bool(int(argv[3])) if len(argv) > 3 else True
frame_step = int(argv[4]) if len(argv) > 4 else 1
spoon_ratio = float(argv[5]) if len(argv) > 5 else decimate_ratio

# fuera todo lo que no es el personaje: cámara, luces, pedestal y fondo
for o in list(bpy.data.objects):
    if o.type in {'CAMERA', 'LIGHT'} or o.name.startswith('Pedestal') or o.name == 'Plano':
        bpy.data.objects.remove(o, do_unlink=True)

polys = 0
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    polys += len(o.data.polygons)
    for m in list(o.modifiers):
        if m.type == 'SUBSURF':
            m.levels = subsurf_level
            m.render_levels = subsurf_level
    ratio = spoon_ratio if 'Cuchara' in o.name else decimate_ratio
    if ratio < 1.0 and len(o.data.polygons) > 300:
        d = o.modifiers.new("reducir", 'DECIMATE')
        d.ratio = ratio

kwargs = dict(
    filepath=out_path,
    export_format='GLB',
    use_selection=False,
    export_apply=True,
    export_animations=with_anim,
    export_skins=True,
    export_yup=True,
    export_frame_step=frame_step,
)
if os.environ.get('DRACO') == '1':
    kwargs.update(
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=7,
        export_draco_position_quantization=12,
        export_draco_normal_quantization=8,
        export_draco_generic_quantization=10,
    )
for extra in ('export_optimize_animation_size', 'export_optimize_animation_keep_anim_armature'):
    kwargs[extra] = True if extra.endswith('size') else False
while True:
    try:
        bpy.ops.export_scene.gltf(**kwargs)
        break
    except TypeError as e:
        bad = str(e).split("'")[1] if "'" in str(e) else None
        if bad and bad in kwargs:
            print("opción no soportada, se omite:", bad)
            kwargs.pop(bad)
            continue
        raise

size = os.path.getsize(out_path)
print("EXPORTOK polys_base=%d archivo=%d bytes (%.0f KB)" % (polys, size, size / 1024))

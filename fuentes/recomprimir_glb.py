import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
src, dst = argv[0], argv[1]
level = int(argv[2]) if len(argv) > 2 else 7
pos_bits = int(argv[3]) if len(argv) > 3 else 12

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)

mats_in = sorted({m.name for m in bpy.data.materials})
polys = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
bones = sum(len(o.data.bones) for o in bpy.data.objects if o.type == 'ARMATURE')
acciones = [a.name for a in bpy.data.actions]

kwargs = dict(
    filepath=dst,
    export_format='GLB',
    use_selection=False,
    export_apply=False,
    export_animations=bool(acciones),
    export_skins=True,
    export_yup=True,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=level,
    export_draco_position_quantization=pos_bits,
    export_draco_normal_quantization=8,
    export_draco_texcoord_quantization=10,
    export_draco_generic_quantization=10,
)
while True:
    try:
        bpy.ops.export_scene.gltf(**kwargs)
        break
    except TypeError as e:
        bad = str(e).split("'")[1] if "'" in str(e) else None
        if bad and bad in kwargs:
            print("opción omitida:", bad)
            kwargs.pop(bad)
            continue
        raise

antes, despues = os.path.getsize(src), os.path.getsize(dst)
print("RECOMP %s: %.0f KB -> %.0f KB | polys=%d huesos=%d acciones=%s materiales=%s" % (
    os.path.basename(src), antes/1024, despues/1024, polys, bones, acciones, mats_in))

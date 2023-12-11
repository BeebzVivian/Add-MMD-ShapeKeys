import logging
from typing import Dict

import bpy

from . import copy_as_mmd_settings
from .copy_as_mmd_settings import CopyAsMMDSettings

log = logging.getLogger(__name__)

# Keep all lowercase
VISEMES = {
    "ah": "あ",
    "ch": "い",
    "u": "う",
    "e": "え",
    "oh": "お",
}

MMD_SHAPEKEYS = {
    "blink": "まばたき",
    "blink 2": "笑い",
    "wink": "ウィンク",
    "wink right": "ウィンク右",
    "wink 2": "ウィンク２",
    "wink 2 right": "ｳｨﾝｸ２右",
    "kiri-eye": "ｷﾘｯ",
    "> <": "はぅ",
    "o o":"はちゅ目",
    "howawa": "なごみ",
    "ha!!!": "びっくり",
    "jitoeye": "じと目",
    "bottomlid up": "下まぶた上げ",
    "anger eye": "恐ろしい",
    "eyestar": "星目",
    "eyestar2": "星目2",
    "eyeheart": "はぁと",
    "starlight": "スターライト",
    "eye small": "瞳小",
    "eye funky": "恐ろしい子！",
    "round eye": "丸い目",
    "eye small h": "瞳縦潰れ",
    "eye invert": "ｺｯﾁﾐﾝﾅ",
    "eye hi off": "ハイライト消",
    "a2": "あ２",
    "a3": "あ３",
    "o small": "お小さい",
    "kiss": "キッス",
    "mouse 1": "∧",
    "mouse 2": "▲",
    "anger": "怒り",
    "wha??": "ええ？",
    "niyari": "にやり",
    "v": "V",
    "omega": "ω",
    "omega a": "ω□",
    "mouth down": "口上げ",
    "mouth up": "口下げ",
    "mouth narrow": "口すぼめる",
    "mouth widen": "口横広げ",
    "get angry": "怒り眉",
    "serious": "真面目",
    "smiley": "にこり眉",
    "trouble": "困った",
    "sadness": "動揺",
    "brow up": "眉上",
    "brow down": "眉下",
}


def copy_shapekey(shapekey: bpy.types.ShapeKey, target: str):
    if (not shapekey
            or target is None
            or shapekey.name == target):
        return

    shapekey.value = 1
    bpy.ops.object.shape_key_add(from_mix=True)
    bpy.context.object.active_shape_key.name = target
    shapekey.value = 0


class DuplicateVisemeAsMmdShapekey(bpy.types.Operator):
    bl_idname = "mesh.duplicate_mmd_shapekeys"
    bl_label = "Duplicate Shape Keys With MMD Names"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        obj = context.object
        settings: CopyAsMMDSettings = obj.CopyAsMMDSettings
        shapekeys: Dict = obj.data.shape_keys.key_blocks

        copy_shapekey(shapekeys.get(settings.ah), VISEMES['ah'])
        copy_shapekey(shapekeys.get(settings.ch), VISEMES['ch'])
        copy_shapekey(shapekeys.get(settings.u), VISEMES['u'])
        copy_shapekey(shapekeys.get(settings.e), VISEMES['e'])
        copy_shapekey(shapekeys.get(settings.oh), VISEMES['oh'])

        # Text Separator Shapekey
        bpy.ops.object.shape_key_add(from_mix=False)
        bpy.context.object.active_shape_key.name = " ^ MMD Visemes / Other v"

        for (key, name) in copy_as_mmd_settings.SHAPEKEY_LIST:
            sk = getattr(settings, key)
            if sk:
                copy_shapekey(shapekeys.get(sk), MMD_SHAPEKEYS.get(name or key))

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(DuplicateVisemeAsMmdShapekey.bl_idname, text=DuplicateVisemeAsMmdShapekey.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(DuplicateVisemeAsMmdShapekey)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(DuplicateVisemeAsMmdShapekey)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

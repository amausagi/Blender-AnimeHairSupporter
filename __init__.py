# アドオンを読み込む時に最初にこのファイルが読み込まれます
import importlib
import inspect
import sys
import bpy

# アドオン情報
bl_info = {
    'name': "Anime Hair Supporter",
    'author': "saidenka",
    'version': (1, 0, 1),
    'blender': (2, 80, 0),
    'location': "3Dビュー > オブジェクトモード > サイドバー > ツール > アニメ髪支援パネル",
    'description': "",
    'warning': "",
    'wiki_url': "https://github.com/saidenka/Blender-AnimeHairSupporter",
    'tracker_url': "https://github.com/saidenka/Blender-AnimeHairSupporter",
    'category': "Tools"
}

# サブスクリプト群をインポート
module_names = [
    "_panel",
    "convert_edgemesh_to_curve",
    "convert_curve_to_edgemesh",
    "maincurve_activate",
    "maincurve_volume_up",
    "maincurve_volume_down",
    "maincurve_extra_deform",
    "maincurve_gradation_tilt",
    "maincurve_select",
    "maincurve_hide",
    "maincurve_set_resolution",
    "maincurve_set_order",
    "tapercurve_activate",
    "tapercurve_id_singlize",
    "tapercurve_change_type",
    "tapercurve_mirror",
    "tapercurve_relocation",
    "tapercurve_remove_alones",
    "tapercurve_select",
    "tapercurve_hide",
    "convert_curve_to_armature",
    "convert_curve_to_mesh",
]
namespace = {}
for name in module_names:
    fullname = '{}.{}.{}'.format(__package__, "lib", name)
    if fullname in sys.modules:
        namespace[name] = importlib.reload(sys.modules[fullname])
    else:
        namespace[name] = importlib.import_module(fullname)


# パネルの設定
class AHS_Props(bpy.types.PropertyGroup):
    maincurve_expand: bpy.props.BoolProperty(name="メインパネルを展開", default=True)
    tapercurve_expand: bpy.props.BoolProperty(name="テーパーパネルを展開", default=True)
    bevelcurve_expand: bpy.props.BoolProperty(name="ベベルパネルを展開", default=True)

# モジュールからクラスの取得
classes = [AHS_Props]
for module in module_names:
    for module_class in [obj for name, obj in inspect.getmembers(namespace[module]) if inspect.isclass(obj)]:
        classes.append(module_class)


# プラグインをインストールしたときの処理
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ahs_props = bpy.props.PointerProperty(type=AHS_Props)


# プラグインをアンインストールしたときの処理
def unregister():
    from pathlib import Path
    if bpy.context.scene.get('ahs_props'):
        del bpy.context.scene['ahs_props']
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    Path(__file__).touch()

# 最初に実行される
if __name__ == '__main__':
    register()

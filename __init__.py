import bpy
import mathutils

bl_info = {
    "name": "レベルエディタ",
    "author": "Tonosaki Ren",
    "version":(1,0),
    "blender":(3,5,0),
    "location":"",
    "description":"レベルエディタ",
    "warning":"",
    "wiki_url":"",
    "tracker_url":"",
    "category":"Object"
}

#モジュールのインポート
from .export_scene import MYADDON_OT_export_scene
from .draw_collider import DrawCollider
from .stretch_vector import MYADDON_OT_stretch_vertex
from .create_ico_sphere import MYADDON_OT_create_ico_sphere
from .add_disable import MYADDON_OT_add_disable
from .add_disable import OBJECT_PT_disabled
from .add_collider import MYADDON_OT_add_collider
from .add_collider import OBJECT_PT_collider
from .add_point_light import MYADDON_OT_add_point_light
from .add_point_light import OBJECT_PT_point_light
from .add_filename import MYADDON_OT_add_filename
from .add_filename import OBJECT_PT_filename
from .spawn import MYADDON_OT_spawn_import_symbol
from .spawn import MYADDON_OT_spawn_create_symbol
from .spawn_player import MYADDON_OT_spawn_create_player_symbol
from .spawn_player import MYADDON_OT_spawn_create_player_symbol_menu
from .spawn_enemy import MYADDON_OT_spawn_create_enemy_symbol
from .spawn_enemy import MYADDON_OT_spawn_create_enemy_symbol_menu

#オペレータ pointLight生成
class MYADDON_OT_create_point_light(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_point_light"
    bl_label = "pointLight生成"
    bl_description = "pointLight生成します"
    bl_options = {'REGISTER' , 'UNDO'}

    # メニューを実行したときに呼ばれる関数
    def execute(self, context):
        bpy.ops.object.light_add(type='POINT', radius=0.1, location=(0, 0, 0))

        # 現在のライトオブジェクトを取得
        light = bpy.context.object

        # カスタムプロパティを設定
        light["pointLight"] = "pointLight"
        light["pointLight_color"] = mathutils.Vector((0, 0, 0))

        print("pointLightを生成しました。")

        return{'FINISHED'}

def draw_menu_manual(self,context):
    #self : 呼び出し元のクラスインスタンス。 C++でいうthisポインタ
    #context : カーソルを合わせた時のポップアップのカスタマイズなどに使用
    #トップバーの「エディターメニュー」に項目(オペレータ)を追加
    self.layout.operator("wm.url_open_preset",text="Manual",icon = 'HELP')

#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #Blenderがクラスを識別するための文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_decription = "拡張メニュー by " + bl_info["author"]

    # サブメニューの描画
    def draw(self, context):

        #トップバーの「エディターメニュー」に項目(オペレータ)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text = MYADDON_OT_stretch_vertex.bl_label)
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, text = MYADDON_OT_create_ico_sphere.bl_label)
        self.layout.operator(MYADDON_OT_create_point_light.bl_idname, text = MYADDON_OT_create_point_light.bl_label)
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, text = MYADDON_OT_export_scene.bl_label)
        self.layout.menu(MYADDON_OT_spawn_create_player_symbol_menu.bl_idname,text=MYADDON_OT_spawn_create_player_symbol_menu.bl_label)
        self.layout.menu(MYADDON_OT_spawn_create_enemy_symbol_menu.bl_idname,text=MYADDON_OT_spawn_create_enemy_symbol_menu.bl_label)
        #区切り線
        self.layout.separator()
        self.layout.operator("wm.url_open_preset", text = "Manual" , icon = 'HELP')
    
    # 既存のメニューにサブメニューを追加
    def submenu(self,context):
        
        # 既存のメニューにサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)
    

classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_create_point_light,
    TOPBAR_MT_my_menu,
    MYADDON_OT_export_scene,
    MYADDON_OT_add_filename,
    OBJECT_PT_filename,
    MYADDON_OT_add_point_light,
    OBJECT_PT_point_light,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
    MYADDON_OT_add_disable,
    OBJECT_PT_disabled,
    MYADDON_OT_spawn_import_symbol,
    MYADDON_OT_spawn_create_symbol,
    MYADDON_OT_spawn_create_player_symbol,
    MYADDON_OT_spawn_create_player_symbol_menu,
    MYADDON_OT_spawn_create_enemy_symbol,
    MYADDON_OT_spawn_create_enemy_symbol_menu,
)

#Add-On有効化時にコールバック
def register():

    #Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)
    #メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)

    #3Dビューに描画関数を追加
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider,(),"WINDOW","POST_VIEW")
    print("レベルエディタが有効化されました")

def unregister():
     #メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
     #3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle,"WINDOW")

     #Blenderにクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("レベルエディタが無効化されました")

if __name__ == "__main__":
    register()
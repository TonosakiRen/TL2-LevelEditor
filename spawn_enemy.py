import bpy
import bpy.ops

from .spawn import MYADDON_OT_spawn_create_symbol

class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label = "エネミーの出現シンボルの作成"
    bl_description = "エネミー出現ポイントのシンボルを作成します"

    def execute(self,context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT',type="Enemy")
        
        return {"FINISHED"}

#トップバーの拡張メニュー
class MYADDON_OT_spawn_create_enemy_symbol_menu(bpy.types.Menu):
    bl_idname ="MYADDON_OT_spawn_create_enemy_symbol_menu"
    bl_label="エネミーの出現ポイントの作成"
    bl_description="プレイヤエネミーの出現ポイントの作成します"

    def draw(self, context):
        layout = self.layout
        layout.operator(MYADDON_OT_spawn_create_enemy_symbol.bl_idname, text="エネミーの出現ポイントを作成")
import bpy
import bpy.ops

from .spawn import MYADDON_OT_spawn_create_symbol

class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label = "プレイヤーの出現シンボルの作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT',type="Player")
        
        return {"FINISHED"}
    
    
#トップバーの拡張メニュー
class MYADDON_OT_spawn_create_player_symbol_menu(bpy.types.Menu):
    bl_idname = "MYADDON_OT_spawn_create_player_symbol_menu"
    bl_label="プレイヤーの出現ポイントの作成"
    bl_description="プレイヤーの出現ポイントの作成します"
    bl_options = {'REGISTER','UNDO'}

    def draw(self, context):
        layout = self.layout
        layout.operator(MYADDON_OT_spawn_create_player_symbol.bl_idname, text="プレイヤーの出現ポイントを作成")
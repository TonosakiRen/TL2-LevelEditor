import bpy
import mathutils

#オペレータ カスタムプロパティ['pointLight']カスタムプロパティを追加
class MYADDON_OT_add_point_light(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_point_light"
    bl_label = "PointLight 追加"
    bl_description = "['pointLight']カスタムプロパティを追加します"
    bl_options = {"REGISTER","UNDO"}

    def execute(self,context):
        
        #['file_name']カスタムプロパティを追加
        context.object["pointLight"] = "pointLight"
        context.object["pointLight_color"] =  mathutils.Vector((0,0,0))

        return {"FINISHED"}
    
#パネル ファイル名
class OBJECT_PT_point_light(bpy.types.Panel):
    """オブジェクトのファイルネームパネル"""
    bl_idname = "OBJECT_PT_point_light"
    bl_label = "PointLight"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.object and "pointLight" in context.object

    # サブメニューの描画
    def draw(self,context):

        #パネルに項目追加
        if "pointLight" in context.object:
           #既にプロパティがあれば、プロパティを表示
            self.layout.prop(context.object,'["pointLight"]',text = "Type")
            self.layout.prop(context.object,'["pointLight_color"]',text = "Color")



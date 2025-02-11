import bpy
import bpy_extras
import math
import json

#オペレータ シーン出力
class MYADDON_OT_export_scene(bpy.types.Operator,bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"
    #出力するファイルの拡張子
    filename_ext = ".json"

    def execute(self,context):

        print("シーン情報Exportします")
        self.export_json()


        print("シーン情報をExportしました")
        self.report({'INFO'},"シーン情報をExportしました")

        return {'FINISHED'}
    
    def export_json(self):
        """JSON形式でファイルに出力"""

        #保存する情報をまとめる
        json_object_root = dict()

        #ノード名
        json_object_root["name"] = "scene"
        #オブジェクトリストを作成
        json_object_root["objects"] = list()
        #Todo: シーン内の全オブジェクト走査してパック
        #シーン内の全オブジェクトについて
        for object in bpy.context.scene.objects:

            #親オブジェクトがあるものはスキップ(代わりに親から呼び出すから)
            if(object.parent):
                continue
            
            #シーン直下のオブジェクトをルートノード(深さ0)とし、再帰関数で操作
            self.parse_scene_recursive_json(json_object_root["objects"],object,0)

        
        #オブジェクトをJSON文字列にエンコード
        json_text = json.dumps(json_object_root,ensure_ascii=False,cls=json.JSONEncoder,indent = 4)
        #コンソールに表示してみる
        print(json_text)

        #ファイルをテキスト形式で書きだしようにオープン
        #スコープを抜けると自動的にクローズされる
        with open(self.filepath,"wt",encoding="utf-8") as file:

            #ファイルに文字列を書き込む
            file.write(json_text)


    def export(self):
        """ファイルに出力"""

        print("シーン情報出力開始... %r" % self.filepath)

        #ファイルをテキスト形式で書き出し用にオープン
        #スコープを抜けると自動的にクローズされる
        with open(self.filepath,"wt") as file:

            #ファイルに文字列に書き込む
            self.write_and_print(file,"SCENE")

            #シーン内の全オブジェクトについて
            for object in bpy.context.scene.objects:
                
                 #親オブジェクトがあるものはスキップ(代わりに親を呼び出すから)
                if (object.parent):
                    continue

                #シーン直下のオブジェクトをルートノード(深さ０)とし、再起関数で走査
                self.parse_scene_recursive(file,object,0)
                    


    def write_and_print(self,file,str):
        print(str)

        file.write(str)
        file.write('\n')

    def parse_scene_recursive(self,file,object,level):
        """シーン解析用関数"""

        #深さ分インデントする(タブを挿入)
        indent = ''
        for i in range(level):
            indent += "\t" 

        self.write_and_print(file,indent + object.type)
        #ローカルトランスフォーム行列から平行移動、回転、スケーリングを抽出
        #型はVector,Quaternion,Vector
        trans,rot,scale = object.matrix_local.decompose()
        #回転を Quternion から Euler (3軸での回転角) に 変換
        rot = rot.to_euler()
        #ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)     
        #トランスフォーム情報を表示
        self.write_and_print(file,indent + "T %f %f %f" % (trans.x,trans.y,trans.z))
        self.write_and_print(file,indent + "R %f %f %f" % (rot.x,rot.y,rot.z))
        self.write_and_print(file,indent + "S %f %f %f" % (scale.x,scale.y,scale.z))
        #カスタムプロパティ'file_name'
        if "file_name" in object:
            self.write_and_print(file,indent + "N %s" % object["file_name"])
        #カスタムプロパティ 'collision'
        if "collider" in object:
            self.write_and_print(file,indent + "C %s" % object["collider"])
            temp_str = indent + "CC %f %f %f"
            temp_str %= (object["collider_center"][0],object["collider_center"][1],object["collider_center"][2])
            self.write_and_print(file,temp_str)
            temp_str = indent + "CS %f %f %f"
            temp_str %= (object["collider_size"][0],object["collider_size"][1],object["collider_size"][2])
            self.write_and_print(file,temp_str)
        self.write_and_print(file,indent + 'END')
        self.write_and_print(file,'')
        #カスタムプロパティ'無効オプション'
        if "disable" in object:
            self.write_and_print(file,indent + "D %s" % object["disable"])

        #子ノードへ進む(深さが１上がる)
        for child in object.children:
            self.parse_scene_recursive(file,child,level + 1)

    def parse_scene_recursive_json(self,data_parent,object,level):

        #シーンのオブジェクト1個分のjsonオブジェクト生成
        json_object = dict()
        #オブジェクト種類
        if "type" in object:
            json_object["type"] = object["type"]
        

        #オブジェクト名
        json_object["name"] = object.name

        #Todo: その他情報をパック
        #オブジェクトのローカルトランスフォームから
        #平行移動、回転、スケールを抽出
        trans,rot,scale = object.matrix_local.decompose()
        #回転を Quaternionから Euler (3 軸での回転角)に変更
        rot = rot.to_euler()
        #ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        #トランスフォーム情報をディクショナリに登録
        transform = dict()
        transform["translation"] = (trans.x,trans.y,trans.z)
        transform["rotation"] = (rot.x,rot.y,rot.z)
        transform["scaling"] = (scale.x,scale.y,scale.z)
        #まとめて1子分のjsonオブジェクトに登録
        json_object["transform"] = transform
        
        #カスタムプロパティ'file_name'
        if "file_name" in object:
            json_object["file_name"] = object["file_name"]
        
        #カスタムプロパティ 'collider'
        if "collider" in object:
            collider = dict()
            collider["type"] = object["collider"]
            collider["center"] = object["collider_center"].to_list()
            collider["size"] = object["collider_size"].to_list()
            json_object["collider"] = collider

        #カスタムプロパティ 'pointLight'
        if "pointLight" in object:
            pointLight = dict()
            pointLight["type"] = object["pointLight"]
            pointLight["color"] = object["pointLight_color"].to_list()
            json_object["pointLight"] = pointLight

        #カスタムプロパティ'file_name'
        if "disable" in object:
            json_object["disable"] = object["disable"]

        #1個分のjsonオブジェクトを親オブジェクトに登録
        data_parent.append(json_object)

        #Todo: 直接の子供リストを走査
        if len(object.children) > 0:
            #子ノードリストを作成
            json_object["children"] = list()

            #子ノードへ進む(深さが1下がる)
            for child in object.children:
                self.parse_scene_recursive_json(json_object["children"],child,level + 1)
    
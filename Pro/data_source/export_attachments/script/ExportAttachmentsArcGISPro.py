# coding:utf-8
# Purpose : ArcGIS Online のホストフィーチャサービスをローカルにダウンロードして添付ファイルを抽出します。
# Author : ESRIジャパン

#------------------------------------------------------------------------------------
# モジュールのインポート
#------------------------------------------------------------------------------------
import arcpy
import arcgis.features
import arcgis.features.managers
import arcgis.gis
import os
import zipfile
from datetime import datetime


#------------------------------------------------------------------------------------
# パラメーターの設定
#------------------------------------------------------------------------------------
agol_flag = arcpy.GetParameterAsText(0)
user_name = arcpy.GetParameterAsText(1)
password = arcpy.GetParameterAsText(2)
feature_service_url = arcpy.GetParameterAsText(3)
replica_layers = arcpy.GetParameterAsText(4)
attachment_table = arcpy.GetParameterAsText(5)
dtime = datetime.now().strftime("%Y%m%d%H%M%S")
replica_name = "replica_%s" % (dtime)
output_folder = os.path.join(arcpy.GetParameterAsText(6), replica_name)


#------------------------------------------------------------------------------------
# ArcGIS Online にアクセス
#------------------------------------------------------------------------------------
def AccessAgol(user_name, password):
    gis = arcgis.gis.GIS("https://www.arcgis.com", user_name, password)
    return gis

#------------------------------------------------------------------------------------
# データを分割するための OBJECTID のリストを取得 (大量データに対してレプリカを作成できないため最大 5000 レコードに分割)
# ※ツールの実行に失敗する場合は、分割するレコード数を小さく設定して試してください
#------------------------------------------------------------------------------------
def SplitObjectIds(object_ids):
    n = 5000
    sort_object_ids = sorted(object_ids)
    for i in range(0, len(sort_object_ids), n):
        yield sort_object_ids[i:i + n]


#------------------------------------------------------------------------------------
# レプリカを作成する際の条件式を作成
#------------------------------------------------------------------------------------
def CreateWheres(replica_layers, feature_layer_collection):
    # フィーチャ サービスの各レイヤーに対して処理
    for id in replica_layers.split(","):
        for feature_layer in feature_layer_collection.layers:
            if feature_layer.url[-1] == id:
                query = feature_layer.query(where='1=1', return_ids_only=True)
                # レコードを分割して処理するための条件式を作成
                split_object_ids = SplitObjectIds(query["objectIds"])
                for object_ids in split_object_ids:
                    sql_Where = "{'%s': {'where':'(OBJECTID >= %d AND OBJECTID <= %d)' , 'useGeometry' : false}}" %(id, object_ids[0], object_ids[-1])
                    yield sql_Where

#------------------------------------------------------------------------------------
# 条件式ごとにファイル ジオデータベースのレプリカを作成しローカルにダウンロード
#------------------------------------------------------------------------------------
def CreateReplicaAndDownroad(feature_service_url, gis, replica_name, replica_layers, output_folder):
    # 処理対象のフィーチャ サービスを取得
    feature_layer_collection = arcgis.features.FeatureLayerCollection(feature_service_url, gis)
    # フィーチャ サービスがレプリカの作成に対応しているかチェック
    if "Extract" in feature_layer_collection.properties.capabilities and "Sync" in feature_layer_collection.properties.capabilities:
        # 指定したフォルダーが存在しない場合は作成
        if os.path.exists(output_folder) == False:
            os.mkdir(output_folder)
        # 条件式ごとにレプリカを作成
        layer_queries = CreateWheres(replica_layers, feature_layer_collection)
        for layer_query in layer_queries:
            replica = feature_layer_collection.replicas.create(replica_name=replica_name,
                                                               layers=replica_layers,
                                                               layer_queries=layer_query,
                                                               return_attachments=True,
                                                               return_attachments_databy_url=False,
                                                               asynchronous=True,
                                                               attachments_sync_direction="bidirectional",
                                                               sync_model="none",
                                                               data_format="filegdb",
                                                               wait=True,
                                                               out_path=output_folder)
            yield replica
    else:
        arcpy.AddError("> 対象のフィーチャ サービスがレプリカの作成に対応していません。フィーチャ サービスの同期とエクスポート機能を有効化して再度試してください。")


#------------------------------------------------------------------------------------
# ダウンロードしたレプリカ (ZIP ファイル) からアタッチメント テーブルを取得
#------------------------------------------------------------------------------------
def GetAttachmentTable(zip_files):
    # ZIP ファイルを解凍
    for zip_file in zip_files:
        extract_path = os.path.splitext(zip_file)[0]
        with zipfile.ZipFile(zip_file) as z:
            z.extractall(extract_path)
        os.remove(zip_file)
        # 解凍したファイルからアッタッチメント テーブルを取得
        walk = arcpy.da.Walk(extract_path, topdown=True, datatype="FeatureClass")
        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                attachment_table = "%s__ATTACH" %(os.path.join(dirpath, filename))
                yield attachment_table


#------------------------------------------------------------------------------------
# アタッチメントテーブルから添付ファイル抽出
#------------------------------------------------------------------------------------
def ExportAttachments(attachment_tables, dtime, output_folder):
    for attachment_table in attachment_tables:
        # 入力テーブルからパスを取得して、ワークスペースを設定
        workspace_path = os.path.dirname(attachment_table)
        arcpy.env.workspace = workspace_path
        # 入力テーブルから、テーブル結合に使用するための結合先となるテーブルを取得
        input_table_name = os.path.basename(attachment_table)
        join_featureclass_name = input_table_name.split("__")[0]
        # テーブル結合を行うためのデータを作成
        input_table_view = arcpy.MakeTableView_management(attachment_table, "inTableView_%s" %(dtime))
        join_feature_layer = arcpy.MakeFeatureLayer_management(join_featureclass_name, "featureLayer_%s" % (dtime))
        # アタッチメント テーブルの GUID フィールド名を取得
        for view_field in arcpy.ListFields(input_table_view):
            if view_field.type.lower() == "guid":
                guid_field_name = view_field.name
                break
        # フィーチャクラスの Global ID フィールド名を取得
        for field in arcpy.ListFields(join_feature_layer):
            if field.type.lower() == "globalid":
                globalid_field_name = field.name
            elif field.type.lower() == "oid":
                oid_field_name = field.name
        # テーブル結合の実行
        join_layer = arcpy.AddJoin_management(
                        input_table_view, guid_field_name, join_feature_layer, globalid_field_name, "KEEP_ALL")
        # 結合テーブルから添付ファイルを抽出して出力
        with arcpy.da.SearchCursor(join_layer,
                                ["%s.DATA" %(input_table_name),
                                    "%s.ATT_NAME" %(input_table_name),
                                    "%s.%s" %(join_featureclass_name, oid_field_name)]) as cursor:
            for row in cursor:
                binaryRep = row[0]
                fileName = row[1]
                OID = row[2]
                open("%s//%s_%s" %(output_folder, OID, fileName), "wb").write(binaryRep)
                del row
                del binaryRep
                del fileName
                arcpy.Delete_management(join_layer)
                arcpy.Delete_management(input_table_view)
                arcpy.Delete_management(join_feature_layer)


#------------------------------------------------------------------------------------
# メインの処理
#------------------------------------------------------------------------------------
def main():
    try:
        arcpy.env.overwriteOutput = True
        if agol_flag == "true":
            arcpy.AddMessage("> ArcGIS Online にアクセスしています。")
            gis = AccessAgol(user_name, password)
            arcpy.AddMessage("> ArcGIS Online のホスト フィーチャサービスからファイル ジオデータベースのレプリカを作成しています。")
            zip_files = CreateReplicaAndDownroad(feature_service_url, gis, replica_name, replica_layers, output_folder)
            arcpy.AddMessage("> ダウンロードしたレプリカ (ZIP ファイル) からアタッチメント テーブルを取得しています。")
            attachment_tables = GetAttachmentTable(zip_files)
            arcpy.AddMessage("> アタッチメント テーブルから添付ファイル抽出しています。")
            ExportAttachments(attachment_tables, dtime, output_folder)
        else:
            arcpy.AddMessage("> アタッチメント テーブルから添付ファイル抽出しています。")
            ExportAttachments([attachment_table], dtime, output_folder)
    except Exception as e:
        arcpy.AddError(str(e))


#------------------------------------------------------------------------------------
# モジュール実行
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
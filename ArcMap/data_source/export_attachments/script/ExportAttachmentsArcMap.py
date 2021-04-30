# coding:utf-8
# Purpose : ArcGIS Online のホストフィーチャサービスをローカルにダウンロードして添付ファイルを抽出します。
# Author : ESRIジャパン

#------------------------------------------------------------------------------------
# モジュールのインポート
#------------------------------------------------------------------------------------
import arcpy
import urllib
import urllib2
import json
import os
import time
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
# サービスにリクエストを送信
#------------------------------------------------------------------------------------
def SendRequest(request):
    response = urllib2.urlopen(request)
    read_response = response.read()
    json_response = json.loads(read_response)
    return json_response


#------------------------------------------------------------------------------------
# トークンを生成
#------------------------------------------------------------------------------------
def CreateToken(user_name, password):
    url = "https://arcgis.com/sharing/rest/generateToken"
    data = {"username": user_name,
            "password": password,
            "referer": "https://www.arcgis.com",
            "f": "json"}
    request = urllib2.Request(url, urllib.urlencode(data))
    json_response = SendRequest(request)
    token = json_response["token"]
    return token


#------------------------------------------------------------------------------------
# データを分割するための OBJECTID のリストを取得 (大量データに対してレプリカを作成できないため最大 5000 レコードに分割)
#------------------------------------------------------------------------------------
def SplitObjectIds(object_ids):
    n = 5000
    sort_object_ids = sorted(object_ids)
    for i in range(0, len(sort_object_ids), n):
        yield sort_object_ids[i:i + n]


#---------------------------------------------------------- --------------------------
# レプリカを作成する際の条件式を作成
#------------------------------------------------------------------------------------
def CreateWheres(replica_layers, feature_service_url, token):
    # フィーチャ サービスの各レイヤーに対して処理
    for id in replica_layers.split(","):
        query_url = "%s//%s//query" %(feature_service_url, id)
        data = {"f": "json",
                "where": "1=1",
                "returnIdsOnly": "true",
                "token": token}
        request = urllib2.Request(query_url, urllib.urlencode(data))
        json_response = SendRequest(request)
        # 最大 5000 レコードずつ処理するための条件式を作成
        split_object_ids = SplitObjectIds(json_response["objectIds"])
        for object_ids in split_object_ids:
            sql_Where = "{'%s': {'where':'(OBJECTID >= %d AND OBJECTID <= %d)' , 'useGeometry' : false}}" %(id, object_ids[0], object_ids[-1])
            yield sql_Where


#------------------------------------------------------------------------------------
# ファイル ジオデータベースのレプリカを作成
#------------------------------------------------------------------------------------
def CreateReplicaAndDownroad(output_folder, token, replica_name, replica_layers, feature_service_url):
    # フィーチャ サービスがレプリカの作成に対応しているかチェック
    data = {"f": "json", "token": token}
    request = urllib2.Request(feature_service_url, urllib.urlencode(data))
    json_response = SendRequest(request)
    capabilities = json_response["capabilities"]
    if "Extract" in capabilities and "Sync" in capabilities:
        # 条件式ごとにレプリカを作成
        create_replica_url = "%s//createReplica" %(feature_service_url)
        layer_queries = CreateWheres(replica_layers, feature_service_url, token)
        for layer_query in layer_queries:
            # レプリカ作成のパラメーターを設定
            data = {"f": "json",
                    "replicaName": replica_name,
                    "layers": replica_layers,
                    "layerQueries": "%s" %(layer_query),
                    "returnAttachments": "true",
                    "returnAttachmentsDatabyURL": "false",
                    "syncModel": "none",
                    "attachmentsSyncDirection": "bidirectional",
                    "dataFormat": "filegdb",
                    "async": "true",
                    "token": token}
            # レプリカ作成のリクエストを送信
            request = urllib2.Request(create_replica_url, urllib.urlencode(data))
            json_response = SendRequest(request)
            url = json_response["statusUrl"]
            check_status_url = "%s?f=json&token=%s" %(url, token)
            request = urllib2.Request(check_status_url)
            json_response = SendRequest(request)
            while not json_response["status"] == "Completed":
                time.sleep(5)
                request = urllib2.Request(check_status_url)
                json_response = SendRequest(request)
                url = json_response["resultUrl"]
            result_replica_url = "%s?token=%s" %(url, token)
            f = urllib2.urlopen(result_replica_url)
            # 指定したフォルダーが存在しない場合は作成
            if os.path.exists(output_folder) == False:
                os.mkdir(output_folder)
            zip_file = "%s\\%s" %(output_folder, replica_name + ".zip")
            with open(zip_file, "wb") as local_file:
                local_file.write(f.read())
            yield zip_file
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
            arcpy.AddMessage("> ArcGIS Online のサービス リクエストに有効なトークンを生成しています。")
            token = CreateToken(user_name, password)
            arcpy.AddMessage("> ArcGIS Online のホスト フィーチャサービスからファイル ジオデータベースのレプリカを作成しています。")
            zip_files = CreateReplicaAndDownroad(output_folder, token, replica_name, replica_layers, feature_service_url)
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

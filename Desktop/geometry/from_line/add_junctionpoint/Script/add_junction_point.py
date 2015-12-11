#coding:utf-8
#-------------------------------------------------------------------------------

import arcpy
import os.path

# フィーチャクラスの作成と属性情報コピーの準備
def setup(input,output):

    # 出力パスの取得
    out_dir = os.path.dirname(output)
    out_name = os.path.basename(output)

    # 入力データの情報を取得
    in_desc = arcpy.Describe(input)
    sr = in_desc.spatialReference
    shape_field = in_desc.ShapeFieldName
    oid_field = in_desc.OIDFieldName
    in_fields = in_desc.Fields

    # フィーチャクラスの作成
    arcpy.CreateFeatureclass_management(out_dir,out_name,"POINT",input,"","",sr)

    # 変数定義
    search_fields_name = []
    search_fields_type = []
    del_fields = []
    use_fields = []

    # 属性情報コピーの準備
    """
    入力:GDB、出力: Shape ファイルの場合
    ・ ID フィールドやShape_length、Shape_Area フィールドなど不必要なフィールドが
      付属するため、削除する。
    ・ フィールド名の長さに制限があるため、出力されるShape ファイルのフィールド名は
      短くなることが考えられる。ただし、フィールドの順序は入力と変化しないため、
      インデックス番号で管理する。
    """
    for i,field in enumerate(in_fields):
        if field.name == shape_field or field.name == oid_field:
            pass
        # 出力が Shape ファイルの場合は、削除対象
        elif field.name.lower() == u"shape_length" or \
             field.name.lower() == u"shape_area":
                del_fields.append(i)
        else:
            search_fields_name.append(field.name)
            search_fields_type.append(field.type)
            # 属性情報コピーの対象となるフィールドのインデックス番号を取得
            use_fields.append(i)

    out_fields = arcpy.ListFields(output)

    # 出力がShape ファイルの場合
    if arcpy.Describe(out_dir).workspacetype == u"FileSystem":

        # 入力もShape ファイルの場合はスルー。
        # Shape_Length、Shape_Area フィールドは削除
        if arcpy.Describe(in_desc.path).workspacetype != u"FileSystem":
            del_fields_name = [out_fields[index].name for index in del_fields]
            arcpy.DeleteField_management(output,del_fields_name)

        # 属性情報コピーの対象とするフィールド名のリストを作成
        # （インデックス番号を用いて Shape ファイルで短くなった名前を取得）
        use_fields_name = [out_fields[index].name for index in use_fields]
        use_fields_name.append("SHAPE@")

    # 出力が GDB の場合は、入力データと同じフィールド構造を使用
    else:
        use_fields_name = search_fields_name

    search_fields_name.append("SHAPE@")

    return search_fields_name,search_fields_type,use_fields_name

def main():

    input_line = arcpy.GetParameterAsText(0)
    output_point = arcpy.GetParameterAsText(1)
    overlap = arcpy.GetParameter(2)

    wstype = arcpy.Describe(os.path.dirname(output_point)).workspacetype

    # 重複を許可する場合、インターセクト ツールを実行して処理を完了
    if overlap == True:
        arcpy.Intersect_analysis(input_line,output_point,"NO_FID","","POINT")
    # 許可しない場合、OID フィールドが早い方を残すように処理を実行
    else:
        search_fields_name,search_fields_type,use_fields_name =  setup(input_line,output_point)

        # インターセクト ツールを実行して交点にポイント発生
        arcpy.Intersect_analysis(input_line,r"in_memory\Intersect","NO_FID","","POINT")

        # インターセクトの結果はマルチパート ポイントで出力されるため、シングルパートに変換
        arcpy.MultipartToSinglepart_management(r"in_memory\Intersect",r"in_memory\Single")

        with  arcpy.da.SearchCursor(r"in_memory\Single",search_fields_name) as input_cur:
            output_cur = arcpy.da.InsertCursor(output_point,use_fields_name)
            list = []

            for row in input_cur:
                # リスト内に同一のポイントが存在しないかを確認
                if not (row[-1].firstPoint.X,row[-1].firstPoint.Y) in list:

                    # 出力がShape ファイルの場合、NULL 値を格納できないため
                    # フィールドのタイプに合わせて、空白や 0 を格納する
                    if wstype == u"FileSystem":
                        geom = row[-1]
                        newValue = []

                        for i,value in enumerate(row[:-1]):
                            if value == None:
                                if search_fields_type[i] == u"String":
                                    newValue.append("")
                                elif search_fields_type[i] in [u"Double",u"Integer",u"Single",u"SmallInteger"]:
                                    newValue.append(0)
                                else:
                                    newValue.append(value)
                            else:
                                newValue.append(value)
                        new_row = tuple(newValue) + (geom,)
                        output_cur.insertRow(new_row)
                        
                        # リストにポイント情報を登録し、重複しないように処理
                        list.append((row[-1].firstPoint.X,row[-1].firstPoint.Y))
                    else:
                        output_cur.insertRow(row)
                        # リストにポイント情報を登録し、重複しないように処理
                        list.append((row[-1].firstPoint.X,row[-1].firstPoint.Y))

        # インメモリ ワークスペースの削除
        arcpy.Delete_management("in_memory")
        
        del input_cur,output_cur

if __name__ == "__main__":
    main()


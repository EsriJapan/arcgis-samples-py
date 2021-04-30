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
    outputType = arcpy.GetParameterAsText(2)
    interval = arcpy.GetParameter(3)
    unit = arcpy.GetParameterAsText(4)

    wstype = arcpy.Describe(os.path.dirname(output_point)).workspacetype

    search_fields_name,search_fields_type,use_fields_name =  setup(input_line,output_point)

    with  arcpy.da.SearchCursor(input_line,search_fields_name) as input_cur:
        output_cur = arcpy.da.InsertCursor(output_point,use_fields_name)

        for row in input_cur:
            geom = row[-1]
            newValue = []

            # 出力がShape ファイルの場合、NULL 値を格納できないため
            # フィールドのタイプに合わせて、空白や 0 を格納する
            if wstype == "FileSystem":
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
            # GDB は NULL 値を格納可能なので元データをそのままコピー
            else:
                newValue = row[:-1]


            totalLength = geom.length
            addPointNum = int(totalLength/interval)
            i = 1
            if outputType == u"始点から":
                newRow = tuple(newValue) + (geom.firstPoint,)
                output_cur.insertRow(newRow)
                while i < addPointNum + 1:
                    newRow = tuple(newValue) + (geom.positionAlongLine(interval * i),)
                    output_cur.insertRow(newRow)
                    i += 1
                newRow = tuple(newValue) + (geom.lastPoint,)
                output_cur.insertRow(newRow)
            else:
                newRow = tuple(newValue) + (geom.lastPoint,)
                output_cur.insertRow(newRow)
                while i < addPointNum + 1:
                    newRow = tuple(newValue) + (geom.positionAlongLine(totalLength - interval*i),)
                    output_cur.insertRow(newRow)
                    i += 1
                newRow = tuple(newValue) + (geom.firstPoint,)
                output_cur.insertRow(newRow)

    del input_cur,output_cur

if __name__ == "__main__":
    main()


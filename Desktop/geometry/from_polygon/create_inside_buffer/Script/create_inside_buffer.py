#coding:utf-8
#-------------------------------------------------------------------------------

import arcpy

def main():

    #パラメータ
    in_polygon = arcpy.GetParameterAsText(0)
    out_polygon = arcpy.GetParameterAsText(1)
    distace = arcpy.GetParameter(2)
    unit = arcpy.GetParameterAsText(3)

    #出力データの作成
    arcpy.CopyFeatures_management(in_polygon,out_polygon)

    #バッファ作成
    with arcpy.da.UpdateCursor(out_polygon,["SHAPE@"]) as cursor:
        i = 0
        for row in cursor:
            geom = row[0]
            #Polygon.buffer メソッドの実行
            buffer = geom.buffer(float(distace) * -1)
            #内向きポリゴンが元のポリゴン範囲を超える場合は、面積0 のポリゴンが
            #作成されるためスキップ
            if buffer.area == 0.0:
                i += 1
                continue
            else:
                cursor.updateRow([geom.difference(buffer)])

    #作成できなかったポリゴンの有無をメッセージング
    if i != 0:
        arcpy.AddWarning(u"内向きバッファのサイズが元のポリゴンの範囲を超えていたため、作成できなかったデータがあります")

    del cursor

if __name__ == "__main__":
    main()

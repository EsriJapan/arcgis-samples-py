#coding:utf-8
#-------------------------------------------------------------------------------

import arcpy

def create_extent_polygon(mxd):

    #対象はアクティブなデータ フレーム内のレイヤ
    df = mxd.activeDataFrame

    #現在の表示範囲を取得
    extent = df.extent

    #10.3 からExtent オブジェクトから直接 Polygon オブジェクトを取得可能
    return extent.polygon

def main():

    #パラメータの設定
    inlyrs = arcpy.GetParameterAsText(0)
    select_type = arcpy.GetParameterAsText(1)
    distace = arcpy.GetParameterAsText(2)

    #現在開いているマップを取得
    mxd = arcpy.mapping.MapDocument("current")

    #レイヤを指定しない場合は、全フィーチャレイヤを対象
    if inlyrs == "":
        lyrs = arcpy.mapping.ListLayers(mxd)
    #指定した場合は、指定レイヤから Layer オブジェクトを生成
    else:
        lyrs = [arcpy.mapping.Layer(lyr) for lyr in inlyrs.split(";")]

    #範囲ポリゴンの生成
    ex_polygon = create_extent_polygon(mxd)

    #対象レイヤに空間検索を行う
    for lyr in lyrs:
        #前の結果が存在する場合は削除
        arcpy.SelectLayerByAttribute_management(lyr,"CLEAR_SELECTION")

        #レイヤ種別の判別（フィーチャ レイヤ以外は対象外）
        if lyr.isFeatureLayer:
            #空間検索条件の場合分け
            #空間検索のパラメータとして直接 Polygon オブジェクトを指定可能
            if select_type == u"表示範囲と重なる":
                arcpy.SelectLayerByLocation_management(lyr,"INTERSECT",ex_polygon,"","ADD_TO_SELECTION")
            elif select_type ==u"表示範囲内に完全に含まれる":
                arcpy.SelectLayerByLocation_management(lyr,"WITHIN",ex_polygon,"","ADD_TO_SELECTION")
            elif select_type == u"表示範囲から指定した距離内にある":
                arcpy.SelectLayerByLocation_management(lyr,"WITHIN_A_DISTANCE",ex_polygon,distace,"ADD_TO_SELECTION")

if __name__ == "__main__":
    main()
#coding:utf-8

"""
-------------------------------------------------------------------------------
 Name:        create_convexhull.py
 Purpose:     ポイントから凸包ポリゴンを作成
-------------------------------------------------------------------------------
"""
import arcpy
import os.path
import sys

def main():

    # パラメータ
    in_point = arcpy.GetParameterAsText(0)
    out_polygon = arcpy.GetParameterAsText(1)
    groupfield = arcpy.GetParameter(2)
    group_fieldname = arcpy.GetParameterAsText(3)
    createbuffer = arcpy.GetParameter(4)
    bufferdistance = arcpy.GetParameter(5)

    # 入力データの情報を取得
    desc = arcpy.Describe(in_point)
    sr = desc.SpatialReference

    tmp_polygon = "in_memory/tmpOut"
    outdir = os.path.dirname(tmp_polygon)
    outname = os.path.basename(tmp_polygon)

    arcpy.CreateFeatureclass_management(outdir,outname,"POLYGON","","","",sr)

    # point.convexHull メソッドはマルチパート ポイントが対象のためディゾルブを実行
    if groupfield == True:
        multi = arcpy.Dissolve_management(in_point,"in_memory/multi",group_fieldname)
    else:
        multi = arcpy.Dissolve_management(in_point,"in_memory/multi")

    with arcpy.da.SearchCursor(multi,["SHAPE@"]) as search_cur:
        insert_cur = arcpy.da.InsertCursor(tmp_polygon,["SHAPE@"])
        for row in search_cur:
            # ポイント数が 3 点以上存在しないとポリゴンが生成できないためスキップ
            if row[0].pointCount < 3:
                arcpy.AddWarning(u"入力フィーチャ数が足りません。")
                arcpy.AddWarning(u"ツールの実行にはポイントが 3 点以上必要です。")
                continue
            # convexHull メソッドで凸包ポリゴンを生成
            convex = row[0].convexHull()
            insert_cur.insertRow([convex])

    # バッファの生成
    if int(arcpy.GetCount_management(tmp_polygon).getOutput(0)) != 0:
        if createbuffer == True:
            arcpy.Buffer_analysis(tmp_polygon,out_polygon,bufferdistance)
        else:
            arcpy.CopyFeatures_management(tmp_polygon,out_polygon)

    arcpy.Delete_management("in_memory")
    
    del search_cur,insert_cur

if __name__ == "__main__":
    main()

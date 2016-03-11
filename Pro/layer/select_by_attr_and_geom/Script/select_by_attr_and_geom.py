#coding:utf-8
"""
-------------------------------------------------------------------------------
 Name:        select_by_attr_and_geom.py
 Purpose:     属性検索と空間検索の同時実行
 Author:      ESRI Japan
 Created:     11/03/2016
-------------------------------------------------------------------------------
"""

import arcpy


def main():

    inLayer = arcpy.GetParameterAsText(0)
    whereClause = arcpy.GetParameterAsText(1)
    select_features = arcpy.GetParameterAsText(2)
    overlap_type = arcpy.GetParameterAsText(3)
    search_distance = arcpy.GetParameterAsText(4)

    arcpy.SelectLayerByAttribute_management(inLayer,"CLEAR_SELECTION")
    arcpy.SelectLayerByAttribute_management(inLayer,"NEW_SELECTION",whereClause)

    if select_features == "":
        return
    else:
        if overlap_type == "空間検索対象レイヤと「交差する」":
            overlap = "INTERSECT"
        elif overlap_type == "空間検索対象レイヤと「交差する（3D）」":
            overlap = "INTERSECT_3D "
        elif overlap_type == "空間検索対象レイヤの「一定距離内に存在する」":
            overlap = "WITHIN_A_DISTANCE"
        elif overlap_type == "空間検索対象レイヤの「一定距離内に存在する（3D）」":
            overlap = "WITHIN_A_DISTANCE_3D"
        elif overlap_type == "空間検索対象レイヤを「含む」":
            overlap = "CONTAINS"
        elif overlap_type == "空間検索対象レイヤを「完全に含む」":
            overlap = "COMPLETELY_CONTAINS"
        elif overlap_type == "空間検索対象レイヤを「含む（clementini）」":
            overlap =  "CONTAINS_CLEMENTINI"
        elif overlap_type == "空間検索対象レイヤに「含まれる」":
            overlap = "WITHIN"
        elif overlap_type == "空間検索対象レイヤに「完全に含まれる」":
            overlap = "COMPLETELY_WITHIN"
        elif overlap_type == "空間検索対象レイヤに「含まれる（clementini）」":
            overlap = "WITHIN_CLEMENTINI"
        elif overlap_type == "空間検索対象レイヤと「正確に一致する」":
            overlap = "ARE_IDENTICAL_TO"
        elif overlap_type == "空間検索対象レイヤの「境界に接する」":
            overlap = "BOUNDARY_TOUCHES"
        elif overlap_type == "空間検索対象レイヤと「線分を共有する」":
            overlap = "SHARE_A_LINE_SEGMENT_WITH"
        elif overlap_type == "空間検索対象レイヤの「アウトラインが横切る」":
            overlap = "CROSSED_BY_THE_OUTLINE_OF"
        elif overlap_type == "空間検索対象レイヤ内に「重心が存在する」":
            overlap = "HAVE_THEIR_CENTER_IN"
        arcpy.SelectLayerByLocation_management(inLayer,overlap,
                            select_features,search_distance,"SUBSET_SELECTION")

if __name__ == "__main__":
    main()

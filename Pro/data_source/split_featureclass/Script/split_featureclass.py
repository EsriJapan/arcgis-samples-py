#coding:utf-8

"""
-------------------------------------------------------------------------------
 Name:        split_featureclass.py
 Purpose:     フィーチャクラスを属性値で分割
 Author:      horui
 Created:     30/09/2015
-------------------------------------------------------------------------------
"""

import arcpy
import os

# 選択ツールの実行関数
def run_select_tool(input,field,outputws,prefix,val):

    # 対象フィールドの取得
    fields = arcpy.Describe(input).fields
    target_field = [f for f in fields if f.name == field][0]

    # 出力ワークスペースの取得
    out_desc =arcpy.Describe(outputws)

    # 対象フィールドが文字列以外
    if target_field.type != "String":
        outname = prefix + str(val)
        # 条件式の生成
        exp = '"{0}" = {1}'.format(field,val)
        # 出力がフォルダ
        if out_desc.workspaceType == "FileSystem":
          output = outputws + os.sep + outname + ".shp"
        # 出力がファイルジオデータベース
        elif out_desc.workspaceType == "LocalDatabase":
          output = outputws + os.sep + outname
    # 対象フィールドが文字列
    elif target_field.type == "String":
        # 数字から始まる場合
        if val[0].isdigit():
            outname = prefix + str(val)
            # 条件式の生成
            exp = '"{0}" = {1}'.format(field,val)
            # 出力がフォルダ
            if out_desc.workspaceType == "FileSystem":
              output = outputws + os.sep + outname + ".shp"
            # 出力がファイルジオデータベース
            elif out_desc.workspaceType == "LocalDatabase":
              output = outputws + os.sep + outname
        # それ以外
        else:
            prefix = val
            # 条件式の生成
            exp = '"{0}" = \' + {1} + \''.format(field,val)
            # 出力がフォルダ
            if out_desc.workspaceType == "FileSystem":
              output = outputws + os.sep + prefix + ".shp"
            # 出力がファイルジオデータベース
            elif out_desc.workspaceType == "LocalDatabase":
              output = outputws + os.sep + prefix
    try:
        # 選択ツールの実行
        arcpy.Select_analysis(input,output,exp)
    except:
        arcpy.AddError(arcpy.GetMessages())


def main():

    # 変数へ代入
    input = arcpy.GetParameterAsText(0)
    field = arcpy.GetParameterAsText(1)
    outputws = arcpy.GetParameterAsText(2)
    prefix = arcpy.GetParameterAsText(3)

    # arcpy.da.SearchCursor 関数を使用して、分割するデータの Cursor を取得します。
    rows = arcpy.da.SearchCursor(input,[field])

    # 空の辞書型オブジェクトを作成します。
    dic = {}

    # フィーチャクラスが持つ属性値のリストを生成
    for row in rows:
      dic[row[0]] = "tmpVal"

    # オブジェクトを削除し、データへの参照を解放します。
    del rows
    i = 0

    # リスト内の属性値を使って、[選択] ツールの関数を実行します。
    for val in dic:

        run_select_tool(input,field,outputws,prefix,val)
        # 処理状況をプログレスウィンドウに表示
        arcpy.SetProgressor("default","{0} : {1} / {2}".format(val,i+1,len(dic)))
        i += 1

    # ツールの終了を表示します。
    arcpy.AddMessage(outputws + " に " + str(i) + " フィーチャクラスの出力が完了しました。")
    del outputws

if __name__ == "__main__":
    main()
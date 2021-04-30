# arcgis-samples-py

ArcPy サイト パッケージのサンプル集です。ArcMap 用と ArcGIS Pro 用のサンプルがあります。個々のサンプル リポジトリに tbx ファイルがある場合は、ArcMap や ArcGIS Pro でジオプロセシング ツールとしてそのまま利用することが可能です。

## 動作確認環境

各サンプル リポジトリを参照してください。

## サンプル リポジトリへのリンク
* 2D ポイント → 3D ポイントへ変換 ([ArcMap](./ArcMap/data_source/2dto3d_point) / [Pro](./Pro/data_source/2dto3d_point))
* 属性値を基にフィーチャクラスを分割 ([ArcMap](./ArcMap/data_source/split_featureclass) / [Pro](./Pro/data_source/split_featureclass))
* ライン データの始点/終点にポイントを発生 ([ArcMap](./ArcMap/geometry/from_line/add_firstlastpoint) / [Pro](./Pro/geometry/from_line/add_firstlastpoint))
* ライン データの交点にポイントを発生 ([ArcMap](./ArcMap/geometry/from_line/add_junctionpoint) / [Pro](./Pro/geometry/from_line/add_junctionpoint))
* ライン データの中点にポイントを発生 ([ArcMap](./ArcMap/geometry/from_line/add_midpoint) / [Pro](./Pro/geometry/from_line/add_midpoint))
* ライン データに指定した間隔でポイントを発生 ([ArcMap](./ArcMap/geometry/from_line/add_point_interval) / [Pro](./Pro/geometry/from_line/add_point_interval))
* ライン データの頂点にポイント データを発生 ([ArcMap](./ArcMap/geometry/from_line/vertextopoint) / [Pro](./Pro/geometry/from_line/vertextopoint))
* ポイントから凸包ポリゴンを作成 ([ArcMap](./ArcMap/geometry/from_point/create_convexhull) / [Pro](./Pro/geometry/from_point/create_convexhull))
* ポリゴンの枠線をラインとして出力 ([ArcMap](./ArcMap/geometry/from_polygon/polygon_to_line) / [Pro](./Pro/geometry/from_polygon/polygon_to_line))
* 現在の表示範囲にあるフィーチャを選択 ([ArcMap](./Desktop/mapping/select_by_extent))
* ポリゴンから内向きバッファ ポリゴンを発生 ([ArcMap](./Desktop/geometry/from_polygon/create_inside_buffer) / [Pro](./Pro/geometry/from_polygon/create_inside_buffer))
* フィーチャ サービス/フィーチャクラスから添付ファイルを一括でエクスポート ([Pro](./Pro/data_source/export_attachments))

## リソース

* [ArcMap ヘルプ](http://desktop.arcgis.com/ja/desktop/latest/analyze/arcpy/what-is-arcpy-.htm)
* [ArcGIS Pro ヘルプ](http://pro.arcgis.com/ja/pro-app/arcpy/main/arcgis-pro-arcpy-reference.htm)


## 免責事項

  * 本リポジトリで提供しているジオプロセシング ツールはサンプルとして提供しているものであり、動作に関する保証、および製品ライフサイクルに従った Esri 製品サポート サービスは提供しておりません。
  * ツールボックスに含まれるジオプロセシング ツールによって生じた損害等の一切の責任を負いかねますのでご了承ください。
  * 弊社で提供しているEsri 製品サポートサービスでは、本ツールに関しての Ｑ＆Ａ サポートの受付を行っておりませんので、予めご了承の上、ご利用ください。詳細は[
ESRIジャパン GitHub アカウントにおけるオープンソースへの貢献について](https://github.com/EsriJapan/contributing)をご参照ください。


## ライセンス
Copyright 2019 Esri Japan Corporation.

Apache License Version 2.0（「本ライセンス」）に基づいてライセンスされます。あなたがこのファイルを使用するためには、本ライセンスに従わなければなりません。
本ライセンスのコピーは下記の場所から入手できます。

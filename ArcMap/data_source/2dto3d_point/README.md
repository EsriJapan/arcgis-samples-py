# 2dto3d_point

指定したフィールドに格納されている数値を基に、2D ポイントから 3D ポイントに変換するサンプル

## 使用している製品

ArcGIS 10.3.x for Desktop

## パラメータ

* 入力ポイント データ   
* [出力ポイント データ  
* z 値が格納されているフィールド  

## 内容

入力ポイント データを [arcpy.CopyFeatures_management](http://desktop.arcgis.com/ja/desktop/latest/tools/data-management-toolbox/copy-features.htm)（フィーチャのコピー）関数を使用してコピーします。この際に、[arcpy.env.outputZFlag](http://desktop.arcgis.com/ja/desktop/latest/tools/environments/output-has-z-values.htm) を用いて z 値を有効化します。

データ アクセス モジュールの [UpdateCursor](http://desktop.arcgis.com/ja/desktop/latest/analyze/arcpy-data-access/updatecursor-class.htm) を使用し、指定したフィールドに格納されている数値を基に、個々のポイント フィーチャを 3D ポイントに更新します。

## ライセンス
Copyright 2015 Esri Japan Corporation.

Apache License Version 2.0（「本ライセンス」）に基づいてライセンスされます。あなたがこのファイルを使用するためには、本ライセンスに従わなければなりません。本ライセンスのコピーは下記の場所から入手できます。

> http://www.apache.org/licenses/LICENSE-2.0

適用される法律または書面での同意によって命じられない限り、本ライセンスに基づいて頒布されるソフトウェアは、明示黙示を問わず、いかなる保証も条件もなしに「現状のまま」頒布されます。本ライセンスでの権利と制限を規定した文言については、本ライセンスを参照してください。

ライセンスのコピーは本リポジトリの[ライセンス ファイル](./LICENSE)で利用可能です。

[](EsriJapan Tags: <タグ（半角スペース区切り）>)
[](EsriJapan Language: <開発言語>)


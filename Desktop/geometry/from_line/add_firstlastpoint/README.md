# add_firstlastpoint

ライン データの始点/終点にポイントを発生させるサンプル
  
  
<img src="..\..\..\..\_images/AddFisrtLastPoint.png" width="500">

## 使用している製品

ArcGIS 10.3.x for Desktop

## パラメータ

* 入力ライン データ   
* 出力ポイント データ  
* 出力形式（両端、始点、終点）
* シングル パートへの分割  

## 内容
### setup 関数
入力ライン データのスキーマ構造を持ったポイント データを[arcpy.CreateFeatureclass_management](http://desktop.arcgis.com/ja/desktop/latest/tools/data-management-toolbox/create-feature-class.htm)（フィーチャのコピー）関数を使用して作成します。また、GDB フィーチャクラスからシェープファイルへデータを移行する場合、以下の留意点があるため、その対処を行う。

* ID フィールドやShape_length、Shape_Area フィールドなど不必要なフィールドが付属するため、削除する。
* フィールド名の長さに制限があるため、出力されるShape ファイルのフィールド名は短くなることが考えられる。ただし、フィールドの順序は入力と変化しないため、インデックス番号で管理する。

### main 関数
データ アクセス モジュールの [SearchCursor](http://desktop.arcgis.com/ja/desktop/latest/analyze/arcpy-data-access/searchcursor-class.htm) を使用し、個々のライン フィーチャにアクセスします。ラインの始点と終点は、[polyline](http://desktop.arcgis.com/ja/desktop/latest/analyze/arcpy-classes/polyline.htm) クラスの firstPoint、lastPoint プロパティから取得します。次にデータ アクセス モジュールの [InsertCursor](http://desktop.arcgis.com/ja/desktop/latest/analyze/arcpy-data-access/insertcursor-class.htm) を使用し、ポイント フィーチャクラスに取得したポイント ジオメトリを挿入します。

## ライセンス
Copyright 2015 Esri Japan Corporation.

Apache License Version 2.0（「本ライセンス」）に基づいてライセンスされます。あなたがこのファイルを使用するためには、本ライセンスに従わなければなりません。本ライセンスのコピーは下記の場所から入手できます。

> http://www.apache.org/licenses/LICENSE-2.0

適用される法律または書面での同意によって命じられない限り、本ライセンスに基づいて頒布されるソフトウェアは、明示黙示を問わず、いかなる保証も条件もなしに「現状のまま」頒布されます。本ライセンスでの権利と制限を規定した文言については、本ライセンスを参照してください。

ライセンスのコピーは本リポジトリの[ライセンス ファイル](./LICENSE)で利用可能です。

[](EsriJapan Tags: <タグ（半角スペース区切り）>)
[](EsriJapan Language: <開発言語>)


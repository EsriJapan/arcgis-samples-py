# split_featureclass

指定したフィールドに格納されている属性値ごとにフィーチャクラスを分割するサンプル
  
  
<img src="..\..\..\_images\SplitFC.png" width="500">

## 使用している製品

ArcGIS 10.3.x for Desktop

## パラメータ

* 入力データ   
* 分割に使用するフィールド
* 出力ワークスペース  
* フィールドが文字列以外の場合は、接頭辞を指定

## 内容

データ アクセス モジュールの [SearchCursor](http://desktop.arcgis.com/ja/desktop/latest/analyze/arcpy-data-access/searchcursor-class.htm) を使用し、指定したフィールドに格納されている属性値のリストを作成します。リスト内に重複が出来ないように、今回は dictionary を用いています。

属性値のリストを用いて、 [arcpy.Select_analysis](http://desktop.arcgis.com/ja/desktop/latest/tools/analysis-toolbox/select.htm)（選択）関数をループ処理にて実行します。出力フィーチャクラス名として、属性値をそのまま使用します。属性値が文字列以外、または数値から始まる文字列の場合は、指定した接頭辞を付与したフィーチャクラス名となります。

## ライセンス
Copyright 2015 Esri Japan Corporation.

Apache License Version 2.0（「本ライセンス」）に基づいてライセンスされます。あなたがこのファイルを使用するためには、本ライセンスに従わなければなりません。本ライセンスのコピーは下記の場所から入手できます。

> http://www.apache.org/licenses/LICENSE-2.0

適用される法律または書面での同意によって命じられない限り、本ライセンスに基づいて頒布されるソフトウェアは、明示黙示を問わず、いかなる保証も条件もなしに「現状のまま」頒布されます。本ライセンスでの権利と制限を規定した文言については、本ライセンスを参照してください。

ライセンスのコピーは本リポジトリの[ライセンス ファイル](./LICENSE)で利用可能です。

[](EsriJapan Tags: <タグ（半角スペース区切り）>)
[](EsriJapan Language: <開発言語>)


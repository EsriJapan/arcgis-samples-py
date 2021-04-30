# export_attachments

フィーチャ サービス/フィーチャクラスから添付ファイルを一括でダウンロードするサンプル

## 動作確認環境

* ArcMap 10.8.1 (Basic ライセンス)

## パラメータ

* ArcGIS Online フィーチャ サービス
* ユーザー名
* パスワード
* フィーチャ サービスの URL
* レプリカを作成するレイヤーのインデックス番号
* 入力アタッチメント テーブル
* 添付ファイルを出力するフォルダー

## 内容

[ArcMap](https://desktop.arcgis.com/ja/arcmap/) では、[アタッチメント](https://desktop.arcgis.com/ja/arcmap/latest/manage-data/editing-attributes/enabling-attachments-on-a-feature-class.htm) (添付ファイル: 画像、PDF、テキスト文書、その他すべての種類のファイル) を[フィーチャクラス](https://www.esrij.com/gis-guide/arcgis-basic/feature-featureclass/)の各フィーチャに追加することができ、またエクスポートしてローカルに保存することもできます。なお、UI 上ではエクスポートは 1 つのフィーチャに対してのみしか行うことができないため、本ツールでは [ArcPy](https://pro.arcgis.com/ja/pro-app/latest/arcpy/get-started/what-is-arcpy-.htm) を使用してフィーチャクラスのすべてのフィーチャから添付ファイルを一括でエクスポートします。さらに、[ArcGIS REST API](https://developers.arcgis.com/rest/) を組み合わせて、[ArcGIS Online](https://www.esrij.com/products/arcgis-online/) に公開しているホスト フィーチャ サービスに対しても同様に、添付ファイルを一括でエクスポートします。

## 使用手順
* ArcGIS Online のフィーチャ サービスに対して処理を行う場合
  1. [ArcGIS Online フィーチャ サービス] パラメーターにチェックを入れます。
  2. [ユーザー名]、[パスワード] パラメーターに ArcGIS Online のアカウントのユーザー名とパスワードを設定します。
  3. [フィーチャ サービスの URL] パラメーターに添付ファイルをダウンロードしたい ArcGIS Online のフィーチャ サービスの URL を設定します。(例: https://services.arcgis.com/wlVTGRSYTzAbjjiC/arcgis/rest/services/sample_att/FeatureServer)
  4. [レプリカを作成するレイヤーのインデックス番号] パラメーターに添付ファイルをダウンロードしたいフィーチャ サービスのレイヤーのインデックス番号を指定します。(例: 0,1)
  5. [添付ファイルを出力するフォルダー] パラメーターに添付ファイルを出力したいフォルダーを設定します。(例: C:\Users\ej2190\Downloads)
* フィーチャクラスに対して処理を行う場合
  1. [ArcGIS Online フィーチャ サービス] パラメーターのチェックを外します。
  2. [入力アタッチメント テーブル] パラメーターに添付ファイルをダウンロードしたいアタッチメント テーブルを設定します。(例: サンプル__ATTACH)
  3. [添付ファイルを出力するフォルダー] パラメーターに添付ファイルを出力したいフォルダーを設定します。(例: C:\Users\ej2190\Downloads)

## 免責事項

  * 本リポジトリで提供しているジオプロセシング ツールはサンプルとして提供しているものであり、動作に関する保証、および製品ライフサイクルに従った Esri 製品サポート サービスは提供しておりません。
  * ツールボックスに含まれるジオプロセシング ツールによって生じた損害等の一切の責任を負いかねますのでご了承ください。
  * 弊社で提供しているEsri 製品サポートサービスでは、本ツールに関しての Ｑ＆Ａ サポートの受付を行っておりませんので、予めご了承の上、ご利用ください。詳細は[
ESRIジャパン GitHub アカウントにおけるオープンソースへの貢献について](https://github.com/EsriJapan/contributing)をご参照ください。

## ライセンス
Copyright 2019 Esri Japan Corporation.

Apache License Version 2.0（「本ライセンス」）に基づいてライセンスされます。あなたがこのファイルを使用するためには、本ライセンスに従わなければなりません。
本ライセンスのコピーは下記の場所から入手できます。
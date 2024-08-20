# メタデータスキーマ作成方法



## Python環境の準備

condaを利用する場合は、以下の手順でPython環境を構築します。

```
> conda create -n xafs-schema python=3.10
> conda activate xafs-schema
(xafs-schema)> pip install -r requirements.txt
```



## メタデータスキーマの作成手順

以下のコマンドで、指定したメタデータ管理用のエクセルファイルからメタデータスキーマファイル（jsonschema）を生成します。

```
(xafs-schema) >python gen_schema.py release/20230203/metadata_schema-xafs.xlsx
... input release/20230203/metadata_schema-xafs.xlsx
... output ./schema/xafs-schema.json
... output ./schema/xafs-schema-strict.json
```

* **xafs-schema.json**
  * `metadata_schema-xafs.xlsx` を基に生成された jsonschemaファイルです。 
  * データ型のチェックが緩めで、数値や文字列の区別がなく、空欄も許容されます。
  * データ型のチェックは緩くなっています。 (数値・文字列の区別なし、空欄もOK)
* **xafs-schema-strict.json**
  * 同様に、`metadata_schema-xafs.xlsx` を基に生成された jsonschemaファイルです。
  * データ型の厳格なチェックが行われます。
  * 信頼性の高いデータ（例: 標準試料データ）にはこちらのスキーマの使用を推奨します。



## XAFSメタデータスキーマのディレクトリ名

* **release/YYYYMMDD/**
  * 公開された正式版のXAFSメタデータスキーマが含まれます。
  * 例:
    * `release/20230203/xafs-schema.json`
    * `release/20230203/xafs-schema-strict.json`
* **draft/YYYYMMDD/**
  * ドラフト版のXAFSメタデータスキーマが含まれます。


# メタデータスキーマ作成方法



## Python環境構築

condaを利用した場合、以下の手順で行います。

```
> conda create -n xafs-schema python=3.10
> conda activate xafs-schema
(xafs-schema)> pip install -r requirements.txt
```



## メタデータスキーマ作成方法

下記のようにメタデータ管理のエクセルファイルを指定してメタデータスキーマファイル (jsonshema)を作成します。

```
(xafs-schema) >python gen_schema.py draft/20230127/metadata_schema-xafs.xlsx
... input draft/20230127/metadata_schema-xafs.xlsx
... output ./schema/xafs-schema.json
... output ./schema/xafs-schema-strict.json
```

* xafs-schema.json
  * metadata_schema-xafs.xls に従って作成された jsonschemaファイルです。 
  * データ型のチェックは緩くなっています。 (数値・文字列の区別なし、空欄もOK)
* xafs-schema-strict.json
  * 同様に、metadata_schema-xafs.xls に従って作成された jsonschemaファイルです。
  * データ型のチェックも行います。
  * 標準試料データなど信頼度の高いデータに対してはこちらのスキーマ利用を推奨します。


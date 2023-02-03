# xafs-schema


## 概要

日本XAFS研究会においてXAFSデータベースのメタデータ案について検討が進められています。

参考URL:  <https://www.jxafs.org/xafs-database/>

上記案に沿ってメタデータ記述を行っていくためには、メタデータ更新やバージョン管理、メタデータスキーマに沿ってメタデータが記述されているのかの確認、および、間違いがあった際の修正が柔軟にできること、がとても重要になります。

本プロジェクトではXAFSメタデータ管理、メタデータスキーマ作成、およびメタデータスキーマを用いたメタデータ確認についての資料をまとめています。

コメントなどありましたらmatumot@spring8.or.jpまでご連絡ください。



## メタデータ管理

さまざまなXAFSメタデータの追加・修正などを簡易に管理できるよう、エクセルファイルを用います。

XAFS.20230203でのエクセルファイルは[こちら](./draft/20230203/metadata_schema-xafs.xlsx)よりアクセスできます。(右側にある**download**ボタンよりダウンロード)

仕様はREADMEシートをご参照ください。各カテゴリのメタデータがそれぞれ定義され、簡易に管理できるようになっています。



## メタデータスキーマ作成

上記のメタデータ管理エクセルファイルよりメタデータスキーマ生成に用いるjsonschemaを作成します。

ユーザーはjsonschemaを利用するのみなので、下記情報は不要です。

* [メタデータスキーマ作成方法  (管理者向け)](./README_schema.md)



## メタデータスキーマ確認

メタデータスキーマ確認についてですが、以下に方法をそれぞれご紹介します。

- [Visual Studio Codeを用いた方法 (YAML)](./README_vscode.md)
- [Pythonを用いた方法 (YAML/Python)](./README_python.md)



## License

Apache License 2.0

## Author

Copyright (C) 2022 Takahiro Matsumoto (matumot@spring8.or.jp)

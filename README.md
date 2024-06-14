# discord-monitaring-server
サーバーの死活監視を行うBOTです
## 使い方
### 1. 必要なライブラリをインストールします<br>
`pip install -r requirements.txt`<br>
### 2. envファイルの作成
`.env.sample`を`.env`に書き換え、BOTのトークンを入れます。
### 3. コンフィグファイルの作成
`config.example.yaml`を`config.yaml`に書き換え、必要な情報を入れます。<br>
***channel_idは入れないと動作しません。***<br>
message_idは入れない場合、ステータス更新の度にメッセージが送信されます。
### 4. サーバーリストファイルの編集
コマンドでも手動でも編集できます。<br>
サーバーリストファイルは、BOT起動時に自動的に作成されます。<br>
### 手動の場合
`サーバー名,IPアドレス`<br>
のようにデータを入力します。
### コマンドの場合
サーバー追加: `!server_add <サーバー名> <IPアドレス>`<br>
サーバー削除: `!server_remove <サーバー名> <IPアドレス>`

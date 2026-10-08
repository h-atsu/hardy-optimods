# 検証用 GCE

Terraform で検証用の GCE インスタンスを作成し、IAP 経由で SSH または VS Code Remote - SSH から接続します。

このドキュメント内の `YOUR_GCP_PROJECT_ID`、`YOUR_OS_LOGIN_USER` などはプレースホルダーです。実際の値へ置き換えてください。実際のプロジェクト ID、アカウント、鍵などは Git にコミットしないでください。

## 作成されるもの

- Debian 12 の GCE インスタンス（既定: `e2-medium`）
- 専用 VPC とサブネット
- IAP 経由の SSH だけを許可するファイアウォールルール
- VM 専用のサービスアカウント（プロジェクト IAM ロールなし）
- Compute Engine、IAM、IAP、OS Login API の有効化

VM は OS Login と Shielded VM を有効にしています。外部 IP は既定で付与されますが、SSH の受信元は IAP の範囲だけです。

## 1. 前提ツール

ローカル環境に以下をインストールします。

- Terraform 1.8 以上
- Google Cloud CLI（`gcloud`）
- Visual Studio Code
- VS Code 拡張機能 [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)

## 2. Google Cloud の認証

Google Cloud CLI と Terraform 用の認証を設定します。

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_GCP_PROJECT_ID
```

プロジェクト ID が不明な場合は次のコマンドで確認できます。

```bash
gcloud projects list
```

表示名ではなく、`PROJECT_ID` 列の値を使用してください。

Terraform を実行するユーザーには、対象プロジェクトで API、ネットワーク、Compute Engine、サービスアカウントを作成できる権限が必要です。

接続するユーザーには少なくとも以下の権限が必要です。

- IAP TCP 転送: `roles/iap.tunnelResourceAccessor`
- OS Login: `roles/compute.osLogin`
- `sudo` を使う場合: `roles/compute.osAdminLogin`

環境の IAM 設定によっては、Compute Engine の参照権限や VM に設定したサービスアカウントを使用する権限も必要です。

## 3. Terraform 変数の設定

サンプルをコピーします。

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
```

`terraform.tfvars` の `project_id` を実際の値へ変更します。

```hcl
project_id = "YOUR_GCP_PROJECT_ID"
```

VS Code Server と開発ツールを動かす場合、メモリ 1 GB の `e2-micro` では応答が不安定になることがあります。VS Code を使用する検証環境では `e2-medium`（メモリ 4 GB）を推奨します。

```hcl
project_id   = "YOUR_GCP_PROJECT_ID"
machine_type = "e2-medium"
```

`terraform.tfvars` は `.gitignore` の対象です。実際の環境情報を `terraform.tfvars.example` へ書かないでください。

## 4. GCE の作成

```bash
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
```

`apply` が完了したら、作成結果を確認します。

```bash
terraform output
```

主な出力は以下です。

- `instance_name`: GCE インスタンス名
- `internal_ip`: 内部 IP
- `external_ip`: 外部 IP（無効化した場合は `null`）
- `iap_ssh_command`: IAP 経由の SSH コマンド

## 5. ターミナルから SSH 接続

Terraform が出力する接続コマンドを確認します。

```bash
terraform output -raw iap_ssh_command
```

表示例:

```bash
gcloud compute ssh hardy-optimods-sandbox \
  --project=YOUR_GCP_PROJECT_ID \
  --zone=asia-northeast1-b \
  --tunnel-through-iap
```

表示されたコマンドを実行します。初回接続では `~/.ssh/google_compute_engine` の SSH 鍵が作成される場合があります。鍵の作成やホスト鍵の確認プロンプトに従ってください。

接続を終了するには次を実行します。

```bash
exit
```

## 6. OS Login ユーザー名の確認

VS Code の SSH 設定には、OS Login の Linux ユーザー名が必要です。

```bash
gcloud compute os-login describe-profile \
  --project=YOUR_GCP_PROJECT_ID \
  --format='value(posixAccounts[0].username)'
```

出力例:

```text
YOUR_OS_LOGIN_USER
```

`gcloud compute ssh --dry-run` の出力を使う場合、末尾に表示される `YOUR_OS_LOGIN_USER@compute.NUMERIC_ID` 全体を SSH の `User` に設定しないでください。`User` に設定するのは `YOUR_OS_LOGIN_USER` の部分だけです。

## 7. SSH config の設定

まず `gcloud` の絶対パスを確認します。

```bash
command -v gcloud
```

`~/.ssh/config` に以下を追加します。`YOUR_GCP_PROJECT_ID`、`YOUR_OS_LOGIN_USER`、`/ABSOLUTE/PATH/TO/gcloud` を実際の値へ置き換えてください。

```sshconfig
Host hardy-optimods-sandbox
    HostName hardy-optimods-sandbox
    User YOUR_OS_LOGIN_USER
    IdentityFile ~/.ssh/google_compute_engine
    IdentitiesOnly yes
    ServerAliveInterval 30
    ServerAliveCountMax 3
    ProxyCommand /ABSOLUTE/PATH/TO/gcloud compute start-iap-tunnel %h %p --listen-on-stdin --project=YOUR_GCP_PROJECT_ID --zone=asia-northeast1-b --verbosity=warning
```

VS Code はシェルと異なる `PATH` で起動する場合があるため、`ProxyCommand` では `gcloud` の絶対パスを推奨します。

SSH config を使った接続を確認します。

```bash
ssh hardy-optimods-sandbox
```

ここで接続できない場合は、VS Code でも接続できません。先に SSH config、Google Cloud の認証、IAM 権限を確認してください。

## 8. VS Code から接続

1. VS Code でコマンドパレットを開きます。
2. `Remote-SSH: Connect to Host...` を実行します。
3. `hardy-optimods-sandbox` を選択します。
4. 初回に接続先 OS を聞かれた場合は `Linux` を選択します。
5. 接続後、`File: Open Folder...` からリモート上の作業ディレクトリを開きます。

画面左下に `SSH: hardy-optimods-sandbox` と表示されれば接続完了です。

## 9. トラブルシューティング

### `The project property must be set to a valid project ID`

`YOUR_GCP_PROJECT_ID` をそのまま使用していないか確認してください。実際のプロジェクト ID を設定します。

```bash
gcloud config set project YOUR_GCP_PROJECT_ID
```

### 鍵の入力後に認証が失敗する

まずターミナルから `terraform output -raw iap_ssh_command` で表示されるコマンドを実行してください。ターミナルで接続できる場合は、`~/.ssh/config` の `User` と `IdentityFile` を確認します。

秘密鍵がパスフレーズなしで作られているかは、次のコマンドで確認できます。

```bash
ssh-keygen -y -P '' -f ~/.ssh/google_compute_engine >/dev/null
```

終了コードが `0` なら、秘密鍵のパスフレーズは空です。

### `OfflineError` または `Connecting with SSH timed out`

次を確認してください。

1. `terraform.tfvars` の `machine_type` が `e2-medium` 以上になっていること
2. ターミナルから `ssh hardy-optimods-sandbox` が成功すること

ターミナルからの SSH は成功するものの、IAP トンネルの確立に 15 秒以上かかる場合に限り、VS Code の User Settingsへ次を追加してタイムアウトを延長します。

```json
{
  "remote.SSH.connectTimeout": 60
}
```

### `Waiting for port forwarding to be ready` のまま進まない

GCE の停止・再起動前に作られた古いポート転送を VS Code が保持している可能性があります。コマンドパレットから次を順に実行します。

1. `Remote-SSH: Kill Local Connection Server For Host...`
2. `Remote-SSH: Kill VS Code Server on Host...`
3. `Developer: Reload Window`

その後、`Remote-SSH: Connect to Host...` から再接続します。

同じ問題が繰り返される場合に限り、VS Code の User Settings へ以下を追加すると、古いローカル SSH トンネルの再利用を無効化できます。

```json
{
  "remote.SSH.useLocalServer": false
}
```

この設定は接続の再利用による高速化も無効にするため、通常は設定する必要がありません。

### Remote - SSH の詳細ログを確認する

VS Code のコマンドパレットで `Remote-SSH: Show Log` を実行します。以下の行の周辺を確認してください。

- `Authenticated to ...`: SSH 認証成功
- `Remote server is listening on port ...`: VS Code Server 起動成功
- `Socket closed`: SSH トンネルまたは古い接続キャッシュの問題
- `Permission denied`: OS Login、IAP、SSH 鍵、IAM 権限の問題

## 10. GCE の削除

検証が終わったら課金を止めるため、リソースを削除します。

```bash
cd infra
terraform destroy
```

Compute Engine などの API 自体は、他のリソースへの影響を避けるため `destroy` 時にも無効化しません。

## 補足

- `assign_external_ip = false` にすると外部 IP を付与しません。その場合も IAP SSH は利用できますが、VM からインターネットへ出るには Cloud NAT などが別途必要です。
- Terraform state はローカル保存です。共有運用する場合は GCS backend への移行を検討してください。
- VM のサービスアカウントには IAM ロールを付けていません。アプリから Google Cloud API を使う場合は、必要最小限のロールを追加してください。

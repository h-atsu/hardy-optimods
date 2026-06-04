# hardy-optimods backend

FastAPI + Celery + Redis based backend for optimization experiments.

## 現在の構成

- `mise`: Python / uv / Redis と開発タスクを管理
- `uv`: Python dependencies / virtualenv を管理
- `redis`: Celery broker / backend
- `sqlite`: API のデフォルト DB

Docker / devcontainer は使いません。

## セットアップ

```bash
mise install
mise run sync
```

## 一括起動

API / Celery worker / Redis / Flower / docs / Streamlit UI をまとめて起動します。

```bash
mise run dev
```

起動後は以下で確認できます。

- API: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8001`
- Flower: `http://127.0.0.1:5555`
- UI: `http://127.0.0.1:8501`

ログは `.local/logs` に出力されます。

## 個別起動

複数ターミナルで個別に起動する場合は、まず Redis を起動します。

```bash
mise run redis
```

別ターミナルで Celery worker を起動します。

```bash
mise run worker
```

別ターミナルで Flower を起動します。

```bash
mise run flower
```

起動後は `http://127.0.0.1:5555` で確認できます。

別ターミナルで API を起動します。

```bash
mise run api
```

別ターミナルで Zensical のドキュメントサイトを起動します。

```bash
mise run docs
```

起動後は `http://127.0.0.1:8001` で確認できます。

別ターミナルで Streamlit UI を起動します。

```bash
mise run ui
```

起動後は `http://127.0.0.1:8501` で確認できます。

## 動作確認

ジョブを投入します。

```bash
curl -X POST http://127.0.0.1:8000/bmi \
  -H "Content-Type: application/json" \
  -d '{"weight": 65, "height": 1.8}'
```

レスポンス例:

```json
{"id":"<task_id>"}
```

ステータスを確認します。

```bash
curl http://127.0.0.1:8000/bmi/<task_id>
```

完了後のレスポンス例:

```json
{"id":"<task_id>","status":"SUCCESS","result":20.061728395061728}
```

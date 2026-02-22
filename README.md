# hardy-optimods backend

FastAPI + Celery + Redis based backend for optimization experiments.

## 現在の構成（意図）

- `vscode`: 開発用コンテナ（FastAPI / Celery worker を手動起動）
- `redis`: Celery broker / backend

## devcontainer での動作確認手順

1. devcontainer を起動し、`vscode` / `redis` が立ち上がることを確認する
2. `vscode` コンテナ内で Celery worker を起動する

```bash
uv run celery --app hardy_optimods.tasks:celery worker --loglevel=info
```

3. 別ターミナルで Flower を起動する

```bash
uv run celery --app hardy_optimods.tasks:celery flower --port=5555
```

起動後は `http://127.0.0.1:5555` で確認できます。

4. 別ターミナルで API を起動する

```bash
uv run uvicorn hardy_optimods.server:app --host 0.0.0.0 --port 8000 --reload
```

5. 別ターミナルで Zensical のドキュメントサイトを起動する

```bash
uv run zensical serve -a 0.0.0.0:8001
```

起動後は `http://127.0.0.1:8001` で確認できます。

6. ジョブ投入

```bash
curl -X POST http://127.0.0.1:8000/bmi \
  -H "Content-Type: application/json" \
  -d '{"weight": 65, "height": 1.8}'
```

レスポンス例:

```json
{"id":"<task_id>"}
```

7. ステータス確認

```bash
curl http://127.0.0.1:8000/bmi/<task_id>
```

完了後のレスポンス例:

```json
{"id":"<task_id>","status":"SUCCESS","result":20.061728395061728}
```

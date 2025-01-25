import mlflow
from mlflow.tracking import MlflowClient

from consts import ROOT
from dataclass_schema import ConfigData
from executers import problem_name2executer


def run_exists(experiment_name: str, run_name: str) -> bool:
    """指定された実験名とrun名の組み合わせが既に存在するかチェック"""
    client = MlflowClient()

    # 実験の取得
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        return False

    # 実験内のrun一覧を取得
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string=f"tags.mlflow.runName = '{run_name}'",
    )

    return len(runs) > 0


def run_experiment(problem_name: str, model_name: str, timelimit: int):
    # MLflowの実験名を設定
    experiment_name = f"{problem_name}_comparison"
    mlflow.set_experiment(experiment_name)

    instance_file_paths = (ROOT / "data" / f"{problem_name}" / "instances").glob("*")
    for instance_file_path in instance_file_paths:
        run_name = f"{model_name}_{instance_file_path.name}_{timelimit}"

        # 既存のrunが存在する場合はスキップ
        if run_exists(experiment_name, run_name):
            print(f"Skip existing run: {run_name}")
            continue

        # MLflowで実行を追跡
        with mlflow.start_run(run_name=run_name):
            config = ConfigData(
                problem_name=problem_name,
                instance_file_name=instance_file_path.name,
                model_name=model_name,
                num_threads=-1,
                timelimit=timelimit,
            )

            executer = problem_name2executer[problem_name]
            output = executer(config)

            # メトリクスとパラメータを記録
            mlflow.log_params(
                {
                    "problem_name": problem_name,
                    "model_name": model_name,
                    "instance": instance_file_path.name,
                    "timelimit": timelimit,
                    "num_threads": -1,
                    "status": output.status.value,
                }
            )

            mlflow.log_metrics(
                {
                    "objective_value": output.objective_value,
                }
            )


if __name__ == "__main__":
    # TSPの実験を実行
    for model_name in ["mip", "cp"]:
        for timelimit in [20, 60]:
            run_experiment("tsp", model_name, timelimit)

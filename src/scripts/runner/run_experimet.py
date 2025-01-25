import mlflow

from consts import ROOT
from dataclass_schema import ConfigData
from executers import problem_name2executer


def run_experiment(problem_name: str, model_name: str, timelimit: int):
    # MLflowの実験名を設定
    mlflow.set_experiment(f"{problem_name}_comparison")

    instance_file_paths = (ROOT / "data" / f"{problem_name}" / "instances").glob("*")
    for instance_file_path in instance_file_paths:
        # MLflowで実行を追跡
        with mlflow.start_run(run_name=f"{model_name}_{instance_file_path.name}"):
            config = ConfigData(
                problem_name=problem_name,
                instance_file_name=instance_file_path.name,
                model_name=model_name,
                num_threads=-1,
                timelimit=timelimit,
            )

            # パラメータを記録
            mlflow.log_params(
                {
                    "problem_name": problem_name,
                    "model_name": model_name,
                    "instance": instance_file_path.name,
                    "timelimit": timelimit,
                    "num_threads": -1,
                }
            )

            executer = problem_name2executer[problem_name]
            output = executer(config)

            # メトリクスを記録（outputの形式に応じて適宜調整が必要）
            mlflow.log_metrics(
                {
                    "objective_value": output.objective_value,
                }
            )


if __name__ == "__main__":
    # 複数のソルバーで実験を実行
    for model_name in ["cp", "mip"]:  # 利用可能なソルバーを追加
        run_experiment("knapsack", model_name, 60)

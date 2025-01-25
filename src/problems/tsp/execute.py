from consts import SolutionStatus
from dataclass_schema import ConfigData, OutputData
from problems.tsp.evaluater import evaluate
from problems.tsp.make_input import make_input_data
from problems.tsp.models.model_factory import model_name2model_class


def execute(
    config_data: ConfigData,
) -> OutputData:  # [TODO] executeは全問題で共通化できる
    # 入力データの読み込み
    input_data = make_input_data(config_data.instance_file_path)

    # モデルの作成と求解
    model_class = model_name2model_class[config_data.model_name]
    model = model_class(input_data, config_data)
    status = model.solve()

    if status in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
        solution = model.get_solution()
        output_data = evaluate(solution, status, input_data)
    else:
        solution = None
        output_data = OutputData(
            objective_value=float("nan"),
            status=status,
            solution=None,
        )

    return output_data


if __name__ == "__main__":
    config_data = ConfigData(
        problem_name="tsp",
        instance_file_name="kroC100.tsp",
        model_name="cp",
        timelimit=30,
    )

    execute(config_data)

from dataclass_schema import ConfigData, OutputData
from knapsack.evaluater import evaluate
from knapsack.make_input import make_input_data
from knapsack.models.model_factory import model_name2model_class


def execute(config_data: ConfigData) -> OutputData:
    # 入力データの読み込み
    input_data = make_input_data(config_data.instance_file_path)

    # モデルの作成と求解
    model_class = model_name2model_class[config_data.model_name]
    model = model_class(input_data, config_data)
    status = model.solve()
    solution = model.get_solution()
    # 評価
    output_data = evaluate(solution, status, input_data)

    return output_data


if __name__ == "__main__":
    output_data = execute("data/knapsack/instances/instance_0.txt", timelimit=10)
    print(output_data)

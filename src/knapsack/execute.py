from knapsack.evaluater import evaluate
from knapsack.make_input import make_input_data
from knapsack.models.mip_model import MIPModel


def execute(input_file_path: str):
    # 入力データの読み込み
    input_data = make_input_data(input_file_path)

    # モデルの作成と求解
    model = MIPModel(input_data)
    solution = model.solve()

    # 評価
    output_data = evaluate(solution, input_data)

    return output_data


if __name__ == "__main__":
    output_data = execute("data/knapsack/instances/instance_0.txt")
    print(output_data)

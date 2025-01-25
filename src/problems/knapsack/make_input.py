from problems.knapsack.schema import InputData


def make_input_data(file_path: str) -> InputData:
    with open(file_path) as f:
        # 1行目から品物の数を読み込む
        n_items = int(f.readline().strip())
        # 2行目からナップサックの容量を読み込む
        capacity = int(f.readline().strip())

        # 3行目から重さのリストを読み込む
        weights = list(map(int, f.readline().strip().split()))
        # 4行目から価値のリストを読み込む
        values = list(map(int, f.readline().strip().split()))

    return InputData(n_items=n_items, capacity=capacity, weights=weights, values=values)

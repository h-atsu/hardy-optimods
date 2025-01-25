from knapsack.schema import InputData


def make_input_data(file_path: str) -> InputData:
    with open(file_path) as f:
        # map()の結果から最初の値を取得
        n_items = next(map(int, f.readline().split()))
        capacity = next(map(int, f.readline().split()))

        weights = list(map(int, f.readline().split()))
        values = list(map(int, f.readline().split()))

    return InputData(n_items=n_items, capacity=capacity, weights=weights, values=values)

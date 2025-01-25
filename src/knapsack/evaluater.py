from knapsack.schema import OutputData


def evaluate(solution, input_data) -> OutputData:
    """
    ナップサック問題の解を評価する関数

    Args:
        solution: 解（選択したアイテムのリスト）
        input_data: 入力データ（重さと価値の情報を含む）

    Returns:
        dict: 評価結果（総価値、使用重量など）
    """
    total_value = 0
    total_weight = 0

    for item_id in solution.selected_items:
        total_value += input_data.values[item_id]
        total_weight += input_data.weights[item_id]

    return {
        "total_value": total_value,
        "total_weight": total_weight,
        "selected_items": solution,
    }

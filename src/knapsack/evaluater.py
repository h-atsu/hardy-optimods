from consts import SolutionStatus
from dataclass_schema import OutputData
from knapsack.schema import InputData, SolutionData


def evaluate(
    solution: SolutionData, status: SolutionStatus, input_data: InputData
) -> OutputData:
    """
    ナップサック問題の解を評価する関数

    Args:
        solution: 解（選択したアイテムのリスト）
        input_data: 入力データ（重さと価値の情報を含む）

    Returns:
        dict: 評価結果（総価値、使用重量など）
    """
    total_value = 0

    for item_id in solution.selected_items:
        total_value += input_data.values[item_id]

    return OutputData(
        objective_value=total_value, status=status.value, solution=solution
    )

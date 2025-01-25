import numpy as np

from consts import SolutionStatus
from dataclass_schema import OutputData
from problems.tsp.schema import InputData, SolutionData


def calculate_total_distance(
    route: list[int], coordinates: list[tuple[float, float]]
) -> float:
    """巡回路の総距離を計算する"""
    total_distance = 0.0
    n = len(route)

    for i in range(n):
        from_city = route[i]
        to_city = route[(i + 1) % n]
        x1, y1 = coordinates[from_city]
        x2, y2 = coordinates[to_city]
        distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        total_distance += distance

    return total_distance


def evaluate(
    solution: SolutionData, status: SolutionStatus, input_data: InputData
) -> OutputData:
    """解の評価を行う

    Args:
        solution: 解
        status: 求解状態
        input_data: 入力データ

    Returns:
        OutputData: 評価結果
    """
    total_distance = calculate_total_distance(solution.route, input_data.coordinates)

    return OutputData(
        objective_value=total_distance, status=status.value, solution=solution
    )

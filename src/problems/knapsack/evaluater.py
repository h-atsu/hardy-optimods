from consts import SolutionStatus
from dataclass_schema import OutputData
from problems.knapsack.schema import InputData, SolutionData


def evaluate(
    solution: SolutionData, status: SolutionStatus, input_data: InputData
) -> OutputData:
    total_value = 0

    for item_id in solution.selected_items:
        total_value += input_data.values[item_id]

    return OutputData(
        objective_value=total_value, status=status.value, solution=solution
    )

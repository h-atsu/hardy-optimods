import pathlib
from enum import Enum

# プロジェクトルート
ROOT = pathlib.Path(__file__).parent.parent


class SolutionStatus(Enum):
    UNKNOWN = "Unknown"
    FEASIBLE = "Feasible"
    INFEASIBLE = "Infeasible"
    OPTIMAL = "Optimal"

    def __str__(self) -> str:
        return self.value

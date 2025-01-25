from mip import BINARY, Model, OptimizationStatus, maximize, xsum

from consts import SolutionStatus
from dataclass_schema import ConfigData
from knapsack.schema import InputData, SolutionData
from solver_base import SolverBase


class MIPModel(SolverBase):
    def __init__(self, input_data: InputData, config_data: ConfigData):
        self.input_data = input_data
        self.config_data = config_data
        self.model = Model()
        self._x = None
        self._status = None

    def solve(self) -> SolutionStatus:
        # 変数の定義
        self._x = [
            self.model.add_var(name=f"x_{i}", var_type=BINARY)
            for i in range(self.input_data.n_items)
        ]

        # 容量制約
        self.model.add_constr(
            xsum(
                self._x[i] * self.input_data.weights[i]
                for i in range(self.input_data.n_items)
            )
            <= self.input_data.capacity
        )

        # 目的関数：選択した荷物の価値の合計を最大化
        self.model.objective = maximize(
            xsum(
                self._x[i] * self.input_data.values[i]
                for i in range(self.input_data.n_items)
            )
        )

        # 求解
        status = self.model.optimize(
            max_seconds=self.config_data.timelimit,
        )
        self._status = status

        if status == OptimizationStatus.OPTIMAL:
            return SolutionStatus.OPTIMAL
        elif status == OptimizationStatus.FEASIBLE:
            return SolutionStatus.FEASIBLE
        else:
            return SolutionStatus.UNKNOWN

    def get_solution(self) -> SolutionData:
        selected_items = []
        if (
            self._status == OptimizationStatus.OPTIMAL
            or self._status == OptimizationStatus.FEASIBLE
        ):
            for i in range(self.input_data.n_items):
                if (
                    self._x[i].x >= 0.5
                ):  # バイナリ変数の場合、数値誤差を考慮して0.5以上を1とみなす
                    selected_items.append(i)

        return SolutionData(selected_items=selected_items)

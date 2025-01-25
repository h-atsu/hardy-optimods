from ortools.sat.python import cp_model

from consts import SolutionStatus
from dataclass_schema import ConfigData
from knapsack.schema import InputData, SolutionData
from solver_base import SolverBase


class CPModel(SolverBase):
    def __init__(self, input_data: InputData, config_data: ConfigData):
        self.input_data = input_data
        self.config_data = config_data
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self._x = None
        self._status = None

    def solve(self) -> SolutionStatus:
        # 変数の定義
        self._x = [
            self.model.NewBoolVar(f"x_{i}") for i in range(self.input_data.n_items)
        ]

        # 容量制約
        self.model.Add(
            sum(
                self._x[i] * self.input_data.weights[i]
                for i in range(self.input_data.n_items)
            )
            <= self.input_data.capacity
        )

        # 目的関数：選択した荷物の価値の合計を最大化
        self.model.Maximize(
            sum(
                self._x[i] * self.input_data.values[i]
                for i in range(self.input_data.n_items)
            )
        )

        # 求解
        self.solver.parameters.max_time_in_seconds = self.config_data.timelimit
        self.solver.parameters.log_search_progress = True
        status = self.solver.Solve(self.model)
        self._status = status

        if status == cp_model.OPTIMAL:
            return SolutionStatus.OPTIMAL
        elif status == cp_model.FEASIBLE:
            return SolutionStatus.FEASIBLE
        else:
            return SolutionStatus.UNKNOWN

    def get_solution(self) -> SolutionData:
        selected_items = []
        if self._status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            for i in range(self.input_data.n_items):
                if self.solver.Value(self._x[i]) == 1:
                    selected_items.append(i)

        return SolutionData(selected_items=selected_items)

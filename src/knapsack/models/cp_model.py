from ortools.sat.python import cp_model

from knapsack.schema import InputData, SolutionData
from solver_base import SolverBase


class CPModel(SolverBase):
    def __init__(self, input_data: InputData):
        self.input_data = input_data
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

    def solve(self) -> SolutionData:
        # 変数の定義
        x = [self.model.NewBoolVar(f"x_{i}") for i in range(self.input_data.n_items)]

        # 容量制約
        self.model.Add(
            sum(
                x[i] * self.input_data.weights[i]
                for i in range(self.input_data.n_items)
            )
            <= self.input_data.capacity
        )

        # 目的関数：選択した荷物の価値の合計を最大化
        self.model.Maximize(
            sum(
                x[i] * self.input_data.values[i] for i in range(self.input_data.n_items)
            )
        )

        # 求解
        status = self.solver.Solve(self.model)

        # 解の取得
        selected_items = []
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for i in range(self.input_data.n_items):
                if self.solver.Value(x[i]) == 1:
                    selected_items.append(i)

        return SolutionData(selected_items=selected_items)

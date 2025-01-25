from mip import BINARY, Model, OptimizationStatus, xsum

from knapsack.schema import InputData, SolutionData
from solver_base import SolverBase


class MIPModel(SolverBase):
    def __init__(self, input_data: InputData):
        self.input_data = input_data
        self.model = Model()

    def solve(self) -> SolutionData:
        # 変数の定義
        x = [
            self.model.add_var(name=f"x_{i}", var_type=BINARY)
            for i in range(self.input_data.n_items)
        ]

        # 容量制約
        self.model.add_constr(
            xsum(
                x[i] * self.input_data.weights[i]
                for i in range(self.input_data.n_items)
            )
            <= self.input_data.capacity
        )

        # 目的関数：選択した荷物の価値の合計を最大化
        self.model.objective = xsum(
            x[i] * self.input_data.values[i] for i in range(self.input_data.n_items)
        )
        self.model.sense = "MAX"

        # 求解
        status = self.model.optimize()

        # 解の取得
        selected_items = []
        if (
            status == OptimizationStatus.OPTIMAL
            or status == OptimizationStatus.FEASIBLE
        ):
            for i in range(self.input_data.n_items):
                if (
                    x[i].x >= 0.5
                ):  # バイナリ変数の場合、数値誤差を考慮して0.5以上を1とみなす
                    selected_items.append(i)

        return SolutionData(selected_items=selected_items)

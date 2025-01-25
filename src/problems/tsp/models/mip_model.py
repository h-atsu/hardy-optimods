import numpy as np
from mip import BINARY, Model, OptimizationStatus, xsum

from consts import SolutionStatus
from dataclass_schema import ConfigData
from problems.tsp.schema import InputData, SolutionData
from solver_base import SolverBase


class MIPModel(SolverBase):
    def __init__(self, input_data: InputData, config_data: ConfigData):
        self.input_data = input_data
        self.config_data = config_data
        self.model = Model()
        self._x = None
        self._status = None

    def _create_distance_matrix(self) -> np.ndarray:
        """座標からユークリッド距離行列を計算する"""
        n = self.input_data.dimension
        dist_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    x1, y1 = self.input_data.coordinates[i]
                    x2, y2 = self.input_data.coordinates[j]
                    dist_matrix[i][j] = int(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
        return dist_matrix

    def solve(self) -> SolutionStatus:
        n = self.input_data.dimension
        dist_matrix = self._create_distance_matrix()

        # スレッド数の設定
        if self.config_data.num_threads > 0:
            self.model.threads = self.config_data.num_threads

        # 変数: x[i,j] = 都市iから都市jへの移動があれば1
        self._x = {
            (i, j): self.model.add_var(name=f"x_{i}_{j}", var_type=BINARY)
            for i in range(n)
            for j in range(n)
            if i != j
        }

        # 制約: 各都市から1つの都市へ出る
        for i in range(n):
            self.model.add_constr(
                xsum(self._x[i, j] for j in range(n) if j != i) == 1,
                name=f"out_{i}",
            )

        # 制約: 各都市へ1つの都市から入る
        for j in range(n):
            self.model.add_constr(
                xsum(self._x[i, j] for i in range(n) if i != j) == 1,
                name=f"in_{j}",
            )

        # 制約: 部分巡回路の除去（MTZ制約）
        u = {i: self.model.add_var(name=f"u_{i}", lb=0, ub=n - 1) for i in range(n)}
        for i in range(1, n):
            for j in range(1, n):
                if i != j:
                    self.model.add_constr(
                        u[i] - u[j] + n * self._x[i, j] <= n - 1,
                        name=f"mtz_{i}_{j}",
                    )

        # 目的関数: 総移動距離の最小化
        self.model.objective = xsum(
            dist_matrix[i][j] * self._x[i, j]
            for i in range(n)
            for j in range(n)
            if i != j
        )

        # 問題を解く
        self._status = self.model.optimize(max_seconds=self.config_data.timelimit)

        if self._status == OptimizationStatus.OPTIMAL:
            return SolutionStatus.OPTIMAL
        elif self._status == OptimizationStatus.FEASIBLE:
            return SolutionStatus.FEASIBLE
        else:
            return SolutionStatus.UNKNOWN

    def get_solution(self) -> SolutionData:
        if self._status in [OptimizationStatus.OPTIMAL, OptimizationStatus.FEASIBLE]:
            n = self.input_data.dimension
            route = []
            current = 0  # 始点を0とする
            for _ in range(n):
                route.append(current)
                # 次の都市を探す
                for j in range(n):
                    if j != current and self._x[current, j].x >= 0.5:
                        current = j
                        break
            return SolutionData(route=route)
        return SolutionData(route=[])

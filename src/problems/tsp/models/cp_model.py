import numpy as np
from ortools.sat.python import cp_model

from consts import SolutionStatus
from dataclass_schema import ConfigData
from problems.tsp.schema import InputData, SolutionData
from solver_base import SolverBase


class CPModel(SolverBase):
    def __init__(self, input_data: InputData, config_data: ConfigData):
        self.input_data = input_data
        self.config_data = config_data
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self._edge_vars = None
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

        # 各辺に対する変数を作成
        self._edge_vars = {}
        edges = []
        for i in range(n):
            for j in range(n):
                if i != j:
                    # 辺(i,j)を使用するかどうかのブール変数
                    var = self.model.NewBoolVar(f"x_{i}_{j}")
                    self._edge_vars[i, j] = var
                    edges.append((i, j, var))

        # 巡回路制約：各都市を1度だけ訪問する
        self.model.AddCircuit(edges)

        # 目的関数：総移動距離の最小化
        self.model.Minimize(
            sum(
                dist_matrix[i][j] * self._edge_vars[i, j]
                for i in range(n)
                for j in range(n)
                if i != j
            )
        )

        # ソルバーの設定と実行
        self.solver.parameters.max_time_in_seconds = self.config_data.timelimit
        self.solver.parameters.log_search_progress = True
        self._status = self.solver.Solve(self.model)

        if self._status == cp_model.OPTIMAL:
            return SolutionStatus.OPTIMAL
        elif self._status == cp_model.FEASIBLE:
            return SolutionStatus.FEASIBLE
        else:
            return SolutionStatus.UNKNOWN

    def get_solution(self) -> SolutionData:
        if self._status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            # 解から巡回路を構築
            n = self.input_data.dimension
            route = []
            current = 0  # 始点を0とする
            for _ in range(n):
                route.append(current)
                # 次の都市を探す
                for j in range(n):
                    if j != current and self.solver.Value(self._edge_vars[current, j]):
                        current = j
                        break
            return SolutionData(route=route)
        return SolutionData(route=[])

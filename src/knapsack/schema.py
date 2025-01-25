from dataclass_schema import BaseInputData, BaseSolutionData


class InputData(BaseInputData):
    n_items: int  # 荷物の数
    capacity: int  # ナップサックの容量
    weights: list[int]  # 各荷物の重さ
    values: list[int]  # 各荷物の価値


class SolutionData(BaseSolutionData):
    selected_items: list[int]  # 選択された荷物のインデックス

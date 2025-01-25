from pydantic import BaseModel


class InputData(BaseModel):
    n_items: int  # 荷物の数
    capacity: int  # ナップサックの容量
    weights: list[int]  # 各荷物の重さ
    values: list[int]  # 各荷物の価値


class SolutionData(BaseModel):
    selected_items: list[int]  # 選択された荷物のインデックス


class OutputData(BaseModel):
    total_value: int  # 総価値
    total_weight: int  # 総重量
    selected_items: list[int]  # 選択された荷物のインデックス

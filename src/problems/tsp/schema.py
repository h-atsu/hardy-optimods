from dataclass_schema import BaseInputData, BaseSolutionData


class InputData(BaseInputData):
    name: str  # 問題名
    dimension: int  # 都市の数
    coordinates: list[tuple[float, float]]  # 各都市の座標


class SolutionData(BaseSolutionData):
    route: list[int]  # 巡回路（都市の訪問順序）

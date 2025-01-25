from pydantic import BaseModel


class InputData(BaseModel):
    N: int
    M: int
    H: int
    A: list[int]
    to: list[list[int]]
    cord: list[tuple[int, int]]


class SolutionData(BaseModel):
    pass


class OutputData(BaseModel):
    pass

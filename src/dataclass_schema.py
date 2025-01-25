from typing import Annotated

from pydantic import BaseModel

from consts import ROOT, SolutionStatus


class BaseInputData(BaseModel):
    pass


class BaseSolutionData(BaseModel):
    pass


class OutputData(BaseModel):
    objective_value: float
    status: SolutionStatus
    solution: BaseSolutionData | None


class ConfigData(BaseModel):
    problem_name: str
    instance_file_name: str
    model_name: str
    num_threads: int = -1
    timelimit: Annotated[int, "seconds"]

    @property
    def instance_file_path(self) -> str:
        return f"{ROOT}/data/{self.problem_name}/instances/{self.instance_file_name}"

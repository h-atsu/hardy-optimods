from typing import Annotated

from pydantic import BaseModel

from consts import ROOT


class BaseInputData(BaseModel):
    pass


class BaseSolutionData(BaseModel):
    pass


class OutputData(BaseModel):
    objective_value: int
    status: str
    solution: BaseSolutionData


class ConfigData(BaseModel):
    problem_name: str
    instance_file_name: str
    model_name: str
    num_threads: int
    timelimit: Annotated[int, "seconds"]

    @property
    def instance_file_path(self) -> str:
        return f"{ROOT}/data/{self.problem_name}/instances/{self.instance_file_name}"

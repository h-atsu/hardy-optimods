import mip

from knapsack.schema import InputData
from solver_base import SolverBase


class CBCModel(SolverBase):
    def __init__(self, input_data: InputData):
        self.input_data = input_data
        self.model = mip.Model()

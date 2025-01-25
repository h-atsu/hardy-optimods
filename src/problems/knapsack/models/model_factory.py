from problems.knapsack.models.cp_model import CPModel
from problems.knapsack.models.mip_model import MIPModel

model_name2model_class = {
    "mip": MIPModel,
    "cp": CPModel,
}

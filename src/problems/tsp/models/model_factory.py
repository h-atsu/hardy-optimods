from problems.tsp.models.cp_model import CPModel
from problems.tsp.models.mip_model import MIPModel

model_name2model_class = {
    "mip": MIPModel,
    "cp": CPModel,
}

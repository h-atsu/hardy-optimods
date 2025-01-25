from problems.knapsack.execute import execute as knapsack_execute
from problems.tsp.execute import execute as tsp_execute

problem_name2executer = {
    "knapsack": knapsack_execute,
    "tsp": tsp_execute,
}

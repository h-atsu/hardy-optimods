from config_schema import ConfigData
from consts import ROOT
from executers import problem_name2executer


def run_experiment(problem_name: str, model_name: str, timelimit: int):
    instance_file_paths = (ROOT / "data" / f"{problem_name}" / "instances").glob("*")
    for instance_file_path in instance_file_paths:
        config = ConfigData(
            problem_name=problem_name,
            instance_file_name=instance_file_path.name,
            model_name=model_name,
            num_threads=-1,
            timelimit=timelimit,
        )
        executer = problem_name2executer[problem_name]
        output = executer(config)

        print(output)


if __name__ == "__main__":
    for model_name in ["cp"]:
        run_experiment("knapsack", model_name, 60)

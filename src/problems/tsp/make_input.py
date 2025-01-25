from pathlib import Path

from problems.tsp.parser import parse_tsp_file
from problems.tsp.schema import InputData


def make_input_data(file_path: str | Path) -> InputData:
    """TSPファイルから入力データを生成する

    Args:
        file_path: TSPファイルのパス

    Returns:
        InputData: 入力データ
    """
    instance = parse_tsp_file(Path(file_path))
    return InputData(
        name=instance.name,
        dimension=instance.dimension,
        coordinates=instance.coordinates,
    )

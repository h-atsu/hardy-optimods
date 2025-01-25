from dataclasses import dataclass
from pathlib import Path


@dataclass
class TSPInstance:
    """TSP問題のインスタンスを表すデータクラス"""

    name: str
    dimension: int
    coordinates: list[tuple[float, float]]


def parse_tsp_file(file_path: Path) -> TSPInstance:
    """TSPファイルを解析してインスタンスを生成する

    Args:
        file_path: TSPファイルのパス

    Returns:
        TSPInstance: 解析されたTSPインスタンス
    """
    name = ""
    dimension = 0
    coordinates = []

    with open(file_path) as f:
        lines = f.readlines()

    reading_coords = False
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("NAME"):
            name = line.split(":")[1].strip()
        elif line.startswith("DIMENSION"):
            dimension = int(line.split(":")[1].strip())
        elif line == "NODE_COORD_SECTION":
            reading_coords = True
        elif line == "EOF":
            break
        elif reading_coords:
            # 座標データの行を解析
            parts = line.split()
            # インデックスは0から始めるため、-1する
            coordinates.append((float(parts[1]), float(parts[2])))

    return TSPInstance(name=name, dimension=dimension, coordinates=coordinates)

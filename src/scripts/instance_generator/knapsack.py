import json
import random
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from consts import ROOT


class KnapsackInstanceConfig(BaseModel):
    """ナップサック問題インスタンスの生成設定

    Attributes:
        n_items: アイテムの数
        min_weight: アイテムの最小重量
        max_weight: アイテムの最大重量
        min_value: アイテムの最小価値
        max_value: アイテムの最大価値
        capacity_ratio: キャパシティを総重量に対する比率
    """

    n_items: int
    min_weight: int
    max_weight: int
    min_value: int
    max_value: int
    capacity_ratio: float


def generate_instance(
    config: KnapsackInstanceConfig,
    seed: int,
) -> dict[str, Any]:
    """単一のナップサック問題インスタンスを生成

    Args:
        config: インスタンス生成の設定
        seed: 乱数シード

    Returns:
        生成されたインスタンスを表す辞書
    """
    random.seed(seed)

    weights = [
        random.randint(config.min_weight, config.max_weight)
        for _ in range(config.n_items)
    ]
    values = [
        random.randint(config.min_value, config.max_value)
        for _ in range(config.n_items)
    ]
    capacity = int(sum(weights) * config.capacity_ratio)

    return {
        "N": config.n_items,
        "capacity": capacity,
        "weights": weights,
        "values": values,
    }


def write_instance(instance: dict[str, Any], output_dir: Path) -> None:
    """インスタンスをJSONファイルとして保存

    Args:
        instance: 保存するインスタンス
        output_dir: 出力ディレクトリのパス
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"instance_{instance['N']}.json"

    with open(output_path, "w") as f:
        json.dump(instance, f, indent=2)


def generate_all_instances(
    configs: list[KnapsackInstanceConfig], n_instances_per_config: int, output_dir: Path
) -> None:
    """複数のインスタンスを生成して保存

    Args:
        configs: インスタンス生成設定のリスト
        n_instances_per_config: 各設定あたりのインスタンス数
        output_dir: 出力ディレクトリのパス
    """
    instance_no = 0
    for config in configs:
        for _ in range(n_instances_per_config):
            instance = generate_instance(
                config=config,
                seed=instance_no,
            )
            write_instance(instance, output_dir)
            instance_no += 1


def main() -> None:
    """メイン処理"""
    configs = [
        KnapsackInstanceConfig(
            n_items=50,
            min_weight=1,
            max_weight=100,
            min_value=1,
            max_value=100,
            capacity_ratio=0.5,
        ),
        KnapsackInstanceConfig(
            n_items=100,
            min_weight=1,
            max_weight=100,
            min_value=1,
            max_value=100,
            capacity_ratio=0.5,
        ),
    ]
    n_instances_per_config = 5
    output_dir = ROOT / "data" / "knapsack" / "instances"

    generate_all_instances(configs, n_instances_per_config, output_dir)


if __name__ == "__main__":
    main()

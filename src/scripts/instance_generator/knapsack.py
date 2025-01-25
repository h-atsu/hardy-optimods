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
        base_value_ratio: 価値/重さの基本比率
        value_noise_ratio: 価値のノイズ比率
        special_item_ratio: 特殊アイテムの割合
        capacity_ratio: キャパシティを総重量に対する比率
    """

    n_items: int
    min_weight: int
    max_weight: int
    base_value_ratio: float = 1.0  # 価値/重さの基本比率
    value_noise_ratio: float = 0.2  # 価値のノイズ比率
    special_item_ratio: float = 0.1  # 特殊アイテムの割合
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

    # 通常アイテムの生成（重さと価値に相関あり）
    n_normal_items = int(config.n_items * (1 - config.special_item_ratio))
    normal_items = []
    for _ in range(n_normal_items):
        weight = random.randint(config.min_weight, config.max_weight)
        # 基本価値に対してノイズを加える
        base_value = weight * config.base_value_ratio
        noise = random.uniform(
            -base_value * config.value_noise_ratio,
            base_value * config.value_noise_ratio,
        )
        value = int(base_value + noise)
        normal_items.append((weight, max(1, value)))  # 価値が0以下にならないように

    # 特殊アイテムの生成
    n_special_items = config.n_items - n_normal_items
    special_items = []
    for _ in range(n_special_items):
        item_type = random.random()
        if item_type < 0.4:  # 40%: 軽くて価値が高い
            weight = random.randint(
                config.min_weight, (config.min_weight + config.max_weight) // 3
            )
            value = random.randint(config.max_weight * 2, config.max_weight * 3)
        elif item_type < 0.8:  # 40%: 重くて価値が高い
            weight = random.randint(
                (config.min_weight + config.max_weight * 2) // 3, config.max_weight
            )
            value = random.randint(config.max_weight * 3, config.max_weight * 4)
        else:  # 20%: 中程度の重さで価値が非常に高い
            weight = random.randint(
                (config.min_weight + config.max_weight) // 3,
                (config.min_weight + config.max_weight * 2) // 3,
            )
            value = random.randint(config.max_weight * 4, config.max_weight * 5)
        special_items.append((weight, value))

    # 全アイテムをシャッフル
    all_items = normal_items + special_items
    random.shuffle(all_items)

    weights = [item[0] for item in all_items]
    values = [item[1] for item in all_items]

    # 容量を設定（総重量の一定割合）
    total_weight = sum(weights)
    capacity = int(total_weight * config.capacity_ratio)

    return {
        "N": config.n_items,
        "capacity": capacity,
        "weights": weights,
        "values": values,
    }


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
            output_path = output_dir / f"instance_{instance_no}.txt"

            with open(output_path, "w") as f:
                print(instance["N"], file=f)
                print(instance["capacity"], file=f)
                print(" ".join(map(str, instance["weights"])), file=f)
                print(" ".join(map(str, instance["values"])), file=f)

            instance_no += 1


def main() -> None:
    """メイン処理"""
    configs = [
        KnapsackInstanceConfig(
            n_items=5000,
            min_weight=1,
            max_weight=100,
            base_value_ratio=2.0,
            value_noise_ratio=0.3,
            special_item_ratio=0.1,
            capacity_ratio=0.3,
        ),
        KnapsackInstanceConfig(
            n_items=10000,
            min_weight=1,
            max_weight=100,
            base_value_ratio=2.0,
            value_noise_ratio=0.3,
            special_item_ratio=0.1,
            capacity_ratio=0.3,
        ),
    ]
    n_instances_per_config = 5
    output_dir = ROOT / "data" / "knapsack" / "instances"

    generate_all_instances(configs, n_instances_per_config, output_dir)


if __name__ == "__main__":
    main()

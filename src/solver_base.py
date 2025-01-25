from abc import ABC, abstractmethod


class SolverBase(ABC):
    @abstractmethod
    def solve(self):
        """
        問題を解くメソッド
        Returns:
            Dict[str, Any]: 計算結果（目的関数値、計算時間など）
        """
        pass

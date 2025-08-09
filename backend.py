"""
backend.py

Headless backend for Taixiu app.
Contains RootModel with persistence, stats, and Markov prediction.
"""

from __future__ import annotations
import json
import os
from collections import defaultdict
from typing import List, Optional, Tuple

class RootModel:
    """
    Backend model that holds history and provides saving/loading, statistics, and Markov prediction.

    History convention: newest result at index 0.
    Results are strings: 'TAI' or 'XIU'.
    """

    def __init__(self, data_dir: Optional[str] = None, filename: str = "taixiu_history.json", maxlen: int = 1000):
        if data_dir is None:
            data_dir = os.path.join(os.getcwd(), "taixiu_data")
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.data_file = os.path.join(self.data_dir, filename)
        self.maxlen = maxlen
        self.history: List[str] = []
        self.load_history()

    def load_history(self) -> None:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.history = data
        except Exception as e:
            print("[RootModel] load_history error:", e)

    def save_history(self) -> None:
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("[RootModel] save_history error:", e)

    def export_json(self, out_filename: str = "export_taixiu.json") -> str:
        out = os.path.join(self.data_dir, out_filename)
        try:
            with open(out, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return out
        except Exception as e:
            raise RuntimeError(f"Export failed: {e}")

    def add_result(self, res: str) -> None:
        res = res.strip().upper()
        if res not in ("TAI", "XIU"):
            raise ValueError("Result must be 'TAI' or 'XIU'")
        self.history.insert(0, res)
        if len(self.history) > self.maxlen:
            self.history = self.history[: self.maxlen]
        self.save_history()

    def clear_history(self) -> None:
        self.history = []
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
        except Exception:
            pass

    def longest_run(self, kind: str) -> int:
        kind = kind.upper()
        maxrun = 0
        cur = 0
        for x in reversed(self.history):
            if x == kind:
                cur += 1
                if cur > maxrun:
                    maxrun = cur
            else:
                cur = 0
        return maxrun

    def stats(self) -> dict:
        total = len(self.history)
        cnt_tai = sum(1 for x in self.history if x == "TAI")
        cnt_xiu = sum(1 for x in self.history if x == "XIU")
        return {
            "total": total,
            "cnt_tai": cnt_tai,
            "cnt_xiu": cnt_xiu,
            "pct_tai": (cnt_tai / total * 100) if total > 0 else 0.0,
            "pct_xiu": (cnt_xiu / total * 100) if total > 0 else 0.0,
            "longest_tai": self.longest_run("TAI") if total > 0 else 0,
            "longest_xiu": self.longest_run("XIU") if total > 0 else 0,
        }

    def predict_markov_probs(self) -> Optional[Tuple[float, float]]:
        if len(self.history) < 2:
            return None
        trans = defaultdict(lambda: defaultdict(int))
        for i in range(len(self.history) - 1, 0, -1):
            prev = self.history[i]
            nxt = self.history[i - 1]
            trans[prev][nxt] += 1
        last = self.history[0]
        counts = trans.get(last, {})
        total = sum(counts.values())
        if total == 0:
            cnt_tai = sum(1 for x in self.history if x == "TAI")
            cnt_xiu = sum(1 for x in self.history if x == "XIU")
            if len(self.history) == 0:
                return (0.5, 0.5)
            pt = cnt_tai / len(self.history)
            px = cnt_xiu / len(self.history)
            return (pt, px)
        p_tai = counts.get("TAI", 0) / total
        p_xiu = counts.get("XIU", 0) / total
        return (p_tai, p_xiu)

    def predict_markov_string(self) -> str:
        probs = self.predict_markov_probs()
        if probs is None:
            return "Chưa đủ dữ liệu để dự đoán"
        p_tai, p_xiu = probs
        return f"TÀI {p_tai*100:.1f}%  —  XỈU {p_xiu*100:.1f}%"

if __name__ == "__main__":
    print("backend.py: RootModel ready. Import from other scripts to use.")

from typing import List

import pandas as pd

from deproj.utils import LogMixin


class Box(LogMixin):

    def __init__(self, kind: str, *vals):
        self.kind = kind
        self.vals: List[dict] = [*vals]

    def to_df(self) -> pd.DataFrame:
        if self.kind == "basic":
            return pd.DataFrame(self.vals)
        elif self.kind == "frame":
            return pd.DataFrame({v["name"]: v["value"] for v in self.vals})
        else:
            raise NotImplementedError(f"to_df is not defined for kind {self.kind}")

    def to_dict(self):
        if self.kind == "basic":

            return {v.get("name") or i: v["value"] for i, v in enumerate(self.vals)}
        elif self.kind == "frame":
            return self.to_df().to_dict(orient='list')
        else:
            raise NotImplementedError(f"to_dict is not defined for kind {self.kind}")

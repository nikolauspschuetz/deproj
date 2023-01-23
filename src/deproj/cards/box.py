import os
from typing import List

import pandas as pd

from deproj.utils import LogMixin, get_output_filepath


class Box(LogMixin):
    def __init__(self, kind: str, side: str, *vals):
        self.kind = kind
        self.side = side
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
            return self.to_df().to_dict(orient="list")
        else:
            raise NotImplementedError(f"to_dict is not defined for kind {self.kind}")

    def to_csv(self):
        return self.to_df().to_csv(index=False)

    def write_csv(self, brand: str, year: int, name_slug: str, i: int):
        path_or_buf = get_output_filepath(brand, year, name_slug, "csv", i)
        os.makedirs(os.path.dirname(path_or_buf), exist_ok=True)
        if os.path.exists(path_or_buf):
            os.remove(path_or_buf)
        self.to_df().to_csv(path_or_buf=path_or_buf, index=False)
        return path_or_buf

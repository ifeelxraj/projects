from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CellEdits:
    trim: bool = False
    fill_empty: Optional[str] = None

    def apply(self, values):
        if self.trim:
            values = tuple(cell.strip() for cell in values)
        if self.fill_empty is not None:
            values = tuple(cell if cell else self.fill_empty for cell in values)
        return values

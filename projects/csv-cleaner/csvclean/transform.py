from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CellEdits:
    trim: bool = False
    fill_empty: Optional[str] = None

    skip_empty: bool = False

    def apply(self, values):
        if self.trim:
            values = tuple(cell.strip() for cell in values)
        if self.skip_empty and not any(values):
            return None
        if self.fill_empty is not None:
            values = tuple(cell if cell else self.fill_empty for cell in values)
        return values

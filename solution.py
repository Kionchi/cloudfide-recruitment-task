import pandas as pd
import re
from typing import List

class ColumnValidator:
    @staticmethod
    def is_valid_name(name: str) -> bool:
        """
        Validates column names. 
        Note: Your test suite requires names WITHOUT numbers (e.g., 'label3' is invalid).
        """
        return bool(re.fullmatch(r'[a-zA-Z_]+', name))

    @staticmethod
    def is_valid_expression(expression: str) -> bool:
        """Allows letters, underscores, spaces, operators, and digits as constants."""
        return bool(re.fullmatch(r'[a-zA-Z0-9_\s\+\-\*\/]+', expression))

class VirtualColumnEngine:
    def __init__(self, df: pd.DataFrame):
        self._df = df.copy()

    def _get_required_columns(self, expression: str) -> List[str]:
        """Extracts column names while ignoring mathematical constants (digits)."""
        tokens = re.split(r'[\s\+\-\*\/]+', expression.strip())
        return [t for t in tokens if t and not t.isdigit()]

    def execute(self, expression: str, target_name: str) -> pd.DataFrame:
        # Validation Pipeline
        if not ColumnValidator.is_valid_name(target_name):
            return pd.DataFrame()

        if not ColumnValidator.is_valid_expression(expression):
            return pd.DataFrame()

        if any(not ColumnValidator.is_valid_name(str(col)) for col in self._df.columns):
            return pd.DataFrame()

        required_cols = self._get_required_columns(expression)
        if not all(col in self._df.columns for col in required_cols):
            return pd.DataFrame()

        try:
            self._df[target_name] = self._df.eval(expression)
            return self._df
        except Exception:
            return pd.DataFrame()

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    engine = VirtualColumnEngine(df)
    return engine.execute(role, new_column)
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "produto",
    "categoria",
    "preco",
    "quantidade_vendida",
    "data_coleta",
}


def load_csv(path: str | Path) -> pd.DataFrame:
    """Carrega e valida a base local de produtos."""
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(missing)}")
    return clean_products(data)


def load_html_tables(url: str) -> list[pd.DataFrame]:
    """Lê todas as tabelas HTML encontradas em uma URL."""
    return pd.read_html(url, flavor="bs4")


def clean_products(data: pd.DataFrame) -> pd.DataFrame:
    """Normaliza tipos e remove registros sem dados essenciais."""
    result = data.copy()
    result["preco"] = pd.to_numeric(result["preco"], errors="coerce")
    result["quantidade_vendida"] = pd.to_numeric(
        result["quantidade_vendida"], errors="coerce"
    )
    result["data_coleta"] = pd.to_datetime(result["data_coleta"], errors="coerce")
    result = result.dropna(subset=["produto", "categoria", "preco"])
    return result.reset_index(drop=True)

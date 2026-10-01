import pandas as pd


def filter_by_price(data: pd.DataFrame, minimum: float, maximum: float) -> pd.DataFrame:
    """Retorna produtos dentro do intervalo de preço informado."""
    if minimum > maximum:
        raise ValueError("O preço mínimo não pode ser maior que o máximo.")
    return data[data["preco"].between(minimum, maximum)].copy()


def summarize(data: pd.DataFrame) -> dict[str, float | int | str]:
    """Calcula indicadores principais da base."""
    if data.empty:
        return {
            "preco_medio": 0.0,
            "menor_preco": 0.0,
            "maior_preco": 0.0,
            "total_vendido": 0,
            "produto_mais_caro": "-",
            "categoria_mais_vendida": "-",
            "ticket_medio": 0.0,
        }

    most_expensive = data.loc[data["preco"].idxmax(), "produto"]
    category_totals = sales_by_category(data)
    return {
        "preco_medio": float(data["preco"].mean()),
        "menor_preco": float(data["preco"].min()),
        "maior_preco": float(data["preco"].max()),
        "total_vendido": int(data["quantidade_vendida"].sum()),
        "produto_mais_caro": str(most_expensive),
        "categoria_mais_vendida": str(category_totals.iloc[0]["categoria"]),
        "ticket_medio": float(data["preco"].sum() / len(data)),
    }


def sales_by_category(data: pd.DataFrame) -> pd.DataFrame:
    """Agrupa a quantidade vendida por categoria."""
    return (
        data.groupby("categoria", as_index=False)["quantidade_vendida"]
        .sum()
        .sort_values("quantidade_vendida", ascending=False)
    )

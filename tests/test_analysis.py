import pandas as pd

from src.analysis import filter_by_price, sales_by_category, summarize
from src.data_loader import clean_products


def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "produto": ["A", "B"],
            "categoria": ["Casa", "Casa"],
            "preco": [10.0, 20.0],
            "quantidade_vendida": [2, 3],
            "data_coleta": pd.to_datetime(["2026-09-01", "2026-09-01"]),
        }
    )


def test_summarize_returns_expected_metrics():
    result = summarize(sample_data())
    assert result["preco_medio"] == 15.0
    assert result["menor_preco"] == 10.0
    assert result["maior_preco"] == 20.0
    assert result["total_vendido"] == 5
    assert result["produto_mais_caro"] == "B"
    assert result["categoria_mais_vendida"] == "Casa"
    assert result["ticket_medio"] == 15.0


def test_sales_by_category_groups_sales():
    result = sales_by_category(sample_data())
    assert result.iloc[0]["categoria"] == "Casa"
    assert result.iloc[0]["quantidade_vendida"] == 5


def test_summarize_handles_empty_data():
    result = summarize(pd.DataFrame())
    assert result == {
        "preco_medio": 0.0,
        "menor_preco": 0.0,
        "maior_preco": 0.0,
        "total_vendido": 0,
        "produto_mais_caro": "-",
        "categoria_mais_vendida": "-",
        "ticket_medio": 0.0,
    }


def test_clean_products_converts_types_and_removes_invalid_prices():
    data = pd.DataFrame(
        {
            "produto": ["Válido", "Inválido"],
            "categoria": ["Casa", "Casa"],
            "preco": ["12.50", "não informado"],
            "quantidade_vendida": ["3", "2"],
            "data_coleta": ["2026-09-01", "2026-09-01"],
        }
    )
    result = clean_products(data)
    assert len(result) == 1
    assert result.iloc[0]["preco"] == 12.5
    assert result.iloc[0]["quantidade_vendida"] == 3


def test_filter_by_price_returns_only_matching_products():
    result = filter_by_price(sample_data(), 15.0, 25.0)
    assert result["produto"].tolist() == ["B"]


def test_filter_by_price_rejects_inverted_range():
    try:
        filter_by_price(sample_data(), 30.0, 10.0)
    except ValueError:
        pass
    else:
        raise AssertionError("Faixa invertida deveria ser rejeitada")

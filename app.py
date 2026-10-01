from pathlib import Path

import plotly.express as px
import streamlit as st

from src.analysis import filter_by_price, sales_by_category, summarize
from src.data_loader import load_csv


BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "products.csv"

st.set_page_config(page_title="Dashboard de Produtos", page_icon="📊", layout="wide")
st.title("📊 Dashboard de Preços e Produtos")
st.caption("MVP de estudo com Python, Pandas, Plotly e Streamlit")

data = load_csv(DATA_PATH)
categories = ["Todas"] + sorted(data["categoria"].unique().tolist())
selected_category = st.sidebar.selectbox("Categoria", categories)
price_min = float(data["preco"].min())
price_max = float(data["preco"].max())
price_range = st.sidebar.slider(
    "Faixa de preço",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
)

if selected_category != "Todas":
    data = data[data["categoria"] == selected_category]
data = filter_by_price(data, *price_range)

metrics = summarize(data)
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Preço médio", f"R$ {metrics['preco_medio']:,.2f}")
col2.metric("Menor preço", f"R$ {metrics['menor_preco']:,.2f}")
col3.metric("Maior preço", f"R$ {metrics['maior_preco']:,.2f}")
col4.metric("Itens vendidos", f"{metrics['total_vendido']:,}")
col5.metric("Categoria líder", metrics["categoria_mais_vendida"])
col6.metric("Ticket médio", f"R$ {metrics['ticket_medio']:,.2f}")

st.subheader("Produtos")
st.dataframe(data, width="stretch", hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Preços por produto")
    price_chart = px.bar(data, x="produto", y="preco", color="categoria")
    st.plotly_chart(price_chart, width="stretch")

with right:
    st.subheader("Vendas por categoria")
    category_chart = px.pie(
        sales_by_category(data),
        names="categoria",
        values="quantidade_vendida",
        hole=0.35,
    )
    st.plotly_chart(category_chart, width="stretch")

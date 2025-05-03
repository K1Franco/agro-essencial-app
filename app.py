
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Agro Essencial - Simulador Agrícola", layout="centered", page_icon="🌾")

# Estilo azul escuro
st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa;}
    h1, h2, h3, .stButton>button {
        color: #0A3871;
    }
    .stButton>button {
        background-color: #0A3871;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Agro Essencial")
st.subheader("Simulador Inteligente de Rentabilidade Agrícola")

st.info("Preencha os dados abaixo para simular o desempenho financeiro de até 3 culturas.")

# Dados da fazenda
area_total = st.number_input("Área total (hectares)", min_value=1.0, value=100.0)
custos_fixos = st.number_input("Custos fixos totais (R$)", min_value=0.0, value=50000.0)

cenarios = {
    "Pessimista": 0.9,
    "Realista": 1.0,
    "Otimista": 1.1
}

def entrada_cultura(index):
    with st.expander(f"Cultura {index + 1}"):
        nome = st.text_input(f"Nome da Cultura {index + 1}", value=f"Cultura {index + 1}")
        custo_ha = st.number_input(f"Custo por hectare - {nome}", min_value=0.0, value=2500.0)
        produtividade = st.number_input(f"Produtividade esperada (sc/ha) - {nome}", min_value=0.0, value=60.0)
        preco = st.number_input(f"Preço por saca (R$) - {nome}", min_value=0.0, value=100.0)
        return {
            "nome": nome,
            "custo_ha": custo_ha,
            "produtividade": produtividade,
            "preco_unitario": preco
        }

culturas = [entrada_cultura(i) for i in range(3)]

if st.button("Simular Lucros"):
    resultados = []
    for cultura in culturas:
        for nome_cenario, fator in cenarios.items():
            receita = cultura["produtividade"] * fator * cultura["preco_unitario"] * area_total
            custo = cultura["custo_ha"] * area_total + custos_fixos
            lucro = receita - custo
            retorno_ha = lucro / area_total
            resultados.append({
                "Cultura": cultura["nome"],
                "Cenário": nome_cenario,
                "Receita Bruta": receita,
                "Custo Total": custo,
                "Lucro Líquido": lucro,
                "Retorno por hectare": retorno_ha
            })

    df = pd.DataFrame(resultados)
    st.subheader("Resultado da Simulação")
    st.dataframe(df)

    df_melhores = df[df["Cenário"] == "Realista"].sort_values(by="Lucro Líquido", ascending=False)
    melhor = df_melhores.iloc[0]
    st.success(f"A melhor escolha no cenário realista é **{melhor['Cultura']}**, com lucro estimado de R${melhor['Lucro Líquido']:,.2f}.")

    # Gráfico de comparação
    st.subheader("Comparação gráfica de Lucro por Cultura e Cenário")
    grafico = df.pivot(index="Cultura", columns="Cenário", values="Lucro Líquido")
    st.bar_chart(grafico)

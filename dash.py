import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
#python -m streamlit run dash.py
# Consulta no banco de dados
query = "SELECT * FROM tb_registro"

#Carregar os dados do MySQL
df = conexao(query)

# Botão para atualização dos dados
if st.button("Atualizar Dados"):   # o st apresenta diversas opções no dash, vamos usar o button
    df = conexao(query)

# MENU LATERAL

st.logo(image="Eco System Call logo.png", 
        icon_image="Eco System Call logo.png")
    
st.sidebar.header("Selecione a informação para gerar o gráfico") #título header e sub subheader

#Opção para selecionar qual sera o eixo x e y
#Seleção de colunas x
#barra lateral precisa incluir o sidebar para ficar na lateral, senão fica no meio
colunaX = st.sidebar.selectbox(
    "Eixo X",
    options=["umidade","temperatura","pressao","altitude", "co2", "poeira"],
    index=0 # vai indicar o primeiro item a partir da lista, neste caso será umidade, se fosse temperatura seria o index 1
) 

colunaY = st.sidebar.selectbox(
    "Eixo Y",
    options=["umidade","temperatura","pressao","altitude", "co2", "poeira"],
    index= 1 
)

# Verificar quais os atributo do filtro
def filtros(atributo):
    return atributo in [colunaX, colunaY]

#Filtro de Range -> SLIDER
st.sidebar.header("Selecione o Filtro")

#TEMPERATURA
if filtros("temperatura"): # checagem se a coluna x ou y foi chamada, isso é feito pelo item incluso dentro das ""
    temperatura_range = st.sidebar.slider(
        "Temperatura (ºC)",
        min_value=float(df["temperatura"].min()),   #indica o valor mínimo 
        max_value=float(df["temperatura"].max()),   #indica o valor máximo
        value=(float(df["temperatura"].min()), float(df["temperatura"].max())), #Faixa de valores selecionados
        step=0.1 #incremento para cada movimento do slider
    )

#UMIDADE


if filtros("umidade"):  # Checagem se a coluna x ou y foi chamada
    umidade_range = st.sidebar.slider(
        "Umidade (%)",
        min_value=float(df["umidade"].min()),  # Indica o valor mínimo
        max_value=float(df["umidade"].max()),  # Indica o valor máximo
        value=(float(df["umidade"].min()), float(df["umidade"].max())),  # Faixa de valores selecionados
        step=0.1  # Incremento para cada movimento do slider
    )


#ALTITUDE

if filtros("altitude"):
    altitude_range = st.sidebar.slider(
        "Altitude (m)",
        min_value=float(df["altitude"].min()),
        max_value=float(df["altitude"].max()),
        value=(float(df["altitude"].min()), float(df["altitude"].max()))
    )


#PRESSÃO
if filtros("pressao"): # checagem se a coluna x ou y foi chamada, isso é feito pelo item incluso dentro das ""
    pressao_range = st.sidebar.slider(
        "Pressao (p)",
        min_value=float(df["pressao"].min()),   #indica o valor mínimo 
        max_value=float(df["pressao"].max()),   #indica o valor máximo
        value=(float(df["pressao"].min()), float(df["pressao"].max())), #Faixa de valores selecionados
        step=0.1 #incremento para cada movimento do slider
    )


#CO2
if filtros("co2"): # checagem se a coluna x ou y foi chamada, isso é feito pelo item incluso dentro das ""
    co2_range = st.sidebar.slider(
        "CO2 (ppm)",
        min_value=float(df["co2"].min()),   #indica o valor mínimo 
        max_value=float(df["co2"].max()),   #indica o valor máximo
        value=(float(df["co2"].min()), float(df["co2"].max())), #Faixa de valores selecionados
        step=0.1 #incremento para cada movimento do slider
    )


#POEIRA
if filtros("poeira"): # checagem se a coluna x ou y foi chamada, isso é feito pelo item incluso dentro das ""
    poeira_range = st.sidebar.slider(
        "Poeira (p)",
        min_value=float(df["poeira"].min()),   #indica o valor mínimo 
        max_value=float(df["poeira"].max()),   #indica o valor máximo
        value=(float(df["poeira"].min()), float(df["poeira"].max())), #Faixa de valores selecionados
        step=0.1 #incremento para cada movimento do slider
    )

def_selecionado = df.copy()
#Cria uma cópia do df original

if filtros("temperatura"):
    def_selecionado = def_selecionado[
        (def_selecionado["temperatura"]>= temperatura_range[0]) &
        (def_selecionado["temperatura"] <= temperatura_range[1])
    ]

if filtros("umidade"):
    def_selecionado = def_selecionado[
        (def_selecionado["umidade"]>= umidade_range[0]) &
        (def_selecionado["umidade"] <= umidade_range[1])
    ]

if filtros("altitude"):
    def_selecionado = def_selecionado[
        (def_selecionado["altitude"]>= altitude_range[0]) &
        (def_selecionado["altitude"] <= altitude_range[1])
    ]

if filtros("pressao"):
    def_selecionado = def_selecionado[
        (def_selecionado["pressao"]>= pressao_range[0]) &
        (def_selecionado["pressao"] <= pressao_range[1])
    ]

if filtros("co2"):
    def_selecionado = def_selecionado[
        (def_selecionado["co2"]>= co2_range[0]) &
        (def_selecionado["co2"] <= co2_range[1])
    ]

if filtros("poeira"):
    def_selecionado = def_selecionado[
        (def_selecionado["poeira"]>= poeira_range[0]) &
        (def_selecionado["temperatura"] <= poeira_range[1])
    ]

# GRAFICOS
def Home():
    with st.expander("Tabela"):
        mostrarDados = st.multiselect(
            "Filtro",
            def_selecionado.columns,
            default=[],
            key="showData_home"
        )

        if mostrarDados:
            st.write(def_selecionado[mostrarDados])
#Calculos estatísticos
    if not def_selecionado.empty:
        media_umidade = def_selecionado["umidade"].mean()
        media_temperatura = def_selecionado["temperatura"].mean()
        media_co2 = def_selecionado["co2"].mean()

        media1, media2, media3 = st.columns(3, gap="large")
        
        with media1:
            st.info("Média de Registros de Umidade", icon="📌")
            st.metric(label="Média", value=f"{media_umidade:.2f}")

        with media2:
            st.info("Média de registros de temperatura", icon="📌")
            st.metric(label="Média", value=f"{media_temperatura:.2f}")

        with media3:
            st.info("Média de registros de CO2", icon="📌")
            st.metric(label="Média", value=f"{media_co2:.2f}")

            st.markdown("""----------""")

#GRÁFICOS
def graficos():
    st.title("Dashboard Monitoramento")
    #aba1= st.info("Gráfico de Linha")

    #aba1= st.tabs("Gráfico de Linha") quando for incluir mais um gráfico

    aba1, aba2 = st.tabs(["Gráfico de Linha", "Gráfico de Dispersão"])

    with aba1:
        if def_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar o gráfico")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return
        try:
            grupo_dados1 = def_selecionado.groupby(by=[colunaX]).size().reset_index(name="contagem")
            fig_valores = px.bar(
                grupo_dados1,
                x=colunaX,
                y="contagem", 
                orientation="h",
                title=f"Contagem de Registros por {colunaX.capitalize()}",
                color_discrete_sequence=["#0083b8"],
                template="plotly_white"
            )
        except Exception as e:
            st.error(f"Erro ao criar o gráfico de linha: {e}")

    st.plotly_chart(fig_valores, use_container_width=True)

# GRAFICO DE DISPERSÃO

    with aba2:
        st.write("Gráfico de Dispersão")
        grupo_dados2= def_selecionado.melt(id_vars=["pressao"], value_vars=["umidade"])

        fig_valores1 = px.scatter(grupo_dados2, x= "pressao", y="umidade",color="variable", title="<b>Dispersão de Valores por Marca</b>")

        st.plotly_chart(fig_valores1, use_container_width=True)

    

# Modelo



Home()
graficos()


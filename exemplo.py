#importar bibliotecas
import pandas as pd
import streamlit as st
import numpy as np

DATA_COLUMN = "date/time"
DATA_URL = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"

#Objeto Transformando dados
@st.cache
def load_data(nrows):
    data = pd.read_csv("https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data["date/time"] = pd.to_datetime(data["date/time"])

    return data

st.title("Como conseguir mais corridas com o Uber em New York utilizando Data Science!")
st.markdown("""

                    Nosso objetivo é conseguir mais "corridas" trabalhando com o app do Uber e 
                    consequentemente conseguir mais dinheiro, tudo isso com o auxilio do Data Science. 
                    Para isto pegamos a base de dados disponibilizados pelo Uber no site:

                    https://data.world/data-society/uber-pickups-in-nyc
            
                    Esta base de dados crua foi tratada da seguinte forma: 

                    - Renomeado os nomes das colunas de forma que todos os caracteres ficassem minúsculos 
                    - Transformado a coluna "date/time" em formato de data, pois ele seguia o padrão de objeto 
            
                    Com essa transformação a a base de dados ficou da seguinte forma:
            
""")

#Carregar Dados
data_load_state = st.text("Carregando dados...")
data = load_data(1028136)
data_load_state.text("Pronto! Carregado.")

#Chechbox para mostrar dados cru
if st.checkbox("Mostrar Row Data"):
    st.subheader("Row Data")
    st.write(data)

st.markdown("""

                Agora a partir desta transformação retiramos os seguintes insights: 

                A melhor forma de conseguir o maior número de corridas em New York é rodar na região 
                destacada entre os horários das 15h à 22h, tendo o maior pico de volume de pessoas 
                solicitando o Uber às 18h conforme identificamos nos gráficos abaixo:
            
""")

#Criando um gráfico de barras numero de corridas x horas do dia
st.subheader("Número de corridas por hora")
hist_values = np.histogram(data["date/time"].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)


#Criar filtros
hour_to_filter = st.slider("hour", 0, 23, 18)
filter_data = data[data[DATA_COLUMN].dt.hour == hour_to_filter]

st.subheader("Mapa para {}h".format(hour_to_filter))
st.map(filter_data)

st.markdown("""
            
            Este pico acontece devido a este horário haver um volume muito alto de pessoas 
            que saem do trabalho necessitam de transporte para voltar para casa e há pessoas 
            que vai e volta do happy hour e devido não poderem dirigir sobre efeito do álcool 
            recorrem ao aplicativo.
 
""")
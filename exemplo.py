#Utilizado a linguagem de programação Python
#Utilizado o PyCharm como IDE
#Importar bibliotecas
import streamlit as st
import pandas as pd
import altair as alt


#fonte de dados declarada em uma váriavel
DATA_URL = "https://raw.githubusercontent.com/carlosfab/curso_data_science_na_pratica/master/modulo_02/ocorrencias_aviacao.csv"

#Armazenando a base de dados em um cache
@st.cache

#Tratamento dos dados em uma função
def load_data():

    #renomear colunas
    columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'ocorrencia_uf': 'uf',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvias'
    }

    data = pd.read_csv(DATA_URL, index_col='codigo_ocorrencia')
    data = data.rename(columns=columns)

    #juntar a coluna data com hora
    data.data = data.data + " " + data.ocorrencia_horario
    data.data = pd.to_datetime(data.data)
    data = data[list(columns.values())]

    return data

df = load_data()

#declarar os valores que serão colocados no filtro em uma váriavel chamada labels
#os valores são da tabela classificacao renomeda na função anterior
labels = df.classificacao.unique().tolist()


# SIDEBAR
# Parâmetros e número de ocorrências
st.sidebar.header("Dados Selecionados")
info_sidebar = st.sidebar.empty()  # placeholder, para trazer informação baseadas no que será filtrado depois
# Slider de seleção do ano
#st.sidebar.subheader("Ano")
#year_to_filter = st.sidebar.slider('Escolha o ano desejado', 2008, 2018, 2017)

# Declarar a váriavel tabela que trará uma tabela filtrada ao usuário
st.sidebar.subheader("Tabela")
tabela = st.sidebar.empty()   # placeholder, para trazer informação baseadas no que será filtrado depois

# Multiselect (Permite multi seleção) com label que declarei na variavel labels anteriormente
label_to_filter = st.sidebar.multiselect(
    label="Escolha a classificação da ocorrência",
    options=labels,
    default=['ACIDENTE']
)

# Informação no rodapé da Sidebar
st.sidebar.markdown("""
A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de Investigação e Prevenção de Acidentes 
Aeronáuticos (CENIPA)***.
""")

# Somente aqui os dados filtrados por ano são atualizados em novo dataframe
filtered_df = df[(df.classificacao.isin(label_to_filter))]

# Aqui o placehoder vazio finalmente é atualizado com dados do filtered_df
info_sidebar.info("{} dados selecionadas.".format(filtered_df.shape[0]))

#Fim da SIDE BAR


# MAIN
st.title("Dashboard para monitorar Acidentes Aeronáuticos")

# Se o usuário clicar no checkbox mostrará a tabela com todos os dados filtrados
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(filtered_df)

st.markdown(f"""
        Está sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
        por Estado!
""")

#Gráfico de quantidades de ocorrência por estado
chart1 = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('uf', sort='-y'),
    y=alt.Y('count(uf)'),
    tooltip=['count(uf)', 'uf'],
)
#colocar rotulo de dados
text1 = chart1.mark_text(
    align='center',
    baseline='middle',
).encode(
    text=('count(uf)'),
)

st.altair_chart(chart1 + text1)

st.markdown(f"""
        Está sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
        por Tipo de Ocorrência!
""")

#Gráfico de quantidades de ocorrência por tipo de ocorrência
chart2 = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('count(tipo)'),
    y=alt.Y('tipo', sort='-x'),
    tooltip=['count(tipo)', 'tipo'],

)

#colocar rotulo de dados
text2 = chart2.mark_text(
    align='left',
    baseline='middle',
    dx=3
).encode(
    text=('count(tipo)'),
)

st.altair_chart(chart2 + text2)


st.markdown(f"""
        Está sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
        por ano!
""")


#Gráfico de quantidades de ocorrência por ano
chart3 = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('year(data)', sort='-y'),
    y=alt.Y('count(data)'),
    tooltip=['count(data)', 'year(data)'],
)

#colocar rotulo de dados
text3 = chart3.mark_text(
    align='left',
    baseline='middle',
).encode(
    text=('count(tipo)'),
)

st.altair_chart(chart3 + text3)

import os
from tokenize import String
import streamlit as st
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializar el analizador de sentimientos de nltk
sia = SentimentIntensityAnalyzer()

# Función para analizar el sentimiento
@st.cache_data
def analyze_sentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment['compound'], sentiment['neu']

def analyze_sentiment_dataset():
    df = st.session_state['df']
    # Inicializar la barra de progreso
    progress_bar = st.progress(0)
    total_rows = len(df)
    # Añadir columnas de polarity y neutrality con barra de progreso
    polarities = []
    neutralities = []
    for i, content in enumerate(df['content']):
        polarity, neutrality = analyze_sentiment(content)
        polarities.append(polarity)
        neutralities.append(neutrality)
        progress_bar.progress((i + 1) / total_rows)
    
    df['polaridad'] = polarities
    df['neutralidad'] = neutralities
    # Convertir polaridad y neutralidad a rangos descriptivos
    df['polaridad_desc'] = df['polaridad'].apply(convert_polarity)
    df['neutralidad_desc'] = df['neutralidad'].apply(convert_neutrality)

# Función para convertir polaridad a rango descriptivo
def convert_polarity(polarity):
    if polarity < -0.5:
        return 'Muy Negativo'
    elif -0.5 <= polarity < 0:
        return 'Negativo'
    elif 0 <= polarity < 0.5:
        return 'Positivo'
    else:
        return 'Muy Positivo'

# Función para convertir neutralidad (subjetividad) a rango descriptivo
def convert_neutrality(neutrality):
    if neutrality < 0.25:
        return 'Muy Poco Neutral'
    elif 0.25 <= neutrality < 0.5:
        return 'Poco Neutral'
    elif 0.5 <= neutrality < 0.75:
        return 'Neutral'
    else:
        return 'Muy Neutral'


def plot_sentiment_distribution(df):
    # Definir el orden de las categorías para polaridad y neutralidad
    polaridad_order = ["Muy Negativo", "Negativo", "Positivo", "Muy Positivo"]
    neutralidad_order = ["Muy Poco Neutral", "Poco Neutral", "Neutral", "Muy Neutral"]

    # Convertir las columnas a categorías ordenadas
    df['polaridad_desc'] = pd.Categorical(df['polaridad_desc'], categories=polaridad_order, ordered=True)
    df['neutralidad_desc'] = pd.Categorical(df['neutralidad_desc'], categories=neutralidad_order, ordered=True)

    # Contar la cantidad de tweets por cada categoría de polaridad
    polaridad_counts = df['polaridad_desc'].value_counts().reindex(polaridad_order).reset_index()
    polaridad_counts.columns = ['polaridad_desc', 'cantidad']

    # Contar la cantidad de tweets por cada categoría de neutralidad
    neutralidad_counts = df['neutralidad_desc'].value_counts().reindex(neutralidad_order).reset_index()
    neutralidad_counts.columns = ['neutralidad_desc', 'cantidad']

    fig, ax = plt.subplots(1, 2, figsize=(14, 7))

    sns.barplot(x='polaridad_desc', y='cantidad', data=polaridad_counts, ax=ax[0], palette='viridis')
    ax[0].set_title('Distribución de Polaridad')
    ax[0].set_xlabel('Polaridad')
    ax[0].set_ylabel('Cantidad de Tweets')

    sns.barplot(x='neutralidad_desc', y='cantidad', data=neutralidad_counts, ax=ax[1], palette='viridis')
    ax[1].set_title('Distribución de Neutralidad')
    ax[1].set_xlabel('Neutralidad')
    ax[1].set_ylabel('Cantidad de Tweets')

    plt.tight_layout()
    st.pyplot(fig)

def plot_entity_boxplot(df):
    plt.figure(figsize=(14, 7))
    sns.boxplot(x='entity', y='polaridad', data=df, palette='viridis')

    plt.title('Distribución de Polaridad por Entidad')
    plt.xlabel('Entidad')
    plt.ylabel('Polaridad')
    
    # Acortar los nombres de las entidades en el eje X
    ax = plt.gca()
    ax.set_xticklabels([label.get_text()[:15] for label in ax.get_xticklabels()], rotation=45, ha='right')

    plt.tight_layout()
    st.pyplot(plt)

def show_interesting_data(df):
    most_negative = df[df['polaridad'] == df['polaridad'].min()]['entity'].values[0]
    most_positive = df[df['polaridad'] == df['polaridad'].max()]['entity'].values[0]
    most_neutral_comments = df[df['neutralidad'] == df['neutralidad'].max()]['entity'].values[0]
    entity_most_comments = df['entity'].value_counts().idxmax()
    entity_least_comments = df['entity'].value_counts().idxmin()
    most_negative_comments_count = df[df['polaridad_desc'] == 'Muy Negativo']['entity'].value_counts().idxmax()
    most_positive_comments_count = df[df['polaridad_desc'] == 'Muy Positivo']['entity'].value_counts().idxmax()
    most_neutral_comments_count = df[df['neutralidad_desc'] == 'Muy Neutral']['entity'].value_counts().idxmax()
    highest_avg_polarity = df.groupby('entity')['polaridad'].mean().idxmax()
    lowest_avg_polarity = df.groupby('entity')['polaridad'].mean().idxmin()

    st.markdown("### Datos Interesantes:")
    col1, col2 = st.columns(2)

    with col1:
       st.markdown("**Entidad con más comentarios negativos**")
       st.info(f"**:red[{most_negative}]**", icon="❗")
       st.markdown("**Entidad con más comentarios positivos**")
       st.info(f"**:green[{most_positive}]**", icon="✅")
       st.markdown("**Entidad con más comentarios neutrales**")
       st.info(f"**:blue[{most_neutral_comments}]**", icon="ℹ️")
       st.markdown("**Entidad con más comentarios**")
       st.info(f"**:purple[{entity_most_comments}]**", icon="🔝")
       st.markdown("**Entidad con menos comentarios**")
       st.info(f"**:brown[{entity_least_comments}]**", icon="🔻")

    with col2:
        st.markdown("**Mayor cantidad de comentarios muy negativos**")
        st.info(f"**:red[{most_negative_comments_count}]**", icon= "❗")
        st.markdown("**Mayor cantidad de comentarios muy positivos**")
        st.info(f"**:green[{most_positive_comments_count}]**", icon="✅")
        st.markdown("**Mayor cantidad de comentarios muy neutrales**")
        st.info(f"**:blue[{most_neutral_comments_count}]**", icon="ℹ️")
        st.markdown("**Polaridad promedio más alta**")
        st.info(f"**:green[{highest_avg_polarity}]**", icon="📈")
        st.markdown("**Polaridad promedio más baja**")
        st.info(f"**:red[{lowest_avg_polarity}]**", icon="📉")


def vizualizacion(df):
    st.write("**Vista aleatoria del dataset:**")
    st.dataframe(df.sample(5))
    # Visualización general de la distribución de sentimientos
    st.subheader("Distribución General de Sentimientos")
    plot_sentiment_distribution(df)
    plot_entity_boxplot(df)

def cargar_datos():
    
    procesamiento = "Tweets con procesamiento previo"
    noProcesamiento = "Tweets sin procesamiento previo"
    propio = "Dataset propio"
    option = st.sidebar.selectbox(
    "**Seleccione con cual dataset desea trabajar**",
    (procesamiento, noProcesamiento, propio),
    index=None,
    placeholder="Selecciona el dataset...")
    uploaded_file = None
    if option == noProcesamiento:
        uploaded_file = "Final_Project\\data_frames\\twitter_training.csv"
    elif option == procesamiento:
        uploaded_file = "Final_Project\\data_frames\\twitter_comments_ready2go.csv"
    elif option == propio:
        uploaded_file = st.sidebar.file_uploader("**Suba el dataset en formato CSV**", type=["csv"])
        st.sidebar.info('*"El formato del dataset debe inlcuir una primera columna llamada **entity** y una segunda columna llamada **content**"*')

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if isinstance(uploaded_file, str):
            uploaded_file_name = uploaded_file.removeprefix('Final_Project\\data_frames\\')
        else:
            uploaded_file_name = uploaded_file.name
        st.session_state['name'] = uploaded_file_name
        if uploaded_file_name == 'twitter_training.csv':
            df.drop(columns=['2401'], inplace=True)
            df['entity'] = df['Borderlands']
            df.drop(columns=['Borderlands'], inplace=True)
            df['content'] = df['im getting on borderlands and i will murder you all ,']
            df.drop(columns=["im getting on borderlands and i will murder you all ,"], inplace=True)
            df['sentiment'] = df['Positive']
            df.drop(columns=["sentiment"], inplace=True)
            df.drop(columns=["Positive"], inplace=True)
            # Eliminar filas con valores nulos o cadenas vacías en la columna 'content'
            df = df.dropna(subset=['content'])
            df = df[df['content'].str.strip() != '']
            # Convertir valores numéricos a cadenas
            df = df.applymap(lambda x: str(x) if isinstance(x, (int, float)) else x)
            #df = df.iloc[:-69200]
        
        st.session_state['df'] = df  # Guardar datos en session_state
        return df
    return None

def main():
    st.set_page_config(
        page_title="Análisis Interactivo de Sentimientos de Tweets",
        layout="wide", #centered
        initial_sidebar_state="expanded",
    )

    user = os.getlogin()
    st.title(f"Hola *:green[{user}!]*")
    st.write(">#### Este es un análisis interactivo de los sentimientos de los tweets de usuarios sobre diferentes entidades y compañías")

    # Siempre mostrar los checkbox y cargar los datos si hay alguna selección
    df = cargar_datos()

    if df is not None:
        name = st.session_state['name']
        if name == 'twitter_training.csv':
            st.write('### Análisis de sentimientos')
            analyze_sentiment_dataset()
            vizualizacion(df)
        elif name == 'twitter_comments_ready2go.csv':
            vizualizacion(df)

        st.sidebar.markdown("---")
        if st.sidebar.button('Mostrar Datos Interesantes'):
            show_interesting_data(df)

        st.sidebar.write("---")
        entity = st.sidebar.selectbox("Selecciona una entidad para ver su análisis de sentimientos", ['Todas'] + list(df['entity'].unique()))
        if entity and entity != 'Todas':
            st.write(f"### Mostrando análisis de sentimientos para: {entity}")
            entity_df = df[df['entity'] == entity]
            plot_sentiment_distribution(entity_df)
            plot_entity_boxplot(entity_df)
        else:
            st.write("### Mostrando análisis de sentimientos para todas las entidades")
            plot_sentiment_distribution(df)
            plot_entity_boxplot(df)

if __name__ == "__main__":
    main()


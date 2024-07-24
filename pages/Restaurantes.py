#################### Bibliotecas e Módulos ####################
# Fazer os imports necessários
import numpy as np
import pandas as pd
from datetime import datetime
from haversine import haversine
from matplotlib import pyplot as plt
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image

# Importar função própria para tratamento dos dados
from tratamento import trata_df

#################### Leitura e Tratamento dos Dados ####################
# Ler os dados originais
dados_originais = pd.read_csv('dados.csv') 

# Tratar os dados originais com a função criada
dados = trata_df(dados_originais)

#################### Configurações da página do Streamlit ####################
st.set_page_config(page_title='Restaurantes', layout='wide', page_icon='🍽️')

#################### Título do Streamlit ####################
st.markdown('# Dashboard - Restaurantes')

#################### Barra lateral do Streamlit ####################
# Inserir o logo da empresa
image = Image.open('fast_delivery_logo.png')
st.sidebar.image(image, width=200)

# Criar o título e subtítulo da barra lateral
st.sidebar.markdown('# Fast Delivery')
st.sidebar.markdown('## The Quickest Delivery')
st.sidebar.markdown('---')

# Criar o filtro da distância da entrega
slider_distancia = st.sidebar.slider('Selecione uma distância da entrega limite (km):',
                                     value=21,
                                     min_value=1,
                                     max_value=21)

linhas_selecionadas = dados['distance_delivery_km'] <= slider_distancia
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro da cidade
filtro_cidade = st.sidebar.multiselect('Selecione as cidades:',
                                       ['Urban', 'Metropolitian', 'Semi-Urban'],
                                       default=['Urban', 'Metropolitian', 'Semi-Urban'])

linhas_selecionadas = dados['City'].isin(filtro_cidade)
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro do tipo de pedido
filtro_pedido = st.sidebar.multiselect('Selecione os tipos de pedido:',
                                       ['Snack', 'Drinks', 'Buffet', 'Meal'],
                                       default=['Snack', 'Drinks', 'Buffet', 'Meal'])

linhas_selecionadas = dados['Type_of_order'].isin(filtro_pedido)
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro da condição de trânsito
filtro_transito = st.sidebar.multiselect('Selecione as condições de trânsito:',
                                         ['Low', 'Medium', 'High', 'Jam'], 
                                         default=['Low', 'Medium', 'High', 'Jam'])

linhas_selecionadas = dados['Road_traffic_density'].isin(filtro_transito)
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro do tempo de entrega
slider_tempo_entrega = st.sidebar.slider('Selecione um tempo de entrega limite (minutos):',
                                         value=54,
                                         min_value=10,
                                         max_value=54)

linhas_selecionadas = dados['Time_taken(min)'] <= slider_tempo_entrega
dados = dados.loc[linhas_selecionadas, :]

#################### Layout do Streamlit ####################
# Criar e nomear as tabs (abas) 
tab_1, tab_2 = st.tabs(['Visão Transporte', 'Visão Velocidade'])

# Preencher a tab 1 (Visão Geográfica)
with tab_1:
  
  # Criar o gráfico da distribuição das distâncias de entrega
  with st.container():
    fig = px.box(dados, x='distance_delivery_km',
                 labels={
                   'distance_delivery_km': 'Distância até a entrega (km)'
                 },
                 title='Distribuição das Distâncias de Entrega')
    st.plotly_chart(fig, use_container_width=True)
    
  # Criar o gráfico da distribuição das distâncias de entrega por cidade 
  with st.container():
    fig = px.box(dados, x='City', y='distance_delivery_km',
                 labels={
                   'City': 'Cidade',
                   'distance_delivery_km': 'Distância até a entrega (km)'
                 },
                 title='Distribuição das Distâncias de Entrega por Cidade')
    st.plotly_chart(fig, use_container_width=True)
    
# Preencher a tab 2 (Visão Velocidade)   
with tab_2:
  
  # Criar o gráfico da distribuição dos tempos de entrega
  with st.container():
    fig = px.histogram(dados, x='Time_taken(min)', nbins=45,
                       labels={
                         'Time_taken(min)': 'Tempo de entrega (minutos)'
                       },
                     title='Distribuição dos Tempos de Entrega')
  st.plotly_chart(fig, use_container_width=True)
  
  # Criar o gráfico da distribuição dos tempos de entrega por cidade  
  with st.container():
    fig = px.box(dados, x='City', y='Time_taken(min)',
                 labels={
                   'City': 'Cidade',
                   'Time_taken(min)': 'Tempo de entrega (min)'
                 },
                 title='Distribuição dos Tempos de Entrega por Cidade')
    st.plotly_chart(fig, use_container_width=True)
    
  # Criar o gráfico da distribuição dos tempos de entrega por cidade e tipo de pedido    
  with st.container():
    fig = px.box(dados, x='City', y='Time_taken(min)', color='Type_of_order',
                 labels={
                   'City': 'Cidade',
                   'Time_taken(min)': 'Tempo de entrega (min)',
                   'Type_of_order': 'Tipo de pedido'
                 },
                 title='Distribuição dos Tempos de Entrega por Cidade e Tipo de Pedido')
    st.plotly_chart(fig, use_container_width=True)
  
  # Criar o gráfico da distribuição dos tempos de entrega por cidade e condição de trânsito    
  with st.container():
    fig = px.box(dados, x='City', y='Time_taken(min)', color='Road_traffic_density',
                 labels={
                   'City': 'Cidade',
                   'Time_taken(min)': 'Tempo de entrega (min)',
                   'Road_traffic_density': 'Condição de Trânsito'
                 },
                 title='Distribuição dos Tempos de Entrega por Cidade e Condição de Trânsito')
    st.plotly_chart(fig, use_container_width=True)
  
  # Criar o gráfico da distribuição dos tempos de entrega por festival   
  with st.container():
    fig = px.box(dados, x='Festival', y='Time_taken(min)',
                 labels={
                   'Time_taken(min)': 'Tempo de entrega (min)',
                 },
                 title='Distribuição dos Tempos de Entrega por Festival')
    st.plotly_chart(fig, use_container_width=True)
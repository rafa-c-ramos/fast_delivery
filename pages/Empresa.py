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
st.set_page_config(page_title='Visão da Empresa', layout='wide')

#################### Título da página do Streamlit ####################
st.markdown('# Marketplace - Visão da Empresa')

#################### Barra lateral do Streamlit ####################
# Inserir o logo da empresa
image = Image.open('fast_delivery_logo.png')
st.sidebar.image(image, width=200)

# Criar o título e subtítulo da barra lateral
st.sidebar.markdown('# Fast Delivery')
st.sidebar.markdown('## The Quickest Delivery')
st.sidebar.markdown('---')

# Criar o filtro de data
slider_dia = st.sidebar.slider('Selecione uma data limite:',
                               value=datetime(2022, 4, 6),
                               min_value=datetime(2022, 2, 11),
                               max_value=datetime(2022, 4, 6),
                               format='DD-MM-YYYY')

linhas_selecionadas = dados['Order_Date'] <= slider_dia
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro da densidade de trânsito
filtro_transito = st.sidebar.multiselect('Selecione as condições de trânsito:',
                                         ['Low', 'Medium', 'High', 'Jam'], 
                                         default=['Low', 'Medium', 'High', 'Jam'])

linhas_selecionadas = dados['Road_traffic_density'].isin(filtro_transito)
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro da semana do ano
slider_semana = st.sidebar.slider('Selecione uma semana limite:',
                                  value=14,
                                  min_value=6,
                                  max_value=14)

linhas_selecionadas = dados['week_of_the_year'] <= slider_semana
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro da condição do tempo
filtro_condicao_tempo = st.sidebar.multiselect('Selecione as condições de tempo:',
                                      ['Sunny', 'Stormy', 'Sandstorm', 'Cloudy', 'Fog', 'Windy'],
                                      default=['Sunny', 'Stormy', 'Sandstorm', 'Cloudy', 'Fog', 'Windy'])

linhas_selecionadas = dados['Weatherconditions'].isin(filtro_condicao_tempo)
dados = dados.loc[linhas_selecionadas, :]

#################### Layout do Streamlit ####################
# Criar e nomear as tabs (abas) 
tab_1, tab_2, tab_3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

# Preencher a tab 1 (Visão Gerencial)
with tab_1:
  # Criar gráfico de número de pedidos por dia
  with st.container():
    aux = dados.groupby('Order_Date')['ID'].count().reset_index()
    fig = px.bar(aux, x='Order_Date', y='ID',
                 labels={
                   'Order_Date': 'Dia do pedido',
                   'ID': 'Contagem'
                 },
                 title='Número de Pedidos por Dia')
    st.plotly_chart(fig, use_container_width=True)
    
  # Criar gráfico de número de pedidos por semana
  with st.container():
    aux = dados.groupby('week_of_the_year')['ID'].count().reset_index()
    fig = px.bar(aux, x='week_of_the_year', y='ID',
                 labels={
                   'week_of_the_year': 'Semana do pedido',
                   'ID': 'Contagem'
                 },
                 title='Número de Pedidos por Semana')
    st.plotly_chart(fig, use_container_width=True)

# Preencher a tab 2 (Visão Tática)     
with tab_2:
  with st.container():
    col_1, col_2 = st.columns(2)
    
    # Criar gráfico de número de pedidos por condição de trânsito
    with col_1:
      aux = dados.groupby('Road_traffic_density')['ID'].count().reset_index()
      fig = px.bar(aux, x='Road_traffic_density', y='ID',
                   labels={
                   'Road_traffic_density': 'Condição de trânsito',
                   'ID': 'Contagem'
                 },
                   title='Número de Pedidos por Condição de Trânsito')
      st.plotly_chart(fig, use_container_width=True)
    
    # Criar gráfico de número de pedidos por condição de trânsito e cidade  
    with col_2:
      aux = dados.groupby(['Road_traffic_density', 'City'])['ID'].count().reset_index()
      fig = px.bar(aux, x='Road_traffic_density', y='ID', color='City',
                    labels={
                   'Road_traffic_density': 'Condição de trânsito',
                   'ID': 'Contagem',
                   'City': 'Cidade'
                 },
                    title='Número de Pedidos por Condição de Trânsito e Cidade')
      st.plotly_chart(fig, use_container_width=True)
  
  with st.container():
    col_1, col_2 = st.columns(2)

    # Criar gráfico de número de pedidos por condição de trânsito  
    with col_1:
      aux = dados.groupby(['Weatherconditions'])['ID'].count().reset_index()
      fig = px.bar(aux, x='Weatherconditions', y='ID',
                 labels={
                   'Weatherconditions': 'Condição de tempo',
                   'ID': 'Contagem',
                 },
                   title='Número de Pedidos por Condição de Tempo')
      st.plotly_chart(fig, use_container_width=True)
      
    # Criar gráfico de número de pedidos por condição de trânsito e cidade    
    with col_2:
      aux = dados.groupby(['Weatherconditions', 'City'])['ID'].count().reset_index()
      fig = px.bar(aux, x='Weatherconditions', y='ID', color='City',
                 labels={
                   'Weatherconditions': 'Condição de tempo',
                   'ID': 'Contagem',
                   'City': 'Cidade'
                 },
                   title='Número de Pedidos por Condição de Tempo e Cidade')
      st.plotly_chart(fig, use_container_width=True) 
                   
# Preencher a tab 3 (Visão Geográfica)        
with tab_3:
  
  # Criar o mapa da visão geográfica
  aux =  dados.groupby(['City', 'Road_traffic_density'])[
    ['Delivery_location_latitude', 'Delivery_location_longitude',]].median().reset_index()
  map_ = folium.Map()
  for index, location_info in aux.iterrows():
    folium.Marker([location_info['Delivery_location_latitude'],
    location_info['Delivery_location_longitude']],
    popup=location_info[['City', 'Road_traffic_density']]).add_to(map_)
  folium_static(map_, width=1024, height=600)    
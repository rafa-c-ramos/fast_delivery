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
st.set_page_config(page_title='Entregadores', layout='wide', page_icon='🏍️')

#################### Título do Streamlit ####################
st.markdown('# Dashboard - Entregadores')

#################### Barra lateral do Streamlit ####################
# Inserir o logo da empresa
image = Image.open('fast_delivery_logo.png')
st.sidebar.image(image, width=200)

# Criar o título e subtítulo da barra lateral
st.sidebar.markdown('# Fast Delivery')
st.sidebar.markdown('## The Quickest Delivery')
st.sidebar.markdown('---')

# Criar o filtro de idade do entregador
slider_idade = st.sidebar.slider('Selecione uma idade limite (anos):',
                                 value=39,
                                 min_value=20,
                                 max_value=39)

linhas_selecionadas = dados['Delivery_person_Age'] <= slider_idade
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro da cidade
filtro_cidade = st.sidebar.multiselect('Selecione as cidades:',
                                       ['Urban', 'Metropolitian', 'Semi-Urban'],
                                       default=['Urban', 'Metropolitian', 'Semi-Urban'])

linhas_selecionadas = dados['City'].isin(filtro_cidade)
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro da densidade de tráfego
filtro_transito = st.sidebar.multiselect('Selecione as condições de trânsito:',
                                         ['Low', 'Medium', 'High', 'Jam'],
                                         default=['Low', 'Medium', 'High', 'Jam'])

linhas_selecionadas = dados['Road_traffic_density'].isin(filtro_transito)
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro da condição do tempo
filtro_condicao_tempo = st.sidebar.multiselect('Selecione as condições de tempo:',
                                               ['Sunny', 'Stormy', 'Sandstorm', 'Cloudy', 'Fog', 'Windy'],
                                               default=['Sunny', 'Stormy', 'Sandstorm', 'Cloudy', 'Fog', 'Windy'])

linhas_selecionadas = dados['Weatherconditions'].isin(filtro_condicao_tempo)
dados = dados.loc[linhas_selecionadas, :]
st.sidebar.markdown('---')

# Criar o filtro do tempo de entrega
slider_tempo_entrega = st.sidebar.slider('Selecione um tempo de entrega limite (min):',
                                         value=54,
                                         min_value=10,
                                         max_value=54)

linhas_selecionadas = dados['Time_taken(min)'] <= slider_tempo_entrega
dados = dados.loc[linhas_selecionadas, :]

#################### Layout do Streamlit ####################
# Criar e nomear as tabs (abas)
tab_1, tab_2 = st.tabs(['Visão Pessoal', 'Visão Avaliativa'])

# Preencher a tab 1 (Visão Pessoal)
with tab_1:
  
  # Criar o gráfico da distribuição da idade dos entregadores
  with st.container():
    fig = px.box(dados, x='Delivery_person_Age',
                 labels={
                   'Delivery_person_Age': 'Idade do entregador'
                 },
                 title='Distribuição da Idade dos Entregadores')
    st.plotly_chart(fig, use_container_width=True)
    
  # Criar o gráfico da distribuição da idade dos entregadores por cidade
  with st.container():
    fig = px.box(dados, x='City', y='Delivery_person_Age',
                 labels={
                   'City': 'Cidade',
                   'Delivery_person_Age': 'Idade do entregador'
                 },
                 title='Distribuição da Idade dos Entregadores por Cidade')
    st.plotly_chart(fig, use_container_width=True)
    
  # Criar o gráfico da proporção de entregadores por tipo de veículo       
  with st.container():
    fig = px.pie(dados, names='Vehicle_condition', values='ID',
                 title='Proporção de Entregadores por Condição do Veículo')
    st.plotly_chart(fig, use_container_width=True)

# Preencher a tab 2 (Visão Avaliativa)
with tab_2:
  
  # Criar o gráfico da distribuição dos ratings dos entregadores por cidade 
  with st.container():
    fig = px.box(dados, x='City', y='Delivery_person_Ratings',
                 labels={
                   'City': 'Cidade',
                   'Delivery_person_Ratings': 'Rating do entregador'
                 },
                 title='Distribuição dos Ratings dos Entregadores por Cidade')
    st.plotly_chart(fig, use_container_width=True)
    
  # Criar o gráfico da distribuição dos ratings dos entregadores por cidade e condição do veículo  
  with st.container():
    fig = px.box(dados, x='City', y='Delivery_person_Ratings', color='Vehicle_condition',
                 labels={
                   'City': 'Cidade',
                   'Delivery_person_Ratings': 'Rating do entregador',
                   'Vehicle_condition': 'Condição do Veículo'
                 },
                 title='Distribuição dos Ratings dos Entregadores por Cidade e Condição do Veículo')
    st.plotly_chart(fig, use_container_width=True)  

  # Criar o gráfico da distribuição dos ratings dos entregadores por cidade e festival
  with st.container():
    fig = px.box(dados, x='City', y='Delivery_person_Ratings', color='Festival',
                 labels={
                   'City': 'Cidade',
                   'Delivery_person_Ratings': 'Rating do entregador',
                   'Festival': 'Festival'
                 },
                 title='Distribuição dos Ratings dos Entregadores por Cidade e Festival')
    st.plotly_chart(fig, use_container_width=True) 
  
  # Criar o gráfico da distribuição dos ratings dos entregadores por condição de trânsito       
  with st.container():
    fig = px.box(dados, x='Road_traffic_density', y='Delivery_person_Ratings',
                 labels={
                   'Road_traffic_density': 'Condição de trânsito',
                   'Delivery_person_Ratings': 'Rating do entregador'
                 },
                 title='Distribuição dos Ratings dos Entregadores por Condição de Trânsito')
    st.plotly_chart(fig, use_container_width=True)
    
    # Criar o gráfico da distribuição dos ratings dos entregadores por condição de tempo     
    with st.container():
      fig = px.box(dados, x='Weatherconditions', y='Delivery_person_Ratings',
                   labels={
                     'Weatherconditions': 'Condição do tempo',
                     'Delivery_person_Ratings': 'Rating do entregador'
                   },
                   title='Distribuição dos Ratings dos Entregadores por Condição de Tempo')
      st.plotly_chart(fig, use_container_width=True)
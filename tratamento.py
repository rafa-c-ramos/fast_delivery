# Importar as bibliotecas e módulos
import numpy as np
import pandas as pd
from datetime import datetime
from haversine import haversine, Unit

# Criar a função para o tratamento dos dados
def trata_df(dados):
  
  """  
  Esta função é responsável pelo tratamento dos dados.
       
  Tipos de tratamento:
  1. Remoção de valores vazios.
  2. Remoção dos espaços nas observações de variáveis nominais.
  3. Correção do tipo das variáveis. 
  4. Criação des novas features.      
  """
  
  # Remover os valores vazios
  dados = dados.dropna()
  
  # Filtrar os NaNs "escritos"
  for variavel in dados.columns:
    linhas_preenchidas = dados[variavel] != 'NaN'
    dados = dados.loc[linhas_preenchidas, :]
    
  # Filtrar os NaNs "escritos" com espaço no final
  for variavel in dados.columns:
    linhas_preenchidas = dados[variavel] != 'NaN '
    dados = dados.loc[linhas_preenchidas, :]
  
  # Resetar o index do dataframe
  dados = dados.reset_index(drop=True)
  
  # Remover espaco das strings das variáveis nominais
  dados.loc[:, 'ID'] = dados.loc[:, 'ID'].str.strip()
  dados.loc[:, 'Delivery_person_ID'] = dados.loc[:, 'Delivery_person_ID'].str.strip()
  dados.loc[:, 'Weatherconditions'] = dados.loc[:, 'Weatherconditions'].str.strip('conditions ')
  dados.loc[:, 'Road_traffic_density'] = dados.loc[:, 'Road_traffic_density'].str.strip()
  dados.loc[:, 'Type_of_order'] = dados.loc[:, 'Type_of_order'].str.strip()
  dados.loc[:, 'Type_of_vehicle'] = dados.loc[:, 'Type_of_vehicle'].str.strip()
  dados.loc[:, 'Festival'] = dados.loc[:, 'Festival'].str.strip()
  dados.loc[:, 'City'] = dados.loc[:, 'City'].str.strip()
  dados.loc[:, 'Time_taken(min)'] = dados.loc[:, 'Time_taken(min)'].str.strip('(min) ')

  # Converter variável de idade do entregador de object para int
  dados['Delivery_person_Age'] = dados['Delivery_person_Age'].astype(int)

  # Converter variável de rating do entregador de object para float
  dados['Delivery_person_Ratings'] = dados['Delivery_person_Ratings'].astype(float)

  # Converter variável de múltiplas entregas de object para int
  dados['multiple_deliveries'] = dados['multiple_deliveries'].astype(int)

  # Converter variável de tempo de entrega de object para int
  dados['Time_taken(min)'] = dados['Time_taken(min)'].astype(int)
  
  # Converter variável de tempo de entrega de object para str
  dados['Vehicle_condition'] = dados['Vehicle_condition'].astype(str)
  
  # Converter variável de data da entrega de object para datetime
  dados['Order_Date'] = pd.to_datetime(dados['Order_Date'], format='%d-%m-%Y')

  # Corrigir a grafia da variável de hora do pedido
  dados.rename(columns={'Time_Orderd':'Time_Ordered'}, inplace=True)

  # Converter as variáveis de horário do pedido e horário da entrega para datetime
  dados['Time_Ordered'] = pd.to_datetime(dados['Order_Date'].astype(str) + ' ' + dados["Time_Ordered"].astype(str))
  dados['Time_Order_picked'] = pd.to_datetime(dados['Order_Date'].astype(str) + ' ' + dados["Time_Order_picked"].astype(str))

  # Consertar a data das entregas que ocorreram após meia-noite
  dados.loc[dados['Time_Ordered'] > dados['Time_Order_picked'], 'Time_Order_picked'] += pd.Timedelta(days=1)

  # Criar a variável com a distância entre os restaurantes e locais de entregas em km
  dados['distance_delivery_km'] = dados.apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                          (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
  
  # Remover observações extremas de distância de entrega
  dados = dados[dados['distance_delivery_km'] <= 2000]
  
  # Criar a variável da semana do ano
  dados['week_of_the_year'] = dados['Order_Date'].dt.isocalendar().week

  # Retornar o dataframe tratado
  return dados
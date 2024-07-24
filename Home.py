# Importar os módulos
import streamlit as st
from PIL import Image

# Ajustar a configuração do Streamlit
st.set_page_config(page_title='Home', layout='wide', page_icon='🌐')

# Inserir o logo da empresa no Streamlit
image = Image.open('fast_delivery_logo.png')
st.sidebar.image(image, width=200)

# Criar o título e subtítulo da barra lateral do Streamlit
st.sidebar.markdown('# Fast Delivery')
st.sidebar.markdown('## The Quickest Delivery')

# Escrever as informações do Streamlit
st.markdown("""
            # Fast Delivery Growth Dashboard
            
            O Growth Dashboard acompanha métricas de negócio da companhia Fast Delivery pelas perspectivas da empresa, dos entregadores e dos restaurantes.
            
            Estrutura do Growth Dashboard:
            
            - Visão da Empresa:
              - Visão Gerencial: panorama macro do crescimento da empresa.
              - Visão Tática: panomara segmentado do crescimento da empresa.
              - Visão Geográfica: mapa de pontos centrais por tipo de trânsito.
            
            - Visão dos Entregadores:
              - Visão Pessoal: características individuais dos entregadores.
              - Visão Avaliativa: situação avaliativa dos entregadores.
        
            - Visão dos Restaurantes:
              - Visão Transporte: descrição da distâncias de entrega.
              - Visão Velocidade: quadro do tempo de espera até a entrega.
                          
            ### Ajuda
            GitHub: rafa-c-ramos.
            """)
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
from groq import Groq
from comandos import instrucao, instrucao_grafico
from streamlit_ace import st_ace

load_dotenv()

@st.dialog('Prévia do gráfico', width='large')
def exibir_grafico(codigo_grafico):
    try:
        exec(codigo_grafico, {'st':st})
    except Exception as erro:
        st.error(f'Não foi possível gerar o gráfico, por: {erro}')

def criar_engine():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError('Variável de ambiente DATABASE_URL não configurada.')
    return create_engine(database_url)

engine = criar_engine()

if 'df' not in st.session_state:
    with engine.connect() as conn:
        st.session_state.df = pd.read_sql(text('select * from vendas_produtos'), conn)


# LAYOUT STREAMLIT
st.set_page_config(layout='wide', page_title='Consultor SQL Carbon')

with st.form('form-pergunta'):
    pergunta = st.text_area('O que você quer saber sobre seus dados?',
                placeholder='Ex: Total de vendas de agosto de 2026', height=200)
    enviar_pergunta = st.form_submit_button('Enviar Pergunta')

    if enviar_pergunta:
        if pergunta:
            instrucao += pergunta
            with st.spinner('Gerando resposta'):
                client = Groq(api_key=os.getenv('GROQ_API_KEY'))
                # gerar sql
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user","content": instrucao}],
                    temperature=0.2,
                )
                st.session_state.sql_gerado = completion.choices[0].message.content

                # gerar codigo python
                prompt_grafico = instrucao_grafico + st.session_state.sql_gerado
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user","content": prompt_grafico}],
                    temperature=0.2,
                )
                st.session_state.codigo_gerado = completion.choices[0].message.content
        else:
            st.error('Escreva a sua pergunta')

col2, col3 = st.columns([0.5,0.5], gap='xsmall')
with col2:
    if 'sql_gerado' not in st.session_state:
        st.session_state.sql_gerado = ''
    
    with st.form('form-sql'):
        st.text('Código SQL')
        sql_editavel = st_ace(value=st.session_state.sql_gerado, height=200, language='sql', theme='monokai')
        executar_sql = st.form_submit_button('Executar consulta')

        if executar_sql:
            with engine.connect() as conn:
                st.session_state.df = pd.read_sql(text(sql_editavel), conn)
                st.success('Consulta realizada')


with col3:
    if'codigo_gerado' not in st.session_state:
        st.session_state.codigo_gerado = ''
    with st.form('codigo_grafico'):
        st.text('Código Gerado')
        codigo_editavel = st_ace(value=st.session_state.codigo_gerado, height=200, language='python', theme='monokai', wrap=True)
        gerar_grafico = st.form_submit_button('Gerar gráfico')

    if gerar_grafico:
        if not codigo_editavel.strip():
            st.warning('Não há código')
        else:
            exibir_grafico(codigo_editavel)

st.dataframe(st.session_state.df)

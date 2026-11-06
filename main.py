from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
from groq import Groq
from comandos import instrucao


def criar_engine():

    database_url = st.secrets.get('DATABASE_URL')
    if not database_url:
        raise ValueError('Variável de ambiente DATABASE_URL não configurada.')
    return create_engine(database_url)

engine = criar_engine()

if 'df' not in st.session_state:
    with engine.connect() as conn:
        st.session_state.df = pd.read_sql(text('select * from vendas_produtos'), conn)


# LAYOUT STREAMLIT
st.set_page_config(layout='wide', page_title='Consultor SQL Carbon')
col1, col2 = st.columns([0.6,0.4])
with col1:
    with st.form('form-pergunta'):
        pergunta = st.text_area('O que você quer saber sobre seus dados?',
                    placeholder='Total de vendas de agosto de 2026', height=200)
        enviar_pergunta = st.form_submit_button('Enviar Pergunta')

        if enviar_pergunta:
            if pergunta:
                instrucao += pergunta
                with st.spinner('Gerando resposta'):
                    client = Groq(api_key=st.secrets.get(('GROQ_API_KEY')))
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[{"role": "user","content": instrucao}],
                        temperature=0.2,
                    )
                    st.session_state.sql_gerado = completion.choices[0].message.content
            else:
                st.error('Escreva a sua pergunta')

with col2:
    if 'sql_gerado' not in st.session_state:
        st.session_state.sql_gerado = ''
    
    with st.form('form-sql'):
        sql_editavel = st.text_area('SQL Gerado',value=st.session_state.sql_gerado, height=200)
        executar_sql = st.form_submit_button('Executar consulta')

        if executar_sql:
            with engine.connect() as conn:
                st.session_state.df = pd.read_sql(text(sql_editavel), conn)
                st.success('Consulta realizada')

st.dataframe(st.session_state.df)

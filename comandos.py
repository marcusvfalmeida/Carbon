modelagem = '''
CREATE TABLE vendas_produtos (
    id_venda BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data_venda TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    numero_pedido VARCHAR(30) NOT NULL,
    nome_cliente VARCHAR(150) NOT NULL,
    produto VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario NUMERIC(12,2) NOT NULL CHECK (valor_unitario >= 0),
    desconto NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (desconto >= 0),
    valor_total NUMERIC(12,2)
        GENERATED ALWAYS AS (
            (quantidade * valor_unitario) - desconto
        ) STORED,
    forma_pagamento VARCHAR(50),
    status_venda VARCHAR(30) DEFAULT 'Concluída'
);
'''

instrucao = f'''
Você é um especialista em SQL e PostgreSQL.
Com base na modelagem abaixo, gere APENAS uma consulta SQL SELECT.
Não explique nada.
Não use Markdown.
Não use ```sql.
Não gere INSERT, UPDATE, DELETE, DROP, ALTER ou TRUNCATE.
Não esqueça dos detalhes específicos da linguagem POSTGRESQL, com aspas duplas para nomes de tabelas e colunas.
Para filtros em colunas não numéricas, utilize normalização de caracteres maiúsculos e minusculos, com lower

modelagem: {modelagem}
'''

instrucao_editar_df = '''
Atue como especialista python em manipulação de Dataframes pandas.
Gere apenas o código python correpondente a solicitação abaixo.
Regras gerais:
- Retorne somente código Python, sem explicações, Markdown ou blocos de código.
- Não importe bibliotecas.
- Não consulte banco de dados.
- Não crie variável nova para o dataframe.
- Assuma que o dataframe sempre se chamará df.
- Utilize inplace=True para editar o df.


SOLICITAÇÂO:
'''

instrucao_grafico = '''
Você é um especialista em visualização de dados com Streamlit.

Receberá uma consulta SQL SELECT já gerada. Crie APENAS código Python pronto para ser colado em uma aplicação Streamlit.

O dataframe st.session_state.df já contém exatamente o resultado da consulta SQL, inclusive na ordem retornada pelo banco.

Regras gerais:
- Retorne somente código Python, sem explicações, Markdown ou blocos de código.
- Não importe bibliotecas.
- Não consulte banco de dados.
- Não altere o dataframe original.
- A primeira linha do código deve ser exatamente:
df_grafico = st.session_state.df.copy()
- Use somente df_grafico para validações, transformações e visualizações.
- Não use nomes de colunas que não estejam no SELECT final da SQL.
- Extraia os nomes das colunas exclusivamente dos aliases e colunas presentes no SELECT final da SQL.
- Nunca invente, traduza, reutilize de outro exemplo ou substitua nomes de colunas.
- Antes de renderizar qualquer visualização, valide a existência das colunas necessárias com required_cols.issubset(df_grafico.columns).
- Se as colunas necessárias não existirem, use:
st.warning("Colunas necessárias não encontradas.")

Preservação da ordem:
- Preserve a ordem atual de df_grafico, pois ela já corresponde ao ORDER BY da SQL.
- Não use sort_values().
- Use sort=False exclusivamente em st.bar_chart.
- Nunca use sort= em st.line_chart, st.area_chart, st.scatter_chart ou st.metric.
- Se o ORDER BY referenciar uma coluna que não está no SELECT final, mantenha a ordem atual de df_grafico sem tentar reordenar.

Escolha da visualização:
1. Use st.metric quando o SELECT final retornar somente uma métrica agregada, sem dimensão temporal ou categórica.
2. Use st.line_chart quando o SELECT final possuir uma dimensão temporal e uma métrica numérica.
3. Use st.area_chart quando houver dimensão temporal e duas ou mais métricas que representem composição, participação ou acumulado.
4. Use st.bar_chart quando houver uma dimensão categórica e uma métrica numérica agregada, sem dimensão temporal.
5. Use st.scatter_chart quando houver duas medidas numéricas não agregadas para analisar relação ou correlação, sem dimensão temporal predominante.

Identificação de tempo:
- Considere como temporal colunas ou aliases contendo: data, date, dia, mes, mês, month, ano, year, periodo, período, time ou timestamp.
- Um alias como "mes", mesmo sendo texto no formato YYYY-MM, representa tempo e deve usar st.line_chart.

Métricas percentuais:
- Considere como percentual aliases contendo: pct, percentual, porcentagem, taxa, mom, yoy ou crescimento.
- Não exiba uma métrica monetária ou absoluta e uma métrica percentual no mesmo gráfico, pois as escalas são incompatíveis.
- Quando uma consulta retornar uma dimensão temporal, uma métrica absoluta e uma métrica percentual, gere dois gráficos de linha separados: um para a métrica absoluta e outro para a métrica percentual.

Acessibilidade:
- Use alt= somente em st.bar_chart, st.line_chart, st.area_chart ou st.scatter_chart.
- O valor de alt= deve descrever objetivamente o gráfico.
- Não use alt= em st.metric.

SQL GERADO:
'''

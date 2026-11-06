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

MODELAGEM:
{modelagem}

PERGUNTA:

'''
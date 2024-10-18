from sqlalchemy import create_engine
import requests
import pandas as pd

DATABASE_TYPE = 'postgresql'
USER = 'northwind_bd_user'
PASSWORD = 'SRj2TltxbiqaqGvZoCNvZfNlcd85jtLc'
HOST = 'host_fornecido_pelo_render'
PORT = '5432'
DATABASE = 'northwind_bd'

connection_string = "postgresql://northwind_bd_user:SRj2TltxbiqaqGvZoCNvZfNlcd85jtLc@dpg-cs4hcujtq21c73ftnqe0-a.oregon-postgres.render.com/northwind_bd"
engine = create_engine(connection_string)


# Inserir no banco de dados
df.to_sql('categories.csv', con=engine, if_exists='replace', index=False)

# Verificar a importação
with engine.connect() as connection:
    result = connection.execute("SELECT * FROM nome_da_tabela LIMIT 5")
    for row in result:
        print(row)
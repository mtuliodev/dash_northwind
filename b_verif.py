from sqlalchemy import create_engine, inspect, text
import pandas as pd

connection_string = "postgresql://northwind_bd_user:SRj2TltxbiqaqGvZoCNvZfNlcd85jtLc@dpg-cs4hcujtq21c73ftnqe0-a.oregon-postgres.render.com/northwind_bd"
engine = create_engine(connection_string)
inspector = inspect(engine)
tabelas = inspector.get_table_names()
print("Tabelas existentes no banco de dados:", tabelas)

with engine.connect() as connection:
    connection.execute(text('DROP TABLE "categories.csv"'))
    print('Tabela "categorias" foi removida.')

# Remover a tabela 'categories'
with engine.connect() as connection:
    connection.execute(text('ALTER TABLE "categories.csv" RENAME TO "categorias"'))
    print('Tabela "categories.csv" foi renomeada para "categorias".')

from sqlalchemy import create_engine
import pandas as pd

connection_string = "postgresql://northwind_zryd_user:w1XZxe6BMEsxNOw9wUphE5YpJjAGzrPV@dpg-cs77vr0gph6c73fft5ng-a.oregon-postgres.render.com/northwind_zryd"
engine = create_engine(connection_string)

df = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/categories.csv', sep = ';')
df2 = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/customer_customer_demo.csv', sep = ';')
df3 = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/customer_demographics.csv', sep = ';')
df4 = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/customers.csv', sep = ';')
df5 = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/employee_territories.csv', sep = ';')
df6 = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/employees.csv', sep = ';')
df7 = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/order_details.csv', sep = ';')
df8 = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/orders.csv', sep = ';')
df9 = pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/products.csv', sep = ';')
df10= pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/region.csv', sep = ';')
df11= pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/shippers.csv', sep = ';')
df12= pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/suppliers.csv', sep = ';')
df13= pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/territories.csv', sep = ';')
df14= pd.read_csv(r'C:/Users/mtuli/Desktop/northwind (3)/us_states.csv', sep = ';')

df.to_sql('categories', con=engine, if_exists='replace', index=False)
df2.to_sql('customer_customer_demo', con=engine, if_exists='replace', index=False)
df3.to_sql('customer_demographics', con=engine, if_exists='replace', index=False)
df4.to_sql('customers', con=engine, if_exists='replace', index=False)
df5.to_sql('employee_territories', con=engine, if_exists='replace', index=False)
df6.to_sql('employees', con=engine, if_exists='replace', index=False)
df7.to_sql('order_details', con=engine, if_exists='replace', index=False)
df8.to_sql('orders', con=engine, if_exists='replace', index=False)
df9.to_sql('products', con=engine, if_exists='replace', index=False)
df10.to_sql('region', con=engine, if_exists='replace', index=False)
df11.to_sql('shippers', con=engine, if_exists='replace', index=False)
df12.to_sql('suppliers', con=engine, if_exists='replace', index=False)
df13.to_sql('territories', con=engine, if_exists='replace', index=False)
df14.to_sql('us_states', con=engine, if_exists='replace', index=False)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard da Northwind Traders", layout="wide")

tab = st.sidebar.radio("Navegue", ["Financeiro", "Clientes", "Produtos"])

if tab == "Financeiro":
    st.title("Dashboard da Northwind Traders")
    st.header("Análise Financeira")

    # Dados
    orders = df8
    order_details = df7
    products = df9
    customers = df4
    categories = df

    # Conversão de datas
    orders['order_date'] = pd.to_datetime(orders['order_date'])

    # Merge dos dataframes
    order_details = order_details.merge(orders, on='order_id')
    order_details = order_details.merge(products, on='product_id')
    order_details = order_details.merge(customers, on='customer_id')
    order_details = order_details.merge(categories, on='category_id')

    # Cálculo do preço total
    order_details['total_price'] = order_details['unit_price'] * order_details['quantity'] * (1 - order_details['discount'])
    order_details['month'] = order_details['order_date'].dt.to_period('M').astype(str)

    # Vendas Mensais Totais
    monthly_sales = order_details.groupby('month')['total_price'].sum().reset_index()
    fig_monthly_sales = px.line(monthly_sales, x='month', y='total_price', markers=True, title='Vendas Mensais Totais')
    st.plotly_chart(fig_monthly_sales, use_container_width=True)

    # Vendas por País
    sales_by_country = order_details.groupby('country')['total_price'].sum().reset_index()
    fig_sales_country = px.bar(sales_by_country, x='country', y='total_price', color='country', title='Vendas por País')
    st.plotly_chart(fig_sales_country, use_container_width=True)

    # Vendas por Categoria
    sales_by_category = order_details.groupby('category_name')['total_price'].sum().reset_index()
    fig_sales_category = px.bar(sales_by_category, x='total_price', y='category_name', orientation='h', title='Vendas por Categoria')
    st.plotly_chart(fig_sales_category, use_container_width=True)

    # Valor Médio dos Pedidos Mensais
    avg_order_value = order_details.groupby('order_id')['total_price'].sum().reset_index()
    avg_order_value['month'] = order_details.groupby('order_id')['order_date'].first().dt.to_period('M').astype(str).values
    avg_order_value_monthly = avg_order_value.groupby('month')['total_price'].mean().reset_index()
    fig_avg_order_value = px.line(avg_order_value_monthly, x='month', y='total_price', markers=True, title='Valor Médio dos Pedidos Mensais')
    st.plotly_chart(fig_avg_order_value, use_container_width=True)

elif tab == "Clientes":
    st.header("Análise de Clientes")

    # Dados
    customers = df4
    orders = df8
    order_details = df7

    # Total de Clientes
    total_customers = customers['customer_id'].nunique()
    st.metric("Total de Clientes", total_customers)

    # Clientes por País
    customers_by_country = customers['country'].value_counts().reset_index()
    customers_by_country.columns = ['country', 'number_of_customers']
    fig_customers_country = px.bar(customers_by_country, x='country', y='number_of_customers', color='country', title='Clientes por País')
    st.plotly_chart(fig_customers_country, use_container_width=True)

    # Top 10 Clientes por Número de Pedidos
    orders_per_customer = orders['customer_id'].value_counts().reset_index()
    orders_per_customer.columns = ['customer_id', 'number_of_orders']
    top_customers_orders = orders_per_customer.merge(customers[['customer_id', 'company_name']], on='customer_id').head(10)
    fig_orders_per_customer = px.bar(top_customers_orders, x='number_of_orders', y='company_name', orientation='h', title='Top 10 Clientes por Número de Pedidos')
    st.plotly_chart(fig_orders_per_customer, use_container_width=True)

    # Top 10 Clientes por Vendas
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    order_data = order_details.merge(orders, on='order_id')
    order_data = order_data.merge(customers, on='customer_id')
    order_data['total_price'] = order_data['unit_price'] * order_data['quantity'] * (1 - order_data['discount'])
    sales_per_customer = order_data.groupby('customer_id')['total_price'].sum().reset_index()
    sales_per_customer = sales_per_customer.merge(customers[['customer_id', 'company_name']], on='customer_id')
    top_customers_sales = sales_per_customer.sort_values('total_price', ascending=False).head(10)
    fig_sales_per_customer = px.bar(top_customers_sales, x='total_price', y='company_name', orientation='h', title='Top 10 Clientes por Vendas')
    st.plotly_chart(fig_sales_per_customer, use_container_width=True)

    # Análise RFM dos Clientes
    snapshot_date = orders['order_date'].max() + pd.Timedelta(days=1)
    rfm = orders.groupby('customer_id').agg({
        'order_date': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'count'
    }).reset_index()
    rfm.columns = ['customer_id', 'recency', 'frequency']
    monetary = order_data.groupby('customer_id')['total_price'].sum().reset_index()
    rfm = rfm.merge(monetary, on='customer_id')
    st.subheader("Análise RFM dos Clientes")
    st.dataframe(rfm.head(10))

    fig_rfm = px.scatter(rfm, x='recency', y='frequency', size='total_price', hover_name='customer_id', title='Análise RFM dos Clientes')
    st.plotly_chart(fig_rfm, use_container_width=True)

elif tab == "Produtos":
    st.header("Análise de Produtos")

    # Dados
    products = df9
    categories = df
    suppliers = df12
    order_details = df7
    orders = df8

    # Total de Produtos
    total_products = products['product_id'].nunique()
    st.metric("Total de Produtos", total_products)

    # Produtos por Categoria
    products_by_category = products.groupby('category_id')['product_id'].count().reset_index()
    products_by_category = products_by_category.merge(categories[['category_id', 'category_name']], on='category_id')
    fig_products_category = px.bar(products_by_category, x='category_name', y='product_id', color='category_name', title='Produtos por Categoria')
    st.plotly_chart(fig_products_category, use_container_width=True)

    # Top Fornecedores por Número de Produtos
    products_by_supplier = products.groupby('supplier_id')['product_id'].count().reset_index()
    products_by_supplier = products_by_supplier.merge(suppliers[['supplier_id', 'company_name']], on='supplier_id')
    top_suppliers = products_by_supplier.sort_values('product_id', ascending=False).head(10)
    fig_products_supplier = px.bar(top_suppliers, x='product_id', y='company_name', orientation='h', title='Top Fornecedores por Número de Produtos')
    st.plotly_chart(fig_products_supplier, use_container_width=True)

    # Top 10 Produtos com Maior Estoque
    top_stock_products = products[['product_name', 'units_in_stock']].sort_values('units_in_stock', ascending=False).head(10)
    fig_stock_products = px.bar(top_stock_products, x='units_in_stock', y='product_name', orientation='h', title='Top 10 Produtos com Maior Estoque')
    st.plotly_chart(fig_stock_products, use_container_width=True)

    # Top 10 Produtos por Vendas
    order_data = order_details.merge(products, on='product_id')
    order_data['total_sales'] = order_data['unit_price'] * order_data['quantity'] * (1 - order_data['discount'])
    sales_per_product = order_data.groupby('product_name')['total_sales'].sum().reset_index()
    top_sales_products = sales_per_product.sort_values('total_sales', ascending=False).head(10)
    fig_sales_per_product = px.bar(top_sales_products, x='total_sales', y='product_name', orientation='h', title='Top 10 Produtos por Vendas')
    st.plotly_chart(fig_sales_per_product, use_container_width=True)

    # Tendência de Vendas dos Top Produtos
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    order_data = order_data.merge(orders[['order_id', 'order_date']], on='order_id')
    order_data['month'] = order_data['order_date'].dt.to_period('M').astype(str)
    top_product_names = top_sales_products['product_name'].tolist()
    sales_trend = order_data[order_data['product_name'].isin(top_product_names)]
    sales_trend = sales_trend.groupby(['month', 'product_name'])['total_sales'].sum().reset_index()
    fig_sales_trend = px.line(sales_trend, x='month', y='total_sales', color='product_name', markers=True, title='Tendência de Vendas dos Top Produtos')
    st.plotly_chart(fig_sales_trend, use_container_width=True)
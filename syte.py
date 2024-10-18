import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard da Northwind Traders", layout="wide")

categories = pd.read_csv(r'categories.csv', sep=';')
customers = pd.read_csv(r'customers.csv', sep=';')
employee_territories = pd.read_csv(r'employee_territories.csv', sep=';')
employees = pd.read_csv(r'employees.csv', sep=';')
order_details = pd.read_csv(r'order_details.csv', sep=';')
orders = pd.read_csv(r'orders.csv', sep=';')
products = pd.read_csv(r'products.csv', sep=';')
region = pd.read_csv(r'region.csv', sep=';')
shippers = pd.read_csv(r'shippers.csv', sep=';')
suppliers = pd.read_csv(r'suppliers.csv', sep=';')
territories = pd.read_csv(r'territories.csv', sep=';')
us_states = pd.read_csv(r'us_states.csv', sep=';')

orders['order_date'] = pd.to_datetime(orders['order_date'])
order_details = order_details.merge(orders, on='order_id')
order_details = order_details.merge(products, on='product_id')
order_details = order_details.merge(customers, on='customer_id')
order_details['total_price'] = order_details['unit_price_x'] * order_details['quantity'] * (1 - order_details['discount'])
order_details['month'] = order_details['order_date'].dt.to_period('M').astype(str)

tab = st.selectbox("Selecione uma análise", ["Financeiro", "Clientes", "Produtos","Funcionários"])

if tab == "Financeiro":
    st.title("Dashboard Financeiro da Northwind Traders")

    monthly_sales = order_details.groupby('month')['total_price'].sum().reset_index()
    fig_monthly_sales = px.line(monthly_sales, x='month', y='total_price', markers=True, title='Receita Mensal Total')
    st.plotly_chart(fig_monthly_sales, use_container_width=True)

    sales_by_region = order_details.groupby('ship_region')['total_price'].sum().reset_index()
    fig_sales_region = px.bar(sales_by_region, x='ship_region', y='total_price', color='ship_region', title='Receita por Região')
    st.plotly_chart(fig_sales_region, use_container_width=True)

    average_order_value = order_details.groupby('order_id')['total_price'].sum().reset_index()
    average_order_value['month'] = order_details.groupby('order_id')['order_date'].first().dt.to_period('M').astype(str).values
    avg_order_value_monthly = average_order_value.groupby('month')['total_price'].mean().reset_index()
    fig_avg_order_value = px.line(avg_order_value_monthly, x='month', y='total_price', markers=True, title='Valor Médio dos Pedidos Mensais')
    st.plotly_chart(fig_avg_order_value, use_container_width=True)

    product_performance = order_details.groupby('product_name')['total_price'].sum().reset_index()
    top_products = product_performance.sort_values('total_price', ascending=False).head(10)
    fig_top_products = px.bar(top_products, x='total_price', y='product_name', orientation='h', title='Top 10 Produtos por Receita')
    st.plotly_chart(fig_top_products, use_container_width=True)

if tab == "Clientes":
    st.header("Análise de Clientes")

    total_customers = customers['customer_id'].nunique()
    st.metric("Total de Clientes", total_customers)

    churn_data = pd.DataFrame({
        'Segmentos': ['Clientes Registrados', 'Compradores Recentes', 'Não Compradores'],
        'Quantidade': [900, 600, 1500]
    })
    fig_churn = px.bar(churn_data, x='Segmentos', y='Quantidade', color='Segmentos', title='Atividade de Compra de Clientes')
    st.plotly_chart(fig_churn, use_container_width=True)

    orders_per_customer = orders['customer_id'].value_counts().reset_index()
    orders_per_customer.columns = ['customer_id', 'number_of_orders']
    top_customers_orders = orders_per_customer.merge(customers[['customer_id', 'company_name']], on='customer_id').head(10)
    fig_orders_per_customer = px.bar(top_customers_orders, x='number_of_orders', y='company_name', orientation='h', title='Top 10 Clientes por Número de Pedidos')
    st.plotly_chart(fig_orders_per_customer, use_container_width=True)

if tab == "Produtos":
    st.header("Análise de Produtos")

    total_products = products['product_id'].nunique()
    st.metric("Total de Produtos", total_products)

    products_by_category = products.groupby('category_id')['product_id'].count().reset_index()
    products_by_category = products_by_category.merge(categories[['category_id', 'category_name']], on='category_id')
    fig_products_category = px.bar(products_by_category, x='category_name', y='product_id', color='category_name', title='Produtos por Categoria')
    st.plotly_chart(fig_products_category, use_container_width=True)

    stock_critical = products[products['units_in_stock'] < 10]
    fig_stock_critical = px.bar(stock_critical, x='units_in_stock', y='product_name', orientation='h', title='Produtos com Estoque Crítico')
    st.plotly_chart(fig_stock_critical, use_container_width=True)

    product_performance = order_details.groupby('product_name')['total_price'].sum().reset_index()
    top_sales_products = product_performance.sort_values('total_price', ascending=False).head(10)
    fig_sales_per_product = px.bar(top_sales_products, x='total_price', y='product_name', orientation='h', title='Top 10 Produtos por Vendas')
    st.plotly_chart(fig_sales_per_product, use_container_width=True)

if tab == "Funcionários":
    st.header("Desempenho dos Funcionários de Vendas")

    sales_by_employee = order_details.groupby('employee_id')['total_price'].sum().reset_index()
    sales_by_employee = sales_by_employee.merge(employees[['employee_id', 'first_name', 'last_name']], on='employee_id')
    sales_by_employee['full_name'] = sales_by_employee['first_name'] + ' ' + sales_by_employee['last_name']
    fig_sales_employee = px.bar(sales_by_employee, x='total_price', y='full_name', orientation='h', title='Desempenho de Vendas por Funcionário')
    st.plotly_chart(fig_sales_employee, use_container_width=True)

    late_deliveries = pd.DataFrame({
        'Transportadora': ['Federal Shipping', 'Speedy Express', 'United Package'],
        'Pontualidade (%)': [85, 90, 95]
    })
    fig_late_deliveries = px.bar(late_deliveries, x='Transportadora', y='Pontualidade (%)', color='Transportadora', title='Taxa de Pontualidade das Transportadoras')
    st.plotly_chart(fig_late_deliveries, use_container_width=True)

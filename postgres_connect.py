import psycopg2
import streamlit as st

conn = psycopg2.connect(
        dbname="businessanalysis",
        user="postgres",
        password="Nxxxxx",
        host="localhost",
        port=5432
    )

c = conn.cursor()

def view_all_data():
	c.execute('SELECT * FROM customers order by id asc')
	data = c.fetchall()
	return data




# def view_all_departments():
# 	c.execute('SELECT Department FROM customers')
# 	data = c.fetchmany
# 	return data



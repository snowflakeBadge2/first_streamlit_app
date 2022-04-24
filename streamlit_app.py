import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized=pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized



streamlit.title('Snowflake Badge 2 Diner')


streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick your fruits",list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)



streamlit.header('FRUITYVICE FRUIT ADVICE')

try:
  fruit_choice=streamlit.text_input("What fruit would you like information about?")
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

#stop snowflake code

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
    return my_cur.fetchall()
    
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


add_fruit=streamlit.text_input("Which fruit would you like to add?")

add_cur=my_cnx.cursor()
add_cur.execute("INSERT INTO FRUIT_LOAD_LIST values('"+add_fruit+"')")
streamlit.write("Thanks for adding"+add_fruit)


my_cur.execute("INSERT INTO FRUIT_LOAD_LIST values('from streamlit')")

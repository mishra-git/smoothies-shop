# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize your :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)



# option = st.selectbox(
 #   "What is your fav fruit?",
 #   ("Banana", "Strawberries", "Peaches"),
#)

#st.write("You selected:", option)



cnx=st.connection("snowflake"
#session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('choose up to 5 ingredients:',my_dataframe)
#ingredients_string = ''

if ingredients_list: 
   # st.write(ingredients_list)
   # st.text(ingredients_list)
    ingredients_string = ''
    
    for chosen_fruit in ingredients_list:
        ingredients_string += chosen_fruit + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
         values ('""" + ingredients_string + """')"""

    #st.write(my_insert_stmt)
    #if ingredients_string:
       # session.sql(my_insert_stmt).collect()
      #  import streamlit as st
      #  st.success('Smoothie order is created ', icon="✅")
    time_to_insert = st.button('Submit Order')

    # Using a button 
    if time_to_insert:
      session.sql(my_insert_stmt).collect()
      import streamlit as st
      st.success('Smoothie order is created ', icon="✅")



    

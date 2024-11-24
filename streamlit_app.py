# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize your :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

name_on_order = st.text_input('Name on the Smoothie')
st.write('Name on the smoothie will be:', name_on_order)


cnx=st.connection("snowflake")
#session = get_active_session()
session = cnx.session()

#session = get_active_session()
st.write("""Choose thse fruits from Database table""")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Convert the snopark data frame to the pandas dataframe so we can use the loc function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect('choose up to 5 ingredients:',my_dataframe,max_selections=5)
#ingredients_string = ''

if ingredients_list: 
   # st.write(ingredients_list)
   # st.text(ingredients_list)
    ingredients_string = ''
    
    for chosen_fruit in ingredients_list:
        ingredients_string += chosen_fruit + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader('Nutritional Information on ' + chosen_fruit)
       fruityvive_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + chosen_fruit)
       fv_df = st.dataframe(data=fruityvive_response.json(), use_container_width=True)
        
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
         values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    st.write(my_insert_stmt)
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









    

import streamlit as st
import requests
import pandas as pd
import plotly.express as pl
import os

direction = 'uploaded_files'
default = 'current_page'
into_an_answer = None

diffrent_pages = {
    "First Page":"Log In",
    "Second Page":"Sign Up",
    "Third Page":"Home"
}



if 'userId' not in st.session_state:
    st.session_state['userId'] = None

# st.write(st.session_state[default])
if st.session_state['userId']:
    st.session_state[default] = 'Home'



def the_form():
    column1,column2,column3 = st.columns([1,2,1])
    with column2:
        with st.form(key='my_form'):
            enter_name = st.text_input('Enter Name')
            enter_email = st.text_input('Enter Email')
            enter_password = st.text_input('Enter Password',type="password")
            columns_inside1,columns_inside2,columns_inside3 = st.columns(3)
            with columns_inside2:
                submit_button = st.form_submit_button('Register')
    columns1,columns2,columns3 = st.columns([1,2,1])
    with columns2:
        if st.button('Have Account'):
            st.session_state[default] = 'Log In'

    if submit_button:
        new_model = {
            'username': enter_name,
            'email': enter_email,
            'password': enter_password
        }

        if len(enter_password) >= 8:
            response = requests.post('http://127.0.0.1:8011/addUser', json=new_model)
            into_answer = response.json()
            if into_answer['added'] == 'With Success':
                st.session_state[default] = 'Log In'
            if into_answer['added'] == 'User With That Username Exists':
                st.error(into_answer['added'])

def logInForm():
    with st.form(key='my_form'):
        username = st.text_input('Username')
        password = st.text_input('Password',type="password")
        submit_button1,submit_button2,submit_button3 = st.columns(3)
        with submit_button2:
            submit_button = st.form_submit_button('Log In')
    dont_have_account1,dont_have_account2,dont_have_account3 = st.columns(3)
    with dont_have_account2:
        if st.button('Dont Have Account?'):
            st.session_state[default] = 'Sign Up'

    if submit_button:
        the_user = {
            'username':username,
            'password':password
        }
        response = requests.post('http://127.0.0.1:8011/logIn',json=the_user)
        the_answer = response.json()
        full_answer = the_answer['Valid']
        if full_answer == 'success':
            the_data = the_answer['data'][0]
            st.session_state['userId'] = the_data
            st.session_state['current_page'] = 'Home'
        else:
            st.write('Wrong Credentinals')
if 'file_submitet' not in st.session_state:
    st.session_state['file_submitet'] = False
def home():
    if st.session_state[default] == 'Home':
        st.subheader('Welcome Here Provide A Csv Link For Data Visualization')
        button1,button2,button3 = st.columns(3)
        with button3:
            if st.button('See Your Files'):
                my_url = f"http://127.0.0.1:8011/seeFiles/{st.session_state['userId']}"
                response_second = requests.get(my_url)
                into_answer = response_second.json()
                into_answer = list(into_answer)
                for name in into_answer:
                    [column] = st.columns(1)
                    if name[1] == 'n':
                        with column:
                            st.text('Nothing Added')
                    else:
                        with column:
                            st.text(name[1])
        st.text(" ")
        st.text(" ")
        st.text(" ")

        column1,column2,column3 = st.columns(3)
        with column2:
            if st.session_state['file_submitet'] == True:
                if st.session_state['fileLink']:
                   my_dictionarie = {}
                   for f in os.listdir(direction):
                       if f.endswith('.csv'):
                           my_dictionarie[f] = f
                   into_df = pd.read_csv(f'uploaded_files/{my_dictionarie[st.session_state['fileLink'].name]}')
                   options = [f for f in into_df.columns]
                   the_column_compare = st.selectbox('Enter Column To Compare In %',options)
                   first_column_top = st.selectbox('Enter First Column To See Top 10 Statistics',options)
                   second_column_top = st.selectbox('Enter The Column To GroupBy What Statistics? ',options)
                   data_set_table = st.text_input('Want To See The Data As Table (y/n)? ')
                   submit_button = st.button('Submit')

                   if submit_button:
                       if into_df[the_column_compare].any():
                           [the_next_column] = st.columns(1)
                           with the_next_column:
                                colors = ['#f9f07e', '#eedf7a', '#e6d62d', '#292929']
                                taking = into_df[the_column_compare].value_counts().head(4)
                                taking_most = taking.reset_index()
                                taking_most.columns = [the_column_compare,'Count']
                                figure = pl.pie(taking_most,names=the_column_compare,values='Count',title=f'Top 4 {the_column_compare}s',color=f'{the_column_compare}',color_discrete_sequence=colors)
                                st.plotly_chart(figure)
                       if into_df[first_column_top].any() and into_df[second_column_top].any():
                           [first_col] = st.columns(1)
                           with first_col:
                                the_df_one = into_df.groupby(first_column_top)[second_column_top].sum()
                                sorted_ones = the_df_one.sort_values(ascending=False).head(10)
                                st.bar_chart(sorted_ones)
                       if data_set_table:
                           st.subheader('Top 15')
                           the_df = into_df[the_column_compare].head(15).dropna()
                           the_df = the_df.to_frame(name=the_column_compare)
                           styled_table = the_df.style \
                               .set_table_attributes('style="width: 100%; border-collapse: collapse;"') \
                               .set_properties(**{'border': '1px solid black', 'text-align': 'center'}) \
                               .highlight_max(color='lightgreen', axis=0) \
                               .highlight_min(color='lightcoral', axis=0) \
                               .background_gradient(cmap='viridis')
                           st.dataframe(styled_table)
            else:
                the_link = st.file_uploader('Choose CSV File',type='csv')
                if the_link:
                    the_file_added = {
                        'file_name':the_link.name,
                        'file_type':the_link.type,
                        'user_id':st.session_state['userId']
                    }
                    the_url = 'http://127.0.0.1:8011/addFile'
                    response = requests.post(the_url,json=the_file_added)
                    global into_an_answer
                    into_an_answer = response.json()
                    st.write(into_an_answer['success'])
                    if into_an_answer['success'] == 'File Exists':
                        st.error('You Alredy Used That File')
                    elif into_an_answer['success'] == 'True':
                        st.success('We Took The DataSet')
                        anotherForm(the_link)
                        st.session_state['file_submitet'] = True
                        st.session_state['fileLink'] = the_link
                        if not os.path.exists(direction):
                            os.makedirs(direction)

                        file_path = os.path.join(direction,the_link.name)
                        with open(file_path,'wb') as f:
                            f.write(the_link.getbuffer())

                    else:
                        st.write('Went Wrong',into_an_answer['success'])
    else:
        st.session_state[default] = 'Sign Up'






def anotherForm(the_file):
    st.session_state[default] = 'anotherForm'
    with st.form(key='the_form'):
        the_df = pd.DataFrame(the_file)
        the_submit = st.form_submit_button('Continue')
        if the_submit:
            pass





if default not in st.session_state:
    st.session_state[default] = 'Sign Up'
if st.session_state[default] == 'Home':
    home()
elif st.session_state[default] == 'Sign Up':
    the_form()
elif st.session_state[default] == 'Log In':
    logInForm()







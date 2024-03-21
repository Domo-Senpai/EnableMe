import textwrap
import time

import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import pandas as pd
import numpy as np
#Source of the Template/Standardpage Code "https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/"


#Settings of the Mainpage, with Title and a change to the sidebar
st.set_page_config(page_title="🤗💬 Diabetes Helper", initial_sidebar_state="expanded")
#Changing settings of the sidebar
st.markdown(
    """
   <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 750px;
           max-width: 750px;
       }
       [data-testid="stSidebar"]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 2rem;
    }
    """,
    unsafe_allow_html=True,
)
#Function to interact with the LLM, hosted by HuggingFace, Login with the secrets.toml file
def generate_response(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)
#Function to display the explanation of this webapp in a stream
def stream_explanation():
    text_string = """This web application is designed to make it easier for them to get to grips with diabetes. 
    There is access to data specific to their type of disease, as well as an explanatory video. Access to the text version on the website is also possible.
     You can also clarify your personal questions with our chatbot.
    It will then respond specifically to the questions based on your chosen situation and help you further. 
    
Your data will not be stored and will not be used to improve our AI. """
    for word in text_string.split(" "):
        yield word + " "
        time.sleep(0.08)


def stream_what_else():
    text_string = """Here on this platform, you have the opportunity to get detailed information about diabetes or go to the EnableMe homepage to get a broader range of knowledge about various diseases. You can also interact with our chatbot to clarify specific questions about prevention or simply get additional information.
    
    
However, the focus of this website is to provide a comprehensive introduction and support for people living with diabetes. We provide resources, tips and a supportive environment for people affected by this disease to help them manage their daily lives and support them in living a healthy and fulfilling life.
 """
    for word in text_string.split(" "):
        yield word + " "
        time.sleep(0.08)
def create_data_frame(type):
    #df = pd.DataFrame(np.random.randn(50, 20), columns = ("col %d" % i for i in range(20)))
    columns = ["Name","Cause", "Age at diagnosis", "Risk factors", "Symptoms", "Treatment", "Frequency"]
    type1 = [type,"The body destroys the insulin-producing cells ", "Often in childhood or adolescence ", "Genetic predisposition and severe viral infection such as mumps in childhood", "Great thirst, tiredness, excessive urination or severe weight loss", "Daily insulin injections necessary", "Approximately five percent of all people affected"]
    type2 = [type,"Insulin resistance or insufficient insulin production", "Mostly in adulthood", "Genetic predisposition and obesity, too little exercise or an unhealthy, high-sugar diet", "Often only tiredness, weakness, visual disturbances or higher risk of infection", "Healthy diet and exercise, oral medication (tablets) or rarely insulin injections", "Approximately 95 percent of all people affected"]
    type3 = [type,"genetic defects, infections or diseases of the pancreas", "-", "-", "chronic increase in blood sugar", "With this type, treatment and therapeutic success are highly dependent on the respective cause. Therapies must therefore be individually adapted", "-"]
    typeg = [type,"During pregnancy, the body needs more energy and therefore produces more insulin to transport the glucose into the cells. However, sometimes this system does not work properly. This means that the glucose does not enter the cells efficiently and remains in the blood instead. As a result, blood glucose levels remain higher than normal. The mother's increased blood sugar affects the fetus, which reacts by producing more insulin. This leads to increased growth and increased fat deposition in the fetus. This in turn can later increase the risk of obesity and type 2 diabetes in the child. Gestational diabetes usually occurs in the last third of pregnancy and disappears again after the birth. Risk factors for gestational diabetes include obesity, the presence of type 2 diabetes in the family and the age of the mother, especially from 30 years onwards.", "", "", "In most cases, the mother experiences no recognizable symptoms and the typical symptoms of diabetes are not present. However, symptoms that may occur can be similar to those of normal pregnancy symptoms, such as severe thirst, frequent urination and tiredness. However, if the mother had gestational diabetes, newborns often have low blood sugar levels. For more information on diabetes in children, we recommend our article: Diabetes in children: symptoms and treatment.", "With gestational diabetes, there is a slightly increased risk of certain birth complication, particularly because the child may have excessive growth, a s previously mentioned. However, in 85% of cases, a change in diet has proven to be an effective treatment. Similarly, regular exercise, particularly in the form of 'pregnancy-friendly' activities such a s swimming or walking, helps to reduce the risk.", ""]
    if type == "autoimmune disease":
        df = pd.DataFrame([type1])
    elif type == "insulin resistance":
        df = pd.DataFrame([type2])
    elif type == "3":
        df = pd.DataFrame([type3])
    elif type == "gestational":
        df = pd.DataFrame([typeg])
    else:
        df = pd.DataFrame("Error appeared")
    df = df.transpose()
    row_titles = ['Names']
    df.index = columns
    df.columns = ["Name"]
    df.index.name = 'Row Title'
    return df
#Setting up all components of the sidebar, with title, login check, video-frame(expandabale) and links to the website to enableme
with st.sidebar:
    st.title('🤗💬 Diabetes Support Chat')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('Access to the support Chatbot', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to get the support you need.', icon='👉')
    st.markdown('📖 Learn more about [diabetes](https://www.enableme.de/de/behinderungen/diabetes-mellitus-eine-storung-des-blutzuckerstoffwechsels-1182) or other [disabilities](https://www.enableme.de/de/behinderungen) !')
    with st.expander("Explanation Video"):
        VIDEO_URL = "https://www.youtube.com/watch?v=RiCzvzPL72E"
        st.video(VIDEO_URL)
#Setting up states to move between the possibility tree structure and holding the choosen type of Diabetes
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'type' not in st.session_state:
    st.session_state.type = "not known"
def set_state(i, type_of_diabetes="not known"):
    st.session_state.stage = i
    st.session_state.type = type_of_diabetes
#Starting in the section of choosing what to do
if st.session_state.stage == 0:

    st.header("Hello you, Iam your helper to get you into your disease")
    st.subheader("How to get started into  these helping service")
    st.write("Choose one of the following Button and start learning about your disease, ask questions or just learn about the other forms of diabetes.")
    st.write("Choosing your type of diabetes is the first step.")
    st.subheader("What do you want to do?")
    st.button("Choose the type of Diabetes", on_click=set_state, args=[1])
    st.button("what is that here?", on_click=set_state, args=[-2])
    st.button("I don't have diabetes, what to do here?", on_click=set_state, args=[-3])
    st.button("direct to the chatbot", on_click=set_state, args=[-1])

if st.session_state.stage == 1:
    st.subheader("If you know which type of diabetes you got, please select.")
    st.button('Type 1 - autoimmune disease', on_click=set_state, args=[2, "autoimmune disease"])
    st.button('Type 2 - insulin resistance', on_click=set_state, args=[2, "insulin resistance"])
    st.button('Type 3', on_click=set_state, args=[2, "3"])
    st.button('Gestational diabetes ', on_click=set_state, args=[2, "gestational"])
    st.button("I don't know", on_click=set_state, args=[-4])
    st.button("back home", on_click=set_state, args=[0])
    st.button("direct to the chatbot", on_click=set_state, args=[-1])


if st.session_state.stage == 2:
    if st.session_state.type == "not known":
        name = st.header(f"Not selected which Type of Diabetes")
    else:
        name = st.header(f"Your Diabetes Type:  {st.session_state.type}")
    #autoimmune disease
    #insulin resistance
    #3
    #gestational


    df = create_data_frame(st.session_state.type)

    st.dataframe(df)


if st.session_state.stage == -4:
    st.button("Home", on_click=set_state, args=[0])

    st.subheader("This 4 tpye exist:")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write_stream(stream_type())
    st.button("direct to the chatbot", on_click=set_state, args=[-1])
if st.session_state.stage == -3:
    st.button("Home", on_click=set_state, args=[0])

    st.subheader("What else?")
    st.write_stream(stream_what_else())
    st.button("direct to the chatbot", on_click=set_state, args=[-1])
if st.session_state.stage == -2:
    st.button("Home", on_click=set_state, args=[0])

    st.subheader("Explanation")
    st.write_stream(stream_explanation)
    st.button("direct to the chatbot", on_click=set_state, args=[-1])
if st.session_state.stage == -1:
    st.button("Home", on_click=set_state, args=[0])
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Diabetes Support"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass)
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)




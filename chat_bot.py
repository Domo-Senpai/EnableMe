import textwrap
import time

import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
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
    st.subheader("What do you want to do?")
    st.button("Choose the type of Diabetes", on_click=set_state, args=[1])
    st.button("what is that here?", on_click=set_state, args=[-2])
    st.button("I don't have diabetes, what to do here?", on_click=set_state, args=[-3])
    st.button("direct to the chatbot", on_click=set_state, args=[-1])

if st.session_state.stage >= 1:
    st.subheader("If you know which type of diabetes you got, please select.")
    st.button('Type 1 - autoimmune disease', on_click=set_state, args=[2, "autoimmune disease"])
    st.button('Type 2 - insulin resistance', on_click=set_state, args=[2, "insulin resistance"])
    st.button('Type 3', on_click=set_state, args=[2, "3"])
    st.button('Gestational diabetes ', on_click=set_state, args=[2, "gestational"])
    st.button("I don't know", on_click=set_state, args=[2])
    st.button("direct to the chatbot", on_click=set_state, args=[-1])


if st.session_state.stage >= 2:
    if st.session_state.type == "not known":
        name = st.header(f"Not selected which Type of Diabetes")
    else:
        name = st.header(f"Your Diabetes Type:  {st.session_state.type}")


###############################################################
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
if st.session_state.stage == -2:
    st.button("Home", on_click=set_state, args=[0])

    st.subheader("Explanation")
    st.write_stream(stream_explanation)
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




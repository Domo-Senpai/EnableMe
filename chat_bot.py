import textwrap
import time

import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import pandas as pd
import numpy as np
type1 = "The question should be interpreted in connection with the background that type 1 autoimmune disease diabetes is prevalent: "
type2 = "The question should be interpreted in connection with the background that type 2 insulin resistance diabetes is prevalent: "
type3 = "The question should be interpreted in connection with the background that type 3 diabetes is prevalent: "
type4 = "The question should be interpreted in connection with the background that Gestational  diabetes is prevalent: "
# Source of the Template/Standardpage Code "https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/"


# Settings of the Mainpage, with Title and a change to the sidebar
st.set_page_config(page_title="🤗💬 Diabetes Helper", initial_sidebar_state="expanded")
# Changing settings of the sidebar
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


# Function to interact with the LLM, hosted by HuggingFace, Login with the secrets.toml file
def generate_response(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

def generate_responsetype1(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    prompt = type1 + prompt_input
    return chatbot.chat(prompt)

def generate_responsetype2(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    prompt = type2 + prompt_input
    return chatbot.chat(prompt)

def generate_responsetype3(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    prompt = type3 + prompt_input
    return chatbot.chat(prompt)

def generate_responsetype4(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    prompt = type4 + prompt_input
    return chatbot.chat(prompt)


# Function to display the explanation of this webapp in a stream
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


def get_diabetes_1():
    df = pd.DataFrame([["autoimmune disease", "The body destroys the insulin-producing cells ", "Often in childhood or adolescence ",
                        "Genetic predisposition and severe viral infection such as mumps in childhood",
                        "Great thirst, tiredness, excessive urination or severe weight loss",
                        "Daily insulin injections necessary", "Approximately five percent of all people affected"]])
    return df


def get_diabetes_2():
    df = pd.DataFrame([["insulin resistance", "Insulin resistance or insufficient insulin production", "Mostly in adulthood",
                        "Genetic predisposition and obesity, too little exercise or an unhealthy, high-sugar diet",
                        "Often only tiredness, weakness, visual disturbances or higher risk of infection",
                        "Healthy diet and exercise, oral medication (tablets) or rarely insulin injections",
                        "Approximately 95 percent of all people affected"]])
    return df


def get_diabetes_3():
    df = pd.DataFrame([["3", "genetic defects, infections or diseases of the pancreas", "-", "-",
                        "chronic increase in blood sugar",
                        "With this type, treatment and therapeutic success are highly dependent on the respective cause. Therapies must therefore be individually adapted",
                        "-"]])
    return df


def get_diabetes_4():
    df = pd.DataFrame([["gestational",
                        "During pregnancy, the body needs more energy and therefore produces more insulin to transport the glucose into the cells. However, sometimes this system does not work properly. This means that the glucose does not enter the cells efficiently and remains in the blood instead. As a result, blood glucose levels remain higher than normal. The mother's increased blood sugar affects the fetus, which reacts by producing more insulin. This leads to increased growth and increased fat deposition in the fetus. This in turn can later increase the risk of obesity and type 2 diabetes in the child. Gestational diabetes usually occurs in the last third of pregnancy and disappears again after the birth. Risk factors for gestational diabetes include obesity, the presence of type 2 diabetes in the family and the age of the mother, especially from 30 years onwards.",
                        "", "",
                        "In most cases, the mother experiences no recognizable symptoms and the typical symptoms of diabetes are not present. However, symptoms that may occur can be similar to those of normal pregnancy symptoms, such as severe thirst, frequent urination and tiredness. However, if the mother had gestational diabetes, newborns often have low blood sugar levels. For more information on diabetes in children, we recommend our article: Diabetes in children: symptoms and treatment.",
                        "With gestational diabetes, there is a slightly increased risk of certain birth complication, particularly because the child may have excessive growth, a s previously mentioned. However, in 85% of cases, a change in diet has proven to be an effective treatment. Similarly, regular exercise, particularly in the form of 'pregnancy-friendly' activities such a s swimming or walking, helps to reduce the risk.",
                        ""]])
    return df


def create_data_frame(number):
    columns = ["Name", "Cause", "Age at diagnosis", "Risk factors", "Symptoms", "Treatment", "Frequency"]
    df = pd.DataFrame()
    if number == 1:
        df = get_diabetes_1()
    elif number == 2:
        df = get_diabetes_2()
    elif number == 3:
        df = get_diabetes_3()
    elif number == 4:
        df = get_diabetes_4()
    df = df.transpose()
    row_titles = ['Names']
    df.index = columns
    df.columns = ["Description"]
    df.index.name = 'characteristic'
    st.subheader("Overview")
    st.dataframe(df)


def visualize_content(dia_type):
    if dia_type == "autoimmune disease":
        col1, col2 = st.columns(2)

        with col1:
            st.button("Home", on_click=set_state, args=[0])

        with col2:

            st.button("Diabetes Type 1 Chatbot", on_click=set_state, args=[10])
        create_data_frame(1)
        st.caption("Type 1 diabetes - autoimmune disease")
        st.write(
            "Type 1 diabetes is an autoimmune disease in which the immune system destroys the insulin-producing cells in the pancreas. As a result, the body can no longer produce insulin, which leads to a deficiency.")
        st.caption("Type 1 diabetes: Cause")
        st.write(
            "Type 1 diabetes has several causes, although there must be a genetic predisposition. In addition, a severe viral infection in childhood, such as mumps or rubella, plays a decisive role. Although this type of diabetes mainly occurs in children and young adults, it can occur at any age.")
        st.write(
            "The cause is that the immune system mistakenly attacks the insulin-producing cells of the pancreas in type 1 diabetes. If this attack leads to more than 90% of these cells being destroyed, an absolute insulin deficiency occurs. Type 1 diabetes is a chronic and incurable disease.")
        st.caption("Type 1 diabetes: Symptoms")
        st.image("Images/diabetes-typ-1-erkennen~-~media--df42eb16--query.webp")
        st.write("Type 1 diabetes can be recognized early on by the following pronounced symptoms:")
        st.write("    -severe thirst")
        st.write("   -Frequent urination")
        st.write("  -In infants and toddlers, wet diapers more often than average at night")
        st.write("   -severe weight loss")
        st.write("    -tiredness")
        st.write("    -fatigue")
        st.caption("Type 1 diabetes: treatment and therapy")
        st.write(
            "People with type 1 diabetes have to inject themselves with insulin every day for the rest of their lives. As yet, there is no cure. How much insulin needs to be injected is calculated by the person affected depending on their blood glucose level. This requires regular monitoring of the blood glucose level with a blood glucose meter. In our article Converting blood sugar, you will find a table for converting your blood sugar levels.")
        st.write(
            "Insulin therapy is often carried out using insulin pens or insulin pumps. The body is then supplied with insulin for up to 24 hours. Insulin therapy is now also possible with so-called 'closed-loop systems'. This is a kind of 'artificial pancreas' with an insulin pump and a sensor that continuously measures the sugar in the subcutaneous fatty tissue.")
        st.write(
            "If type 1 diabetes is not treated, the blood sugar level rises sharply (hyperglycaemia) and there is a high risk of diabetic coma (hyperacidity coma). Type 1 diabetics or other diabetics who have to inject insulin regularly also have an increased risk of suffering diabetic shock.")
    elif dia_type == "insulin resistance":
        col1, col2 = st.columns(2)

        with col1:
            st.button("Home", on_click=set_state, args=[0])

        with col2:

            st.button("Diabetes Type 2 Chatbot", on_click=set_state, args=[20])
        create_data_frame(2)
        st.caption("Type 2 diabetes - insulin resistance")
        st.write("Type 2 diabetes is a metabolic disease in which the body either does not produce enough insulin or the insulin that is produced cannot be used effectively. It typically develops in adulthood.")
        st.caption("Type 2 diabetes: Cause")
        st.write("In type 2 diabetes, the production of insulin by the pancreas is insufficient or the body cannot use it effectively to convert blood sugar into energy, which is known as insulin resistance. Around 95 percent of all diabetes cases are type 2. A genetic predisposition can play a role, similar to type 1.")
        st.write("Type 2 diabetes usually occurs in adults and older people, with an unhealthy lifestyle characterized by little exercise and obesity being the main cause. In recent years, however, there has been an increase in type 2 diabetes in overweight children and adolescents. This underlines the importance of a healthy lifestyle for the prevention of this disease, which is not limited to older age groups.")
        st.caption("Type 2 diabetes: Symptoms")
        st.image("Images/diabetes-typ-2-erkennen~-~media--df42eb16--query.webp")
        st.write("In the initial phase of type 2 diabetes, there are often only symptoms such as")
        st.write("                 -fatigue")
        st.write("                 -weakness")
        st.write("                 -visual disturbances")
        st.write("                 -Higher risk of infection")
        st.write("                 -Poor wound healing (wounds heal more slowly)")
        st.write("As these symptoms are unspecific, it often takes several years before type 2 diabetes is diagnosed. As a result, many people with diabetes do not even know that they have the disease. If you think you might have type 2 diabetes, you should consult your family doctor. The specialist will carry out various tests, for example to check your long-term blood glucose level and confirm the diagnosis.")
        st.caption("Type 2 diabetes: treatment and therapy")
        st.write("Type 2 treatment consists of a balanced diet, regular exercise and a reduction in body weight. If the elevated blood sugar levels cannot be normalized through a change in lifestyle, oral ant idiabetic drugs (tablets) are administered. If oral antidiabetics are also not sufficient, insulin therapy is necessary, just as with type 1.")
        st.write("Untreated type 2 diabetes, especially in older people, can lead to severely elevated blood sugar levels (hyperglycaemia) over time. There is then a risk of a diabetic coma (dehydration coma).")
    elif dia_type == "3":
        col1, col2 = st.columns(2)

        with col1:
            st.button("Home", on_click=set_state, args=[0])

        with col2:

            st.button("Diabetes Type 3 Chatbot", on_click=set_state, args=[30])
        create_data_frame(3)
        st.caption("Type 3 diabetes - secondary forms of diabetes or other types of diabetes")
        st.write("Type 3 diabetes includes all forms of diabetes that do not fall under type 1 or type 2. Like the other types, however, this also involves a chronic increase in blood sugar.")
        st.caption("Type 3 diabetes: Cause")
        st.write("Since 2019, other rare forms of diabetes mellitus have been summarized under the term 'secondary forms of diabetes' or 'other types of diabetes'. These forms are characterized by mixtures of different features. The causes can be genetic defects, infections or diseases of the pancreas.")
        st.caption("Type 3 diabetes: treatment and therapy")
        st.write("With this type, treatment and therapeutic success are highly dependent on the respective cause. Therapies must therefore be individually adapted.")

    elif dia_type == "gestational":
        col1, col2 = st.columns(2)

        with col1:
            st.button("Home", on_click=set_state, args=[0])

        with col2:

            st.button("Diabetes Type 4 Chatbot", on_click=set_state, args=[40])
        create_data_frame(4)
        st.caption("Type 4 diabetes - gestational or gestational diabetes")
        st.write("Type 4 diabetes involves elevated blood sugar, which is first detected during pregnancy and is triggered by excess insulin production. Gestational diabetes is one of the most common complications of pregnancy and can lead to later health problems for the child.")
        st.caption("Type 4 diabetes: Cause")
        st.write("During pregnancy, the body needs more energy and therefore produces more insulin to transport the glucose into the cells. However, sometimes this system does not work properly. This means that the glucose does not enter the cells efficiently and remains in the blood instead. As a result, blood glucose levels remain higher than normal.")
        st.write("The mother's increased blood sugar affects the fetus, which reacts by producing more insulin. This leads to increased growth and increased fat deposition in the fetus. This in turn can later increase the risk of obesity and type 2 diabetes in the child.")
        st.write("Gestational diabetes usually occurs in the last trimester of pregnancy and disappears again after the birth. Risk factors for gestational diabetes include obesity, the presence of type 2 diabetes in the family and the age of the mother, especially from the age of 30.")
        st.caption("Type 4 diabetes: symptoms")
        st.write("In most cases, the mother experiences no recognizable symptoms and the typical symptoms of diabetes are not present. However, symptoms that may occur can be similar to those of normal pregnancy symptoms, such as severe thirst, frequent urination and fatigue.")
        st.write("However, if the mother had gestational diabetes, newborns often have low blood sugar levels. For more information on diabetes in children, we recommend our article: Diabetes in children: symptoms and treatment.")
        st.caption("Type 4 diabetes: treatment and therapy")
        st.write("With gestational diabetes, there is a slightly increased risk of certain birth complications, particularly because the child may have excessive growth, a s previously mentioned.")
        st.write("In 85% of cases, however, a change in diet has proven to be an effective treatment. Regular exercise, especially in the form of 'pregnancy-friendly' activities such as swimming or walking, also helps to reduce the risk.")

    else:
        st.write("Error appeared")


# Setting up all components of the sidebar, with title, login check, video-frame(expandabale) and links to the website to enableme
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
    st.markdown(
        '📖 Learn more about [diabetes](https://www.enableme.de/de/behinderungen/diabetes-mellitus-eine-storung-des-blutzuckerstoffwechsels-1182) or other [disabilities](https://www.enableme.de/de/behinderungen) !')
    with st.expander("Explanation Video"):
        VIDEO_URL = "https://www.youtube.com/watch?v=RiCzvzPL72E"
        st.video(VIDEO_URL)
# Setting up states to move between the possibility tree structure and holding the choosen type of Diabetes
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'type' not in st.session_state:
    st.session_state.type = "not known"


def set_state(i, type_of_diabetes="not known", possible_diabetes=None):
    st.session_state.stage = i
    st.session_state.type = type_of_diabetes
    st.session_state.possible_diabetes = possible_diabetes

def check_values(q1,q2,q3,q4,q5,q6,q7,q8, q9, q10):
    list_of_possiblities = []
    if (q1 == "Yes" and q2 == "Yes" and q3 == "Yes") or (q1 == "Yes" and q8 == "Low (less than 30 minutes per day"):
        list_of_possiblities.append("autoimmune disease")
    if (q1 == "Yes" and q2 == "Yes" and q3 == "Yes" and q4 == "Yes") or q8 == "Moderate (30-60 minutes per day)" or q8 == "High (more than 60 minutes per day)":
        list_of_possiblities.append("insulin resistance")
    if q1 == "Yes" and q5 == "Yes" and q6 == "Yes" and q7 == "Yes" and q9 == "Yes":
        list_of_possiblities.append("gestational")
    if q10 == "Yes":
        list_of_possiblities.append("3")
    return list_of_possiblities

# Starting in the section of choosing what to do
if st.session_state.stage == 0:
    st.header("Hello you, Iam your helper to get you into your disease")
    st.subheader("How to get started into  these helping service")
    st.write(
        "Choose one of the following Button and start learning about your disease, ask questions or just learn about the other forms of diabetes.")
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
    # autoimmune disease
    # insulin resistance
    # 3
    # gestational

    visualize_content(st.session_state.type)


if st.session_state.stage == -4:
    col1, col2 = st.columns(2)

    with col1:
        st.button("Home", on_click=set_state, args=[0])

    with col2:
        st.button("direct to the chatbot", on_click=set_state, args=[-1])
    q1 = st.radio(
        "Have you felt increasingly thirsty recently? ",
        ["Yes", "No"])
    q2 = st.radio(
        "Do you suffer from frequent urination?",
        ["Yes", "No"])
    q3 = st.radio(
        "Have you lost weight recently even though you eat normally?",
        ["Yes", "No"])
    q4 = st.radio(
        "Do you have any family members who already suffer from diabetes?",
        ["Yes", "No"])
    q5 = st.radio(
        "Have you recently experienced an increased appetite?",
        ["Yes", "No"])
    q6 = st.radio(
        "Do you suffer from increased tiredness or weakness?",
        ["Yes", "No"])
    q7 = st.radio(
        "Have you noticed any visual disturbances recently? ",
        ["Yes", "No"])
    q8 = st.radio(
        "How would you describe your physical activity?",
        ["Low (less than 30 minutes per day)", "Moderate (30-60 minutes per day)", "High (more than 60 minutes per day)"])
    q9 = st.radio(
        "Are you pregnant",
        ["Yes", "No"])
    q10 = st.radio(
        "Do you have damage to the pancreas or pancreatitis or pancreatic cancer?",
        ["Yes", "No"])

    possible_values = []

    possible_values = check_values(q1,q2,q3,q4,q5,q6,q7,q8, q9, q10)
    st.button("Submit", on_click=set_state, args=[99, "not known",possible_values])


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
if st.session_state.stage == 10:
    st.header("Ask Question you need to know")
    st.subheader("Chat with the Bot about your Autoimmune disease Diabetes")
    st.button("Home", on_click=set_state, args=[0])
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Autoimmune disease Diabetes Type 1 Support"}]

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
                response = generate_responsetype1(prompt, hf_email, hf_pass)
                #response = response["response"].replace(type1, "")
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
if st.session_state.stage == 20:
    st.header("Ask Question you need to know")
    st.subheader("Chat with the Bot about your Insulin resistance Diabetes")
    st.button("Home", on_click=set_state, args=[0])
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Insulin resistance Diabetes Type 2 Support"}]

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
                response = generate_responsetype2(prompt, hf_email, hf_pass)
                response = response["response"].replace(type2, "")
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
if st.session_state.stage == 30:
    st.header("Ask Question you need to know")
    st.subheader("Chat with the Bot about your Type 3 Diabetes")
    st.button("Home", on_click=set_state, args=[0])
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Diabetes Type 3 Support"}]

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
                response = generate_responsetype3(prompt, hf_email, hf_pass)
                response = response["response"].replace(type3, "")
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
if st.session_state.stage == 40:
    st.header("Ask Question you need to know")
    st.subheader("Chat with the Bot about your Gestational Diabetes")
    st.button("Home", on_click=set_state, args=[0])
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Gestational Diabetes Support"}]

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
                response = generate_responsetype4(prompt, hf_email, hf_pass)
                response = response["response"].replace(type4, "")
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

if st.session_state.stage == 99:

    col1, col2 = st.columns(2)

    with col1:
        st.button("Home", on_click=set_state, args=[0])

    with col2:
        st.button("direct to the chatbot", on_click=set_state, args=[-1])
    st.header("The possible Diabetes Types you got:")
    st.subheader("Choose one to learn more about it, if there is a multiple choice you have to remember them to choose again if the first choosen wasnt the right one, after going back to home. ")
    if "autoimmune disease" in st.session_state.possible_diabetes:
        st.button('Type 1 - autoimmune disease', on_click=set_state, args=[2, "autoimmune disease"])
    if "insulin resistance" in st.session_state.possible_diabetes:
        st.button('Type 2 - insulin resistance', on_click=set_state, args=[2, "insulin resistance"])
    if "3" in st.session_state.possible_diabetes:
        st.button('Type 3', on_click=set_state, args=[2, "3"])
    if "gestational" in st.session_state.possible_diabetes:
        st.button('Gestational diabetes ', on_click=set_state, args=[2, "gestational"])
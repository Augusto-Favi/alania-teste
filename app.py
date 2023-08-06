from langchain.embeddings import OpenAIEmbeddings
import streamlit as st
import os
from PIL import Image
import streamlit.components.v1 as components
from streamlit_chat import message as st_message
from datetime import datetime
import hashlib
import random
import base64
import time

st.set_page_config(
    page_title="AlanIA",
    page_icon="👩🏻‍🦰",
)

if "session_unique_key" not in st.session_state:
    st.session_state.session_unique_key = f"{hashlib.sha256(('unique-key-'+str(random.random())).encode()).hexdigest()}-{datetime.now()}"
if "current_path" not in st.session_state:
    st.session_state.current_path = os.path.realpath(os.path.dirname(__file__))
if "history" not in st.session_state:
    st.session_state.history = []
    
logo = Image.open(f'{st.session_state.current_path}/images/logo.png')

def generate_answer():
    user_message = st.session_state.input_text
    st.session_state.input_text = ""

    response, sources = st.session_state.conversational_bot.inference(user_message, st.session_state.session_unique_key)

    st.session_state.pdf_source = sources[0].replace("data_src", "../Base-Conhecimento").replace(".md", ".pdf")
    print('pdf_source: ', st.session_state.pdf_source)


    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": response, "is_user": False})
    

def gpt3_app():

    # st.image(logo)

    st.title("AlanIA")
    
    for chat in st.session_state.history:
        st_message(**chat)  # unpacking
    
    st.text_input("Fale com o robo", key="input_text", on_change=generate_answer)

    if st.button("LIMPAR"):

            st.session_state.history = []
            st.session_state.pdf_source = "Vazio"
            st.session_state.session_unique_key = f"{hashlib.sha256(('unique-key-'+str(random.random())).encode()).hexdigest()}-{datetime.now()}"

            st.experimental_rerun()
        
    time.sleep(0.15)
    components.html(
        f"""
            <!--{len(st.session_state.history)}-->
            <script>
                var objDiv = window.parent.document.querySelector('section.main');
                objDiv.scrollTop = objDiv.scrollHeight;
            </script>
        """,
        height=0
    )


gpt3_app()
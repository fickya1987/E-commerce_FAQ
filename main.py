import streamlit as st
from langchain_helper import create_vectordb, get_response

# For Streamlit
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

st.markdown("""
<style>
    #MainMenu
    {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
Made by [Ficky Alkarim - Gaman](https://github.com/fickya1987)\n
""", unsafe_allow_html=True)
st.title("Lestari Bahasa Kita")

st.markdown("""
Bagi para pecinta bahasa daerah di seluruh indonesia, Kami menyediakan fitur Tanya Jawab AI untuk memudahkan Anda dalam belajar bahasa daerah.
Anda dapat melihat panduannya pada [Panduan Tanya Jawab GAMAN AI](https://github.com/fickya1987/E-commerce_FAQ/blob/main/Ecommerce_FAQs.csv)
dan Anda dapat juga bertanya dengan pertanyaan lain yang sesuai dengan template yang diberikan tersebut.\n
***"Silahkan Bertanya!"*** , etc.
""", unsafe_allow_html=True)

query = st.text_input("Pertanyaan: ")

if query:
    response = get_response(query)

    st.header(" Lestari Bahasa menjawab: ")
    st.write(response)

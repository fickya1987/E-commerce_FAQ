# Import necessary libraries
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

# Set up the model
load_dotenv()
generation_config = {
    "temperature": 0.9,
}
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
llm = genai.GenerativeModel(model_name="gemini-1.5-flash-001", generation_config=generation_config)

# Vector Embedding
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.environ["GOOGLE_API_KEY"])


def create_vectordb():
    # Load data from CSV file
    loader = CSVLoader(file_path='FAQ_Basa_Sunda.csv', encoding='cp1252', source_column='prompt')
    documents = loader.load()
    vectordb = Chroma.from_documents(documents,
                                     embedding=embeddings,
                                     persist_directory='./ChromaDB')
    vectordb.persist()


def get_response(query):
    vectordb = Chroma(persist_directory="ChromaDB", embedding_function=embeddings)
    retriever = vectordb.as_retriever()

    # Prompt template
    prompt_template = """ Merujuk pada konteks dan pertanyaan yang telah ada, berikan jawaban dari pertanyaan yang ditanyakan. Dalam menjawab pertanyaan, lihat bagian "prompt" dan berikan jawaban sesuai dengan kolom bagian "response" tanpa banyak dirubah-rubah narasinya. Apabila tidak tahu, ucapkan saja saya tidak tahu atau silahkan tanya pertanyaan lain.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}

    # Chat model and Chain
    chat = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.9)
    chain = load_qa_chain(chat, chain_type="stuff", prompt=PROMPT)

    # Query
    # query = "how long is the shipping and can I cancel my order?"
    response = \
        chain.invoke({"input_documents": retriever.get_relevant_documents(query), "question": query},
                     return_only_outputs=True)['output_text']
    return response


if __name__ == '__main__':
    # create_vectordb()
    print(get_response("shipping duration?"))

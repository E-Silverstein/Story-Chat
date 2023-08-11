import os

import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

openai_api_key = os.environ['OPENAI_KEY']

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container.expander("Context Retrieval")

    def on_retriever_start(self, query: str, **kwargs):
        self.container.write(f"**Question:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        # self.container.write(documents)
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.container.write(f"**Document {idx} from {source}**")
            self.container.markdown(doc.page_content)

books = {
    'Alice In Wonderland': ['embeddingsbooks/Alice_In_Wonderland.txt', ['Alice', 'The White Rabbit', 'The Queen of Hearts', 'The King of Hearts', 'The Mad Hatter']],
    'A Doll\'s House': ['embeddingsbooks/Doll_House.txt', ['Nora Helmer', 'Torvald Helmer', 'Dr. Rank', 'Mrs. Linde', 'Krogstad']],
    'Frankenstein; or, The Modern Prometheus': ['embeddingsbooks/Frankenstein.txt', ['Victor Frankenstein', 'The Monster', 'Robert Walton', 'Elizabeth Lavenza', 'Henry Clerval']],
    'The Great Gatsby': ['embeddingsbooks/Gatsby.txt', ['Nick Carraway', 'Jay Gatsby', 'Daisy Buchanan', 'Tom Buchanan', 'Jordan Baker']],
    'Adventures of Huckleberry Finn': ['embeddingsbooks/Huckleberry_Finn.txt', ['Huckleberry Finn', 'Tom Sawyer', 'Jim', 'Pap Finn', 'The Duke']],
    'Romeo and Juliet': ['embeddingsbooks/Romeo_and_Juliet.txt', ['Romeo', 'Juliet', 'Friar Laurence', 'Mercutio', 'Tybalt']],
}

st.title('Story Chat')
st.write('This is a story chat app. You can chat with characters from various stories.')
st.info('This is a beta version. Please be patient with the bot.')


st.subheader('Please type your character\'s name and click on the button below to start the chat.')
book = st.selectbox('Book', ['Alice In Wonderland', 'A Doll\'s House', 'Frankenstein; or, The Modern Prometheus', 'The Great Gatsby', 'Adventures of Huckleberry Finn', 'Romeo and Juliet'])
character_name = st.selectbox('Character', books[book][1] )
file_name = books[book][0]
question = st.text_input('Question', 'Ask me anything!')
start = st.button(label = 'Start Chat')

db = Chroma(persist_directory=books[book][0], embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key))
retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=.5, streaming=True), retriever=retriever)

if start:   
    query = "You will act as " + character_name+  " from "  + book + ". You will speak to me as if you where them. Question: " + question + character_name + ":"
    response = qa.run(query)
    st.success(character_name + ": " + response)

from langchain.document_loaders import TextLoader
import os

txt = TextLoader("data/gen_ai.txt")
txt_docs = txt.load()

# recursive text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1600, chunk_overlap=200)
docs = splitter.split_documents(txt_docs)

# chroma db
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

embedding = OllamaEmbeddings(model="nomic-embed-text:latest")
persist_directory = "outputs/ga_db/chroma/"

if os.path.exists(persist_directory):
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding)
else:
    db = Chroma.from_documents(docs, embedding, persist_directory=persist_directory)


db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Create a OllamaModel model
from langchain_ollama.llms import OllamaLLM
model = OllamaLLM(model="phi3.5")

# Contextualize question prompt
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)

# Create a prompt template for contextualizing questions
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
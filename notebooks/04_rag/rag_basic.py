# loading text file
from langchain_community.document_loaders import TextLoader
txt = TextLoader("data/super_hero.txt")

txt_docs = txt.load()
print(txt_docs[0])


# web page loader
from langchain_community.document_loaders import WebBaseLoader
import bs4


webLoader = WebBaseLoader(web_paths=(["https://lilianweng.github.io/posts/2023-06-23-agent/"]), bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=['post-title', 'post-content', 'post-header'])))

web_docs = webLoader.load()
print(web_docs)

# loading pdf file
from langchain_community.document_loaders import PyPDFLoader


pdfLoader = PyPDFLoader('data/attention is all you need.pdf')
pdf_docs = pdfLoader.load()
print(pdf_docs)


#--------------------------------------------
# TEXT SPLITTER
#--------------------------------------------

# recursive text splitter

from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1600,chunk_overlap=200)
docs = splitter.split_documents(txt_docs)

# len(docs)

#--------------------------------------------
# TEXT EMBEDDINGS
#--------------------------------------------

# chroma db
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

embedding = OllamaEmbeddings(model='nomic-embed-text:latest')
persist_directory = 'output/db/chroma/'

if os.path.exists(persist_directory):
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding)
else:
    db = Chroma.from_documents(docs, embedding, persist_directory=persist_directory)


query = "What does superheros use their powers for?"
res = db.similarity_search(query)
# query = "Who are authors of attention is all you need research paper?"
# res = db.similarity_search(query)

res

#--------------------------------------------
# Faiss db

# from langchain.vectorstores import FAISS
# fdb = FAISS.from_documents(docs, embedding)

# fdb.save_local('output/db/faiss/')
# res = fdb.similarity_search(query)
# res

# fdb2 = FAISS.load_local(folder_path='output/db/faiss/index.faiss',embeddings=embedding)

# ----------------------------------------------
# retriever
# ----------------------------------------------

from langchain_ollama.llms import OllamaLLM

llm = OllamaLLM(model ='phi3.5:latest')

# chat template
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context. Think step by step properly before providing answer. I will tip $1000 if I find answer helpful.
<context>
{context}
</context>                                         
Question: {input}
                                          """)

prompt.invoke({'context':"This is a test context",'input':"what is your name?"})

# chain
from langchain.chains.combine_documents import create_stuff_documents_chain

doc_chain = create_stuff_documents_chain(llm,prompt)

# retriever
retriever = db.as_retriever()

retriever

# retriever chain
from langchain.chains.retrieval import create_retrieval_chain
import os

retriever_chain = create_retrieval_chain(retriever,doc_chain)

res = retriever_chain.invoke({"input":"What does the superheros uses their super powers for?"})
res['answer']
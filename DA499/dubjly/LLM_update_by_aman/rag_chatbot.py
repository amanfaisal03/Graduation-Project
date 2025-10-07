from LLM_Online import * 
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq


class RAG_System:
    def __init__(self, video_text, api_key="k_BKbu896AjrZq9RPjI3AsWGdyb3FYj52pYGChMT5A8aL4L4OVwARc"):
     
        self.llm_text = Full_LLM(Text=video_text)
        self.text = self.llm_text.C_Text  
        self.api_key = api_key
      

    def split_text(self, text, chunk_size=1000, chunk_overlap=200):
        """Split the text into smaller chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
        )
        docs = text_splitter.create_documents([text])
        print(f"{len(docs)} chunks created from the text.")
        return docs


    def chunk_to_Embeddings(self):
        """Create embeddings model."""
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return embeddings


    def Vector_Store(self, chunks, embeddings):
        """Create a vector store from the text."""
        db = Chroma.from_texts(chunks, embedding=embeddings, persist_directory="./db")
        return db

    def persist_vector_store(self, db):
        """Persist the vector store to disk."""
        db.persist()
        print("Vector store persisted to disk.")

    def llm_Initialization(self):
        """Initialize the LLM."""
        llm = ChatGroq(model="qwen-2.5-32b", temperature=0, api_key=self.api_key)
        return llm

    def Retriever(self, vector_store, llm):
        """Create a retriever from the vector store."""
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever())
        return qa_chain

    def RAG_Chatbot(self, retriever, question):
        """Answer a question using the RAG system."""
        answer = retriever.run(question)
        print("\n💬 الإجابة:\n", answer)
        return answer
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
import boto3

import json
import os
import sys


# bedrock client

bedrock = boto3.client(service_name = 'bedrock-runtime')
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)


def data_ingestion():
    loader=PyPDFDirectoryLoader("./data")
    documents = loader.load()
    
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 1000 )
    text_splitter.split_documents(documents)
    
    docs = text_splitter.split_documents(documents)
    
    return docs

def get_vector_store(doc):
    vector_store_faiss = FAISS.from_documents(doc, BedrockEmbeddings)
    vector_store_faiss.save_local("faiss_index")


if __name__ == '__main__':
    docs = data_ingestion()
    get_vector_store(docs)
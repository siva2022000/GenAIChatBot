from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from bs4 import BeautifulSoup
import json
import os
from markdown import markdown

model = SentenceTransformer('all-MiniLM-L6-v2')

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'model_files')
CHUNKS_FILE = os.path.join(RESOURCES_DIR, 'chunks.json')
INDEX_FILE = os.path.join(RESOURCES_DIR, 'faiss_index.index')
os.makedirs(RESOURCES_DIR, exist_ok=True)

def preprocess_handbook(directory):
    chunks = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    md_content = f.read()
                    plain_text = markdown(md_content)  # Convert Markdown to plain text
                    soup = BeautifulSoup(plain_text, "html.parser")
                    chunks.append(soup.get_text()) 

    print(chunks[0])
    print(len(chunks))
    #Generate embeddings for each chunk
    embeddings = model.encode(chunks) 

    #Create a FAISS index
    embedding_dim = embeddings.shape[1] 
    index = faiss.IndexFlatL2(embedding_dim)  
    index.add(embeddings) 

    print(f"FAISS index has {index.ntotal} vectors.")

    with open(CHUNKS_FILE, 'w') as f:
        json.dump(chunks, f)

    faiss.write_index(index, INDEX_FILE)





def extractAnswerSummary(query):
    print(query)

    with open(CHUNKS_FILE, 'r') as f:
        data_chunks = json.load(f)
    
    data_chunks[10]

    index = faiss.read_index(INDEX_FILE)

    # Encode the query into an embedding
    query_embedding = model.encode([query])  # Shape: (1, embedding_dim)

    #Perform similarity search
    k = 3  # Number of most similar chunks to retrieve
    distances, indices = index.search(query_embedding, k)

    # Step 3: Retrieve and print the results
    print("Top results:")
    for idx, distance in zip(indices[0], distances[0]):
        print(idx)
        print(data_chunks[idx])
    return "done"

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from bs4 import BeautifulSoup
import json
import os
from markdown import markdown
import requests
import git

model = SentenceTransformer('all-MiniLM-L6-v2')

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'resources')
MODEL_FILES_DIR = os.path.join(RESOURCES_DIR, 'model_files')
REPOS_DIR = os.path.join(RESOURCES_DIR, 'repos')
os.makedirs(RESOURCES_DIR, exist_ok=True)
os.makedirs(MODEL_FILES_DIR, exist_ok=True)
os.makedirs(REPOS_DIR, exist_ok=True)   
CHUNKS_FILE = os.path.join(MODEL_FILES_DIR, 'chunks.json')
INDEX_FILE = os.path.join(MODEL_FILES_DIR, 'faiss_index.index')

def fetch_resources():
    chunks = []
    resources = json.loads(os.getenv("RESOURCES"))
    for resource in resources:
        print(f'Fetching resources from {resource["repo"]}')
        local_repo_dir = os.path.join(REPOS_DIR, resource["fName"])
        if not os.path.exists(local_repo_dir):
            git.Repo.clone_from(resource["repo"], local_repo_dir)
        print(f'Repository {resource["repo"]} cloned to {local_repo_dir}')
        source_dir = os.path.join(local_repo_dir, resource["sourcePath"])
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        md_content = f.read()
                        plain_text = markdown(md_content)  # Convert Markdown to plain text
                        soup = BeautifulSoup(plain_text, "html.parser")
                        chunks.append(soup.get_text()) 
        print(f'{len(chunks)} chunks fetched from {resource["repo"]}')
    return chunks

def preprocess_resources():
    chunks = fetch_resources()

    print("Generating embeddings")
    #Generate embeddings for each chunk
    embeddings = model.encode(chunks) 

    #Create a FAISS index
    embedding_dim = embeddings.shape[1] 
    index = faiss.IndexFlatL2(embedding_dim)  
    index.add(embeddings) 

    print("Saving chunks and index")
    with open(CHUNKS_FILE, 'w') as f:
        json.dump(chunks, f)

    faiss.write_index(index, INDEX_FILE)

def generate_summary(query, relevant_chunks, model_name="text-bison"):
    # Construct the endpoint URL
    endpoint = os.getenv("LLM_ENDPOINT") + os.getenv("LLM_API_KEY")

    # Combine relevant chunks into a single input
    chunks_text = "\n".join([f"- {chunk}" for chunk in relevant_chunks])
    prompt = f"""
    Query: {query}
    Relevant Chunks:
    {chunks_text}
    Summarize the answer to the query based on the relevant chunks. Don't include any other information.
    """

    # Set up the request payload
    payload = {"contents":[{"parts":[{"text":prompt}]}]}

    # Set up the headers
    headers = {
        "Content-Type": "application/json", 
    }

    # Send the POST request
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

    # Parse and return the response
    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Answer extraction failed"


def extractAnswerSummary(query):

    with open(CHUNKS_FILE, 'r') as f:
        data_chunks = json.load(f)
    
    data_chunks[10]

    index = faiss.read_index(INDEX_FILE)

    # Encode the query into an embedding
    query_embedding = model.encode([query])  # Shape: (1, embedding_dim)

    #Perform similarity search
    k = 5# Number of most similar chunks to retrieve
    distances, indices = index.search(query_embedding, k)

    result = []
    # Step 3: Retrieve and print the results
    for idx, distance in zip(indices[0], distances[0]):
        result.append(data_chunks[idx])
    answer = generate_summary(query, result)
    return answer           
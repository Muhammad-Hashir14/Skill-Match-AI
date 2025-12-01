from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
import os
from langchain.schema import Document
from werkzeug.utils import secure_filename
import numpy as np


def load_doc(resumes):
    docs = []
    for filepath in resumes:
        loader = PyPDFLoader(filepath)
        pages = loader.load()
        full_text = "\n".join([p.page_content for p in pages])
        docs.append(Document(page_content=full_text, metadata={"source": filepath}))
    return docs


def load_HF_Embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings


def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


def find_perc(results, jd_embedding, embeddings):
    ranks = []
    for doc, _ in results:
        resume_vec = embeddings.embed_query(doc.page_content)
        raw_sim = cosine_similarity(jd_embedding, resume_vec)
        sim = ((raw_sim + 1) / 2) * 100   # convert to 0–100%
        ranks.append({
            "Resume": os.path.basename(doc.metadata["source"]),
            "Similarity": round(sim, 2)
        })
    return ranks


def get_max_similarity(resume_list):
    if not resume_list:
        return None  # Return None if list is empty

    max_resume = max(resume_list, key=lambda x: x['Similarity'])
    return max_resume

def find_content(results, best_resume):
    for doc, _ in results:
        if os.path.basename(doc.metadata["source"]) == best_resume["Resume"]:
            return doc.page_content
    return ""


def maketempdir(resumes):
    saved_files=[]
    tempdir = os.path.join(os.getcwd(),"tempdir")
    os.makedirs(tempdir, exist_ok=True)
    for file in resumes:
        if file and file.filename.endswith(".pdf"):
            filename = secure_filename(file.filename)
            save_path = os.path.join(tempdir,filename)
            file.save(save_path)
            saved_files.append(save_path)
    
    print(saved_files)
    return tempdir, saved_files
        
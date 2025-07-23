from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
import os
from werkzeug.utils import secure_filename


def load_doc(resumes):
    text = []
    for filepath in resumes:
        loader = PyPDFLoader(filepath)
        text.extend(loader.load())
    return text

def load_HF_Embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

def l2_to_similarity(distance):
    # Assume max possible distance ≈ 2 for normalized vectors
    similarity = 1 - min(distance / 2, 1)
    return round(similarity * 100, 2)

def find_perc(results):
    ranks = []
    for doc, score in results:
        ranks.append({
            "Resume": os.path.basename(doc.metadata["source"]),
            "Similarity": l2_to_similarity(score)
        })
    return ranks

def get_max_similarity(resume_list):
    if not resume_list:
        return None  # Return None if list is empty

    max_resume = max(resume_list, key=lambda x: x['Similarity'])
    return max_resume

def find_content(results, br):
    for doc,number in results:
        if br["Resume"] == os.path.basename(doc.metadata["source"]):
            print(br["Resume"])
            content = doc.page_content
    return content

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
        
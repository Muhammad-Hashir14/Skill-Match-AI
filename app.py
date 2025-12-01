from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from langchain.embeddings import HuggingFaceEmbeddings
from src.helper import (
    maketempdir,
    load_doc,
    load_HF_Embeddings,
    find_perc,
    get_max_similarity,
    find_content
)
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
import os
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import getpass
from src.prompt import resume_analysis_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
import markdown
import tempfile


load_dotenv()

app = Flask(__name__)
embeddings = load_HF_Embeddings()


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("base.html")

@app.route("/results", methods=["GET", "POST"])
def upload_resumes():

    resumes = request.files.getlist('resumes')
    jd = request.form.get("job_description")
    
    # tempdir, saved_files = maketempdir(resumes)
    # print(tempdir)
    with tempfile.TemporaryDirectory() as tempdir:
        saved_files = []
        for resume in resumes:
            filename = secure_filename(resume.filename)
            file_path = os.path.join(tempdir, filename)
            resume.save(file_path)
            saved_files.append(file_path)
            print(file_path)
        text = load_doc(saved_files)
    
        
        # uuids = [str(uuid4()) for _ in range(len(text))]
        vector_store = FAISS.from_documents(text, embeddings)
        print("this is vector store")
        print(vector_store)
        jd_embedding=embeddings.embed_query(jd)
        top_k = len(saved_files)
        print(top_k)
        results = vector_store.similarity_search_with_score_by_vector(jd_embedding, k=top_k)
        print(results)

        # calculate correct cosine similarity ranking
        ranks = find_perc(results, jd_embedding, embeddings)

        top_resume = get_max_similarity(ranks)
        content = find_content(results, top_resume)

        prompt = resume_analysis_prompt(content, top_resume["Similarity"])

        result = llm(prompt)
        print(result)
        output = markdown.markdown(result.content)

    return render_template("results.html", ranks = ranks, output = output, jd=jd)


if __name__=="__main__":
    app.run(debug=True)
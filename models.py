from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from utils import cargar_pdf

# Cargar PDF
texto = cargar_pdf("uploads/Codigo-PENAL_12-NOV-1874.pdf")

# Dividir texto
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_text(texto)

# Crear embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_texts(chunks, embeddings)

# Modelo local (Qwen2.5 desde Hugging Face)
generator = pipeline("text-generation", model="Qwen/Qwen2-7B-Instruct", trust_remote_code=True)

def responder_pregunta(pregunta):
    docs = db.similarity_search(pregunta, k=3)
    contexto = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
Contexto:
{contexto}

Pregunta:
{pregunta}

Instrucción: Responde únicamente basándote en el contexto proporcionado. Si no hay información suficiente, di que no puedes ayudar.
Respuesta:
"""

    output = generator(prompt, max_new_tokens=200)
    return output[0]['generated_text'].replace(prompt, "").strip()
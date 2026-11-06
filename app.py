
import chromadb
import streamlit as st
from openai import OpenAI
from sentence_transformers import SentenceTransformer


REPLI = "Je ne trouve pas cette information dans la documentation."

@st.cache_resource                       # charge le modèle et la base une seule fois
def charger():
    modele = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    collection = chromadb.PersistentClient(path="base_vectorielle").get_collection("altea")
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    return modele, collection, client

modele, collection, client = charger()

def rechercher(question, k=3):
    res = collection.query(query_embeddings=modele.encode([question]).tolist(), n_results=k)
    return [{"texte": t, "source": m["source"], "page": m["page"]}
            for t, m in zip(res["documents"][0], res["metadatas"][0])]

def repondre(question, k=3):
    extraits = rechercher(question, k)
    contexte = "".join(f"[{i}] ({e['source']}, page {e['page']})\n{e['texte']}\n\n"
                       for i, e in enumerate(extraits, start=1))
    prompt = f"""Tu es l'assistant interne d'Altéa Services.
Réponds à la question en utilisant UNIQUEMENT les extraits ci-dessous.
Après chaque information, indique le numéro de l'extrait entre crochets, par exemple [1].
Si les extraits ne contiennent pas la réponse, réponds exactement : "{REPLI}"

Extraits :
{contexte}
Question : {question}
Réponse :"""
    reponse = client.chat.completions.create(
        model="llama3.2", temperature=0,
        messages=[{"role": "user", "content": prompt}])
    return reponse.choices[0].message.content, extraits

st.title("Assistant documentaire Altéa")
question = st.text_input("Votre question")

if question:
    with st.spinner("Recherche dans la documentation…"):
        reponse, extraits = repondre(question)
    st.write(reponse)
    st.subheader("Sources")
    for i, e in enumerate(extraits, start=1):
        with st.expander(f"[{i}] {e['source']}, page {e['page']}"):
            st.write(e["texte"])
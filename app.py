# import streamlit as st 
# from groq import Groq
# from rag_engine import load_and_chunk , build_index , retrieve 



# # ── Configuration de la page ────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Assistant Boutique",
#     page_icon="🛍️",
#     layout="centered",
# )


# # ── Constantes ──────────────────────────────────────────────────────────────
# BOUTIQUE_FILE = "documentation_boutique.txt"
# GROQ_MODEL = "llama-3.1-8b-instant"   # gratuit et rapide sur Groq

# @st.cache_resource(show_spinner="📚 Chargement de la base de connaissances…")
# def load_knowledge_base():
#     chunks = load_and_chunk(BOUTIQUE_FILE,80)
#     index = build_index(chunks)
#     return chunks, index


# # ── Initialisation du client Groq ───────────────────────────────────────────
# @st.cache_resource
# def get_groq_client():
#     api_key = st.secrets.get("GROQ_API_KEY", None)
#     if not api_key:
#         st.error("❌ Clé API Groq manquante. Ajoute-la dans `.streamlit/secrets.toml`.")
#         st.stop()
#     return Groq(api_key=api_key)

# def answer_question(client: Groq, question: str, context_chunks: list[str]) -> str:
#     """Envoie la question + le contexte récupéré à l'LLM et retourne la réponse."""
#     context = "\n\n".join(context_chunks)

#     system_prompt = (
#             "Tu es un assistant virtuel pour une boutique. "
#             "Réponds uniquement à partir des informations fournies dans le CONTEXTE ci-dessous. "
#             "Si la réponse n'est pas dans le contexte, dis-le poliment. "
#             "Réponds toujours en français, de façon claire et concise."
#         )
    
#     user_prompt = f"""CONTEXTE :
#         {context}

#         QUESTION : {question}

#         RÉPONSE :"""
    

#     response = client.chat.completions.create(
#         model=GROQ_MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ],
#         temperature=0.3,
#         max_tokens=512,
#     )

#     return response.choices[0].message.content.strip()

# # ── Interface utilisateur ───────────────────────────────────────────────────
# def main():
#     st.title("🛍️ Assistant de la Boutique")
#     st.markdown("Posez votre question sur notre boutique — horaires, produits, livraison, retours…")
#     st.divider()

# # Chargement de la base de connaissances
#     chunks, index = load_knowledge_base()

#     client = get_groq_client()

#     # Historique de conversation (stocké en session)
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Affichage de l'historique
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])
    
#     # Zone de saisie
#     if question := st.chat_input("Votre question…"):
#          # Affiche la question de l'utilisateur
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user"):
#             st.markdown(question)

#         # Récupération des chunks pertinents (RAG)
#         with st.spinner("🔍 Recherche dans la base de connaissances…"):
#             relevant_chunks = retrieve(question, chunks, index, top_k=2)


#          # Génération de la réponse
#         with st.spinner("🤖 Génération de la réponse…"):
#             answer = answer_question(client, question, relevant_chunks)


#         # Affiche et sauvegarde la réponse
#         st.session_state.messages.append({"role": "assistant", "content": answer})
#         with st.chat_message("assistant"):
#             st.markdown(answer)




# if __name__ == "__main__":
#     main()





































import streamlit as st
from groq import Groq
from rag_engine import load_and_chunk , build_index , retrieve


# ── Configuration de la page ────────────────────────────────────────────────
st.set_page_config(
    page_title="Boutique Enchantée AI",
    page_icon="🛍️",
    layout="centered",
)

# ── Style visuel (CSS léger) ────────────────────────────────────────────────
st.markdown("""
<style>
.main-title {
    font-size:38px;
    font-weight:700;
    color:#6A5ACD;
}
.subtitle {
    font-size:18px;
    color:gray;
}
.footer {
    text-align:center;
    font-size:14px;
    color:gray;
    margin-top:50px;
}
</style>
""", unsafe_allow_html=True)


# ── Constantes ──────────────────────────────────────────────────────────────
BOUTIQUE_FILE = "documentation_boutique.txt"
GROQ_MODEL = "llama-3.1-8b-instant"


# ── Chargement de la base de connaissances ──────────────────────────────────
@st.cache_resource(show_spinner="📚 Chargement de la base de connaissances…")
def load_knowledge_base():
    chunks = load_and_chunk(BOUTIQUE_FILE,80)
    index = build_index(chunks)
    return chunks, index


# ── Initialisation du client Groq ───────────────────────────────────────────
@st.cache_resource
def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY", None)
    if not api_key:
        st.error("❌ Clé API Groq manquante. Ajoute-la dans `.streamlit/secrets.toml`.")
        st.stop()
    return Groq(api_key=api_key)


# ── Fonction réponse LLM ────────────────────────────────────────────────────
def answer_question(client: Groq, question: str, context_chunks: list[str]) -> str:

    context = "\n\n".join(context_chunks)

    system_prompt = (
        "Tu es un assistant virtuel pour une boutique. "
        "Réponds uniquement à partir des informations fournies dans le CONTEXTE. "
        "Si l'information n'existe pas, dis-le poliment. "
        "Réponds toujours en français de manière claire."
    )

    user_prompt = f"""
CONTEXTE :
{context}

QUESTION :
{question}

RÉPONSE :
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()


# ── Interface principale ────────────────────────────────────────────────────
def main():

    # Sidebar
    with st.sidebar:
        st.title("🛍️ Boutique Enchantée")
        st.markdown("""
Bienvenue dans notre **assistant intelligent**.

Il peut vous aider à :
- Découvrir nos produits
- Comprendre la livraison
- Connaître les moyens de paiement
- Consulter la politique de retour
- Vérifier les horaires

Posez simplement votre question !
        """)

        st.divider()

        st.info("💡 Exemple :\n\n"
                "- Quels bijoux proposez-vous ?\n"
                "- Quels sont les délais de livraison ?\n"
                "- Puis-je retourner un produit ?")

    # Titre principal
    # st.markdown('<p class="main-title">✨ Assistant Intelligent de la Boutique Enchantée</p>', unsafe_allow_html=True)

    st.markdown("""
        <style>
        .main-title {
            text-align: center;
            font-size: 60px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(
    '<p class="main-title">✨ Assistant Intelligent de la Boutique Enchantée</p>',
    unsafe_allow_html=True
)
    
    st.image("boutique_img.png", caption="", use_container_width =True)

    st.markdown(
        '<p class="subtitle">Votre conseiller virtuel disponible 24h/24 pour répondre à toutes vos questions.</p>',
        unsafe_allow_html=True
    )

    st.divider()


    # Chargement base
    chunks, index = load_knowledge_base()
    client = get_groq_client()


    # Historique conversation
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


    # Input utilisateur
    if question := st.chat_input("💬 Posez votre question sur la boutique..."):

        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        # Recherche RAG
        with st.spinner("🔎 Recherche des informations dans notre base..."):
            relevant_chunks = retrieve(question, chunks, index, top_k=3)

        # Génération réponse
        with st.spinner("🤖 L'assistant prépare votre réponse..."):
            answer = answer_question(client, question, relevant_chunks)

        # Affichage
        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)

        
         # Optionnel : afficher les chunks utilisés (debug)
        with st.expander("📄 Contexte utilisé par le RAG", expanded=False):
            for i, chunk in enumerate(relevant_chunks, 1):
                st.markdown(f"**Chunk {i} :** {chunk}")


    # Footer
    st.markdown("""
    <div class="footer">
    ✨ Assistant AI — Boutique Enchantée <br>
    Propulsé par Groq + RAG + Streamlit
    </div>
    """, unsafe_allow_html=True)




if __name__ == "__main__":
    main()
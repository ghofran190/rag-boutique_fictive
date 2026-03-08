
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Définir le modèle d'embeddings
# --------------------------------------------------------------------
EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')


# Charge le fichier texte et le découpe en chunks chevauchants.
# --------------------------------------------------------------

def load_and_chunk(filepath: str, chunk_size: int = 200, overlap: int = 40) -> list[str]:
    """
    Charge le fichier texte et le découpe en chunks chevauchants.
    chunk_size : nombre de mots par chunk
    overlap    : nombre de mots partagés entre deux chunks consécutifs
    """
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks




# Génère les embeddings pour tous les chunks
# ----------------------------------------------------------------
def build_index(chunks: list[str]) -> np.ndarray:
    """Génère les embeddings pour tous les chunks."""
    embeddings = EMBED_MODEL.encode(chunks, show_progress_bar=False)
    return np.array(embeddings)




# etourne les top_k chunks les plus pertinents pour la question posée.
# -------------------------------------------------------------------
def retrieve(query: str, chunks: list[str], index: np.ndarray, top_k: int = 3) -> list[str]:
    """
    Retourne les top_k chunks les plus pertinents pour la question posée.
    """
    query_vec = EMBED_MODEL.encode([query])
    scores = cosine_similarity(query_vec, index)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in top_indices]

# -------------------------------------------------------------------

# if __name__ == "__main__":
#     # 1️⃣ Charger les chunks depuis boutique.txt

#     chunks = load_and_chunk("text.txt", chunk_size=100, overlap=10)
#     print(f"Nombre de chunks : {len(chunks)}")

#     # 2️⃣ Construire les embeddings
#     embeddings = build_index(chunks)

#     # 3️⃣ Vérifier le type et la forme
#     print(f"Shape des embeddings : {embeddings.shape}")

#     # 3️⃣ Test de la fonction retrieve
#     query = "Quels sont vos produits?"
#     top_chunks = retrieve(query, chunks, embeddings, top_k=2)

#     print("\nTop 3 chunks pertinents pour la question :")
#     for i, c in enumerate(top_chunks, start=1):
#         print(f"\n--- Chunk {i} ---\n{c}")





import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Ortam değişkenlerini yükle
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Sayfa ayarları
st.set_page_config(page_title="🎨 Öğretmen Etkinlik Öneri Chatbotu", page_icon="🎈", layout="wide")
st.title("🎨 Etkinlik Öneri Chatbotu")
st.markdown("Malzemeleri yaz, sana en uygun etkinlikleri önerelim 👇")

# Kullanıcı girdisi
user_input = st.text_area("🧺 Elindeki malzemeler:", placeholder="örnek: balon, ip, pipet, bant, boncuk")

# Türkçe embedding modeli
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Embedding class'ı
class SentenceTransformerEmbedding:
    def __call__(self, input):
        return model.encode(input).tolist()

embedding_fn = SentenceTransformerEmbedding()

# Chroma istemcisi
client = chromadb.PersistentClient(path="chroma")
collection = client.get_or_create_collection(
    name="etkinlikler",
    embedding_function=embedding_fn
)

# Buton tıklanınca
if st.button("🎈 Etkinlik Öner"):
    if not user_input.strip():
        st.warning("Lütfen bazı malzemeler gir 🙏")
    else:
        # En benzer etkinlikleri bul
        results = collection.query(
            query_texts=[user_input],
            n_results=3
        )
        context = "\n\n".join(results["documents"][0])

        # Gemini'ye gönderilecek prompt
        prompt = f"""
        Sen yaratıcı bir okul öncesi öğretmen yardımcısısın.
        Aşağıdaki malzemelerle yapılabilecek etkinlikleri öner.
        Malzemeler: {user_input}

        Veri tabanındaki benzer etkinlikler:
        {context}

        Bunlardan yola çıkarak 2-3 etkinlik öner.
        Her birini başlık, açıklama ve kazanımlar şeklinde açıkla.
        """

        with st.spinner("düşünüyor..."):
            model_gemini = genai.GenerativeModel("gemini-2.0-flash")
            response = model_gemini.generate_content(prompt)

        st.markdown("### 🎯 Önerilen Etkinlikler:")
        st.write(response.text)

import chromadb
from sentence_transformers import SentenceTransformer

# Türkçe destekli Hugging Face modeli
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Chroma API formatına uygun embedding class'ı
class SentenceTransformerEmbedding:
    def __call__(self, input):
        return model.encode(input).tolist()

# Embedding fonksiyonunu oluşturma
embedding_fn = SentenceTransformerEmbedding()

# Kalıcı Chroma istemcisi
client = chromadb.PersistentClient(path="chroma")

# Koleksiyonu oluştur veya var olanı getir
collection = client.get_or_create_collection(
    name="etkinlikler",
    embedding_function=embedding_fn
)

# Veri dosyasını oku
with open("etkinlikler_dataset.md", "r", encoding="utf-8") as f:
    data = f.read()

# Etkinlikleri ayır
chunks = [chunk.strip() for chunk in data.split("---") if len(chunk.strip()) > 0]
print(f"Toplam {len(chunks)} etkinlik bulundu.")

# Veritabanına ekle
for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        ids=[f"etkinlik_{i}"]
    )

print("Türkçe embedding modeli ile veritabanı başarıyla oluşturuldu.")

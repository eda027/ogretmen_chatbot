# Öğretmen Etkinlik Öneri Chatbotu

Bu proje, **okul öncesi ve sınıf öğretmenlerinin** elindeki malzemelere göre uygun etkinlikleri önermesini sağlayan bir **RAG tabanlı chatbot** sistemidir.Sınıf öğretmeni olan yakın arkadaşımın sürekli yeni etkinlik bulma konusunda zorluk yaşamasından ilham alınarak gündelik hayat problemine çözüm üretmek için tasarlanmıştır.  
Model, **Türkçe destekli embedding** (SentenceTransformers) ve **Google Gemini 2.0 API** ile anlam temelli etkinlik önerileri üretir.

---

## Proje Amacı

Öğretmenler çoğu zaman “Elimde balon, ip ve pipet var; ne etkinliği yapabilirim?” gibi sorulara hızlı yanıt arar.  
Bu proje, 53 etkinliklik bir veri tabanı üzerinden **malzeme bazlı öneriler** üretir.

Chatbot:
-  Öğretmenden malzeme girdisini alır  
-  En yakın etkinlikleri vektör benzerliği ile bulur  
-  Gemini 2.0 Flash modeliyle anlamlı öneriler üretir  

---

##  Sistem Mimarisi

```
Kullanıcı Girdisi (malzemeler)
        │
        ▼
[SentenceTransformer Embedding] → metni vektöre çevir
        │
        ▼
[ChromaDB] → en yakın etkinlikleri bul
        │
        ▼
[Gemini 2.0 API] → doğal dilde etkinlik önerisi üret
        │
        ▼
[Streamlit Arayüzü] → kullanıcıya göster
```

---

##  Kullanılan Teknolojiler

| Teknoloji | Amaç | Neden Seçildi? |
|------------|------|----------------|
| **Python 3.10+** | Proje dili | Geniş ekosistem, AI desteği |
| **Streamlit** | Web arayüzü | Hızlı prototipleme, kullanıcı dostu |
| **ChromaDB** | Vektör veritabanı | RAG sistemleri için optimize |
| **SentenceTransformer** (`paraphrase-multilingual-MiniLM-L12-v2`) | Türkçe embedding | Anlam bazlı benzerlik, offline çalışır |
| **Google Gemini 2.0 Flash** | LLM (Cevap üretimi) | Hızlı, Türkçe destekli, güçlü |
| **python-dotenv** | API anahtarı yönetimi | Güvenli yapılandırma |

---

##  Embedding (Vektörleştirme) Süreci

**Embedding**, metinleri sayısal vektörlere dönüştürür.  
Bu vektörler, cümlelerin **anlamını matematiksel olarak temsil eder.**

Örnek:
```
"balon, pipet, ip" → [0.13, -0.22, 0.56, ...]
"Balon Roketi" → [0.14, -0.20, 0.54, ...]
```

Bu iki vektörün **cosine similarity** değeri yüksek olduğu için sistem “Balon Roketi” etkinliğini önerir.

Model:
>  `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

---

##  Dosya Yapısı

```
ogretmen-chatbot/
│
├── etkinlikler_dataset.md      # 53 etkinliklik veri seti
├── create_database.py          # Embedding veritabanı oluşturur
├── streamlit_app.py            # Ana uygulama arayüzü
├── requirements.txt            # Gereklilikler
├── .env                        # API anahtarı
└── chroma/                     # Otomatik oluşur (vektör DB)
```

---

##  Kurulum ve Çalıştırma

### 1- Ortamı hazırla
```bash
cd ogretmen-chatbot
python -m venv venv
venv\Scripts\activate        # Windows
# veya
source venv/bin/activate       # macOS / Linux
```

### 2- Gerekli kütüphaneleri yükle
```bash
pip install -r requirements.txt
```

### 3- .env dosyasını oluştur
```bash
GEMINI_API_KEY=senin_gemini_api_anahtarın
```
> API anahtarını buradan alabilirsin:  
>  [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### 4- Embedding veritabanını oluştur
```bash
python create_database.py
```
Çıktı şöyle olmalı:
```
 Toplam 53 etkinlik bulundu.
 Türkçe embedding modeli ile veritabanı başarıyla oluşturuldu.
```

### 5- Uygulamayı çalıştır
```bash
streamlit run streamlit_app.py
```
Tarayıcıda aç:
 [http://localhost:8501](http://localhost:8501)

---

##  Örnek Kullanım

**Kullanıcı:**  
> balon, pipet, bant, ip  

**Model Yanıtı:**  
> **Etkinlik:** Balon Roketi  
> **Açıklama:** Balon şişirilir, pipete bantlanır ve ip boyunca ilerler.  
> **Kazanımlar:** Motor beceriler, dikkat, neden-sonuç ilişkisi.

---

##  Teknik Detaylar

###  Embedding Fonksiyonu (Yeni Chroma 0.5.x için)
```python
class SentenceTransformerEmbedding:
    def __call__(self, input):
        return model.encode(input).tolist()
```
Bu sınıf, Chroma’nın yeni `__call__(self, input)` imzasına uygundur.

###  Model Yükleme
İlk çalıştırmada model Hugging Face’ten indirilir (~400 MB).  
Sonraki çalıştırmalarda yerel önbellekten yüklenir.

---


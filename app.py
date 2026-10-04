import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SAYFA VE ARAYÜZ AYARLARI ---
st.set_page_config(page_title="Osmanlıca Çevirmen", page_icon="📜", layout="centered")
st.title("📜 Osmanlıca Yapay Zeka Çevirmeni")
st.markdown("Uygulamaya hoş geldiniz! Çevirmek istediğiniz metni yazın veya belgenin fotoğrafını yükleyin.")

# --- GİZLİ KASADAN API ANAHTARINI ÇEKME ---
# Kod, şifreyi kullanıcıdan değil, Streamlit'in güvenli ayarlarından alacak.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.8-flash')
except KeyError:
    st.error("Sistem hatası: API anahtarı bulunamadı. Lütfen uygulamanın 'Secrets' ayarlarını kontrol edin.")
    st.stop()

# --- SEKME (TAB) YAPISI ---
tab1, tab2 = st.tabs(["✍️ Metin Yazarak Çevir", "📸 Fotoğraf Yükleyerek Çevir"])

# --- 1. SEKME: METİN ÇEVİRİSİ ---
with tab1:
    osmanlica_metin = st.text_area("Çevrilecek metni girin:", height=150, 
                                   placeholder="Örn: Bâki kalan bu kubbede bir hoş sadâ imiş...")

    if st.button("Metni Çevir 🚀"):
        if not osmanlica_metin.strip():
            st.warning("Lütfen çevrilecek bir metin girin.")
        else:
            with st.spinner('Çeviri yapılıyor, lütfen bekleyin...'):
                try:
                    prompt = f"""
                    Sen alanında uzman bir Osmanlıca-Türkçe çevirmensin. 
                    Aşağıdaki Osmanlıca metni anlama en uygun, akıcı günümüz Türkçesine çevir.
                    Sadece çeviriyi ver.
                    
                    Çevrilecek Metin: {osmanlica_metin}
                    """
                    response = model.generate_content(prompt)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Hata oluştu: {e}")

# --- 2. SEKME: FOTOĞRAFTAN ÇEVİRİ (OCR) ---
with tab2:
    yuklenen_fotograf = st.file_uploader("Osmanlıca metnin fotoğrafını seçin", type=["png", "jpg", "jpeg"])
    
    if yuklenen_fotograf is not None:
        image = Image.open(yuklenen_fotograf)
        st.image(image, caption="Yüklediğiniz Belge", use_container_width=True)
        
        if st.button("Fotoğrafı Oku ve Çevir 📸"):
            with st.spinner('Yapay zeka belgeyi inceliyor ve çeviriyor...'):
                try:
                    prompt_gorsel = """
                    Sen uzman bir Osmanlıca paleograf ve çevirmensin.
                    Ekteki görselde yer alan Osmanlıca metni oku.
                    Lütfen yanıtını tam olarak şu formatta ver:
                    
                    **📝 Metnin Okunuşu:**
                    [Görselden okuduğun Osmanlıca metnin latin harfleriyle yazılışı]
                    
                    **🇹🇷 Günümüz Türkçesine Çevirisi:**
                    [Okuduğun metnin akıcı günümüz Türkçesi ile çevirisi]
                    """
                    response_gorsel = model.generate_content([prompt_gorsel, image])
                    st.subheader("İnceleme Sonucu:")
                    st.success(response_gorsel.text)
                except Exception as e:
                    st.error(f"Görsel okunurken bir hata oluştu: {e}")

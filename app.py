import streamlit as st
import google.generativeai as genai
from PIL import Image  # Fotoğrafları işlemek için eklediğimiz kütüphane

# --- SAYFA VE ARAYÜZ AYARLARI ---
st.set_page_config(page_title="Osmanlıca Çevirmen", page_icon="📜", layout="centered")
st.title("📜 Osmanlıca Yapay Zeka Çevirmeni")

# --- API AYARLARI (SOL MENÜ) ---
st.sidebar.header("Ayarlar ⚙️")
api_key = st.sidebar.text_input("Gemini API Anahtarınızı Girin:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.8-flash')
    st.sidebar.success("Gemini 3.8 Flash başarıyla bağlandı!")
else:
    st.sidebar.warning("Lütfen çeviri yapabilmek için API anahtarınızı girin.")

# --- SEKME (TAB) YAPISI ---
# Arayüzü güzelleştiriyoruz: Kullanıcıya iki seçenek sunuyoruz
tab1, tab2 = st.tabs(["✍️ Metin Yazarak Çevir", "📸 Fotoğraf Yükleyerek Çevir"])

# --- 1. SEKME: METİN ÇEVİRİSİ ---
with tab1:
    st.markdown("### Klavyeden Metin Girişi")
    osmanlica_metin = st.text_area("Çevrilecek metni girin (Transkripsiyon veya Arap harfli):", height=150, 
                                   placeholder="Örn: Bâki kalan bu kubbede bir hoş sadâ imiş...")

    if st.button("Metni Çevir 🚀"):
        if not api_key:
            st.error("Lütfen sol menüden API anahtarınızı ekleyin.")
        elif not osmanlica_metin.strip():
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
    st.markdown("### Arşiv Belgesi veya Kitap Sayfası Yükle")
    # Dosya yükleme aracı (Sadece png, jpg, jpeg kabul eder)
    yuklenen_fotograf = st.file_uploader("Osmanlıca metnin fotoğrafını seçin", type=["png", "jpg", "jpeg"])
    
    if yuklenen_fotograf is not None:
        # Yüklenen fotoğrafı ekranda gösteriyoruz
        image = Image.open(yuklenen_fotograf)
        st.image(image, caption="Yüklediğiniz Belge", use_container_width=True)
        
        if st.button("Fotoğrafı Oku ve Çevir 📸"):
            if not api_key:
                st.error("Lütfen sol menüden API anahtarınızı ekleyin.")
            else:
                with st.spinner('Yapay zeka belgeyi inceliyor ve çeviriyor... (Bu işlem biraz sürebilir)'):
                    try:
                        # Görsel için modele verilecek özel talimat
                        prompt_gorsel = """
                        Sen uzman bir Osmanlıca paleograf ve çevirmensin.
                        Ekteki görselde yer alan Osmanlıca metni (matbu veya el yazısı olabilir) dikkatlice oku.
                        Lütfen yanıtını tam olarak şu formatta ver:
                        
                        **📝 Metnin Okunuşu:**
                        [Görselden okuduğun Osmanlıca metnin latin harfleriyle yazılışı]
                        
                        **🇹🇷 Günümüz Türkçesine Çevirisi:**
                        [Okuduğun metnin akıcı günümüz Türkçesi ile çevirisi]
                        """
                        
                        # DİKKAT: Burada modele hem yazılı talimatı (prompt_gorsel) hem de fotoğrafı (image) aynı anda yolluyoruz!
                        response_gorsel = model.generate_content([prompt_gorsel, image])
                        
                        st.subheader("İnceleme Sonucu:")
                        st.success(response_gorsel.text)
                    except Exception as e:
                        st.error(f"Görsel okunurken bir hata oluştu: {e}")
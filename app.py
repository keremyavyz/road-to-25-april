import streamlit as st
import random
import time
import base64
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Road to 25 April | Elite Edition",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS: GENEL TASARIM & ANİMASYONLAR ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Lora:ital,wght@0,500;1,400&family=Montserrat:wght@300;600&display=swap');

    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 100%);
        background-attachment: fixed;
    }

    /* --- GİRİŞ EKRANI (BAŞLANGIÇ) --- */
    .start-screen-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 50px;
        border-radius: 30px;
        border: 4px solid #be123c;
        text-align: center;
        box-shadow: 0 20px 50px rgba(190, 18, 60, 0.3);
        animation: fadeIn 1s ease-in;
    }
    .winner-text {
        font-family: 'Cinzel Decorative', cursive;
        color: #be123c;
        font-size: 40px;
        margin-top: 20px;
        text-shadow: 2px 2px 0px #fff;
    }

    /* --- ARA GEÇİŞ (PASLAŞMA) EKRANI --- */
    .handover-box {
        background-color: #be123c;
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 3px solid #d4af37;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    /* --- KART TASARIMI (3D & STICKER) --- */
    .card-wrapper {
        position: relative;
        width: 100%;
        max-width: 500px;
        margin: 20px auto;
        animation: floatUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Yaylanma efekti */
    }
    @keyframes floatUp {
        from { transform: translateY(100px) rotate(-5deg); opacity: 0; }
        to { transform: translateY(0) rotate(0deg); opacity: 1; }
    }

    .white-card-box {
        background: #ffffff;
        padding: 30px 25px 50px 25px;
        border-radius: 25px;
        box-shadow: 
            0 15px 35px rgba(190, 18, 60, 0.15),
            0 5px 15px rgba(0,0,0,0.05);
        text-align: center;
        border: 2px solid #d4af37;
        position: relative;
        z-index: 10;
    }
    
    /* Kartın üzerindeki doku efekti */
    .white-card-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url("https://www.transparenttextures.com/patterns/cream-paper.png");
        opacity: 0.5;
        border-radius: 23px;
        z-index: -1;
    }

    .card-title-text {
        color: #9f1239;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        text-transform: uppercase;
        border-bottom: 2px solid #fce7f3;
        padding-bottom: 10px;
        display: inline-block;
    }

    .mini-photo-frame {
        width: 100px;
        height: 100px;
        margin: 0 auto 20px auto;
        border-radius: 50%;
        border: 4px solid #d4af37;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        overflow: hidden;
        background-color: #fff;
    }
    .mini-photo-frame img { width: 100%; height: 100%; object-fit: cover; }

    .card-content-text {
        color: #374151;
        font-size: 24px;
        line-height: 1.6;
        font-family: 'Lora', serif;
        font-style: italic;
        font-weight: 500;
    }

    /* 3D STICKER */
    .sticker-3d {
        position: absolute;
        bottom: -30px;
        right: -25px;
        width: 140px;
        z-index: 20;
        filter: drop-shadow(5px 10px 10px rgba(0,0,0,0.4));
        transform: rotate(-10deg);
        transition: transform 0.3s;
    }
    .sticker-3d:hover { transform: rotate(0deg) scale(1.1); }

    /* --- BUTONLAR --- */
    .stButton>button {
        background: linear-gradient(90deg, #be123c, #db2777);
        color: white;
        border-radius: 50px;
        height: 60px;
        font-size: 20px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(190, 18, 60, 0.4);
        width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(190, 18, 60, 0.6);
    }

    /* Müzik Player Konteyner */
    .music-box {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.9);
        padding: 10px 20px;
        border-radius: 30px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        z-index: 100;
    }
    
    .status-text {
        text-align: center;
        color: #6b7280;
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---
def get_image_base64(path):
    if not os.path.exists(path): return ""
    with open(path, "rb") as f: encoded = base64.b64encode(f.read()).decode()
    ext = path.split('.')[-1]
    return f"data:image/{ext};base64,{encoded}"

# Görselleri Yükle
img_busra_main = get_image_base64("busra.jpg")
img_kerem_main = get_image_base64("kerem.jpg")
img_biz_main = get_image_base64("biz.jpg")
img_sticker_busra = get_image_base64("sticker_busra.png")
# İstersen Kerem için de sticker ekleyebilirsin:
img_sticker_kerem = get_image_base64("kerem.jpg") # Şimdilik normal fotoyu kullanalım

# --- OYUN DURUMU (SESSION STATE) ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'START' # START, PLAYING, HANDOVER
if 'current_player' not in st.session_state:
    st.session_state.current_player = None # 'Kerem' veya 'Busra'
if 'pending_card' not in st.session_state:
    st.session_state.pending_card = None
if 'deck' not in st.session_state:
    # 64 KARTLIK DESTE (Aynı liste)
    st.session_state.deck = [
        # ... (Buraya önceki tüm 64 kartlık listeyi aynen yapıştır) ...
        # KODUN KISA OLMASI İÇİN ÖRNEK KARTLAR KOYUYORUM, SEN HEPSİNİ EKLE:
        {"type": "SORU (BÜŞRA)", "target": "Busra", "text": "Aksaray'daki o seminerde masana kedi atladığında attığın o çığlığı hatırla... O gün kediden kaçan Büşra'dan, bugün Lila ve Simba'ya annelik yapan Büşra'ya dönüşmek sence nasıl bir yolculuktu?"},
        {"type": "SORU (KEREM)", "target": "Kerem", "text": "6 Temmuz'da, kendi doğum gününü feda edip evlilik teklifi etmek... Bu tarihi seçerken aklındaki asıl mesaj neydi?"},
        {"type": "GÖREV (ORTAK)", "target": "Both", "text": "Telefonunu çıkar, rastgele bir şarkı aç. Çalan şarkının ritmine göre dans etmek zorundayız."},
        {"type": "İTİRAF", "target": "Both", "text": "Göktürk Starbucks'ta o ilk kahveyi içerken... aklından geçen ama söylemediğin o ilk düşünce neydi?"},
        # ... Diğer tüm kartları buraya ekle (target='Busra', 'Kerem', 'Both' olarak işaretleyerek)
    ]
    # Kartlara 'target' özelliği eklemeyi unutma! 
    # Mantık: SORU (BÜŞRA) -> target: Busra (Cevaplayacak kişi)
    # SORU (KEREM) -> target: Kerem
    # Diğerleri -> target: Both
    
    # Hızlı düzeltme döngüsü (Eğer elle tek tek target yazmazsan bu otomatik atar):
    for card in st.session_state.deck:
        if "target" not in card:
            if "(BÜŞRA)" in card['type']: card['target'] = "Busra"
            elif "(KEREM)" in card['type']: card['target'] = "Kerem"
            else: card['target'] = "Both"
            
    random.shuffle(st.session_state.deck)

# --- BAŞLIK ---
if st.session_state.game_state != 'START':
    st.markdown("<h2 style='text-align: center; color: #be123c; margin-top:-20px; font-family: \"Cinzel Decorative\";'>ROAD TO 25 APRIL 💍</h2>", unsafe_allow_html=True)

# ==========================================
# 1. SAHNE: KİM BAŞLIYOR? (START SCREEN)
# ==========================================
if st.session_state.game_state == 'START':
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) # Boşluk
    
    st.markdown("""
    <div class='start-screen-box'>
        <h1 style='color:#be123c; font-family: "Cinzel Decorative";'>HAZIR MISINIZ?</h1>
        <p style='font-size:20px; color:#555;'>14 Şubat Gecesi Başlıyor...</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎲 KİMİN BAŞLAYACAĞINI SEÇ 🎲"):
        with st.spinner("Kader Çarkı Dönüyor..."):
            time.sleep(2) # Heyecan süresi
        
        # Rastgele seçim
        winner = random.choice(["Kerem", "Büşra"])
        st.session_state.current_player = winner
        st.session_state.game_state = 'PLAYING'
        st.experimental_rerun()

# ==========================================
# 2. SAHNE: OYUN AKIŞI (PLAYING)
# ==========================================
elif st.session_state.game_state == 'PLAYING':
    
    # Şu an kimde sıra?
    player = st.session_state.current_player
    remaining = len(st.session_state.deck)
    
    st.markdown(f"<p class='status-text'>Telefon Şu An: <b>{player.upper()}</b>'de | Kalan Kart: {remaining}</p>", unsafe_allow_html=True)

    if remaining > 0:
        btn_text = f"✨ Kart Çek ({player}) ✨"
        if st.button(btn_text):
            # Kartı çek ama hemen gösterme, kontrol et
            card = st.session_state.deck.pop()
            st.session_state.pending_card = card
            
            # KONTROL: Eğer telefon Kerem'deyse ve kart "Kerem'e Soru" ise -> PASLAŞMA GEREKİR
            # Tam tersi Büşra için de geçerli.
            
            # Senaryo 1: Telefon Kerem'de, Soru Kerem'e -> UYARI (Büşra'ya ver)
            if player == "Kerem" and card['target'] == "Kerem":
                st.session_state.game_state = 'HANDOVER'
            
            # Senaryo 2: Telefon Büşra'da, Soru Büşra'ya -> UYARI (Kerem'e ver)
            elif player == "Büşra" and card['target'] == "Busra":
                st.session_state.game_state = 'HANDOVER'
                
            # Senaryo 3: Diğer durumlar (Normal) -> Göster
            else:
                st.session_state.current_card = card
            
            st.experimental_rerun()
            
        # Eğer bir kart aktifse göster
        if 'current_card' in st.session_state:
            card = st.session_state.current_card
            
            # Görsel Ayarları
            mini_photo = img_biz_main
            sticker_html = ""
            
            if card['target'] == "Busra":
                mini_photo = img_busra_main
                # Soru Büşra'ya ise, Sticker Büşra olsun (Soruyu soran/Okuyan kişiyi izliyor gibi)
                # Ya da senin dediğin gibi: Büşra'nın png'si kartın üzerinde.
                if img_sticker_busra:
                    sticker_html = f'<img src="{img_sticker_busra}" class="sticker-3d">'
            elif card['target'] == "Kerem":
                mini_photo = img_kerem_main
            
            # KART HTML
            html_card = f"""
            <div class="card-wrapper">
                <div class="white-card-box">
                    <div class="card-title-text">{card['type']}</div>
                    <div class="mini-photo-frame"><img src="{mini_photo}"></div>
                    <div class="card-content-text">{card['text']}</div>
                </div>
                {sticker_html}
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
            
            # Sırayı Devret Butonu (Sıradaki tura geçiş)
            st.markdown("---")
            if st.button("Sırayı Diğerine Ver 🔄"):
                # Sırayı değiştir
                new_player = "Büşra" if player == "Kerem" else "Kerem"
                st.session_state.current_player = new_player
                # Kartı temizle
                del st.session_state.current_card
                st.experimental_rerun()

    else:
        st.balloons()
        st.success("Tüm kartlar bitti! Sonsuza kadar mutlu olun! ❤️")

# ==========================================
# 3. SAHNE: PASLAŞMA (HANDOVER)
# ==========================================
elif st.session_state.game_state == 'HANDOVER':
    
    target_person = "Büşra" if st.session_state.current_player == "Kerem" else "Kerem"
    
    st.markdown(f"""
    <div class='handover-box'>
        <h1 style='font-size: 50px;'>🛑 HOP!</h1>
        <h3 style='font-family:"Montserrat"'>Bu Soru Sana Geldi!</h3>
        <p style='font-size: 20px; margin-top:20px;'>
            Sürprizi bozmamak için okuma.<br>
            Telefonu hemen <b>{target_person.upper()}</b>'ya uzat!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(f"Telefonu Aldım ({target_person}) ✅"):
        # Oyuncuyu değiştir
        st.session_state.current_player = target_person
        # Bekleyen kartı aktif et
        st.session_state.current_card = st.session_state.pending_card
        # Oyuna dön
        st.session_state.game_state = 'PLAYING'
        st.experimental_rerun()

# --- MÜZİK PLAYER (SABİT ALT) ---
st.markdown("""
<div class='music-box'>
    <a href="https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" target="_blank" style="text-decoration:none; color:#be123c; font-weight:bold; font-family:'Montserrat';">
        ♫ Romantik Müzik Aç ♫
    </a>
</div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div style='text-align:center; color:#ccc; margin-top:50px; font-size:12px;'>For My Better Half, Büşra ❤️</div>", unsafe_allow_html=True)

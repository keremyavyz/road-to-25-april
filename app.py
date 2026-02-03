import streamlit as st
import random
import time
import base64
import os
from pathlib import Path

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Road to 25 April",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS: MODERN TASARIM VE ANİMASYONLAR ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');

    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #fef6f8 0%, #ffe8ee 50%, #fff0f5 100%);
        background-attachment: fixed;
    }

    /* Streamlit default padding remove */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* --- İLERLEME BARI --- */
    .progress-container {
        width: 100%;
        max-width: 500px;
        margin: 20px auto;
        background: rgba(255,255,255,0.7);
        border-radius: 25px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(190, 18, 60, 0.15);
        backdrop-filter: blur(10px);
    }
    .progress-bar-bg {
        height: 10px;
        background: rgba(190, 18, 60, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #be123c, #db2777, #f472b6);
        border-radius: 10px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 20px rgba(190, 18, 60, 0.5);
        animation: shimmer 2s infinite;
    }
    @keyframes shimmer {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    .progress-text {
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        color: #be123c;
        margin-top: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* --- ZAR ATMA EKRANI --- */
    .dice-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,240,245,0.95));
        padding: 50px 30px;
        border-radius: 30px;
        border: 3px solid #be123c;
        text-align: center;
        box-shadow: 0 20px 60px rgba(190, 18, 60, 0.25);
        animation: slideUp 0.6s ease-out;
        margin-top: 40px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    @keyframes slideUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .dice-title {
        font-family: 'Playfair Display', serif;
        color: #be123c;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }
    .dice-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
        font-weight: 400;
    }
    
    /* Zar Animasyonu */
    .dice-box {
        display: inline-block;
        width: 120px;
        height: 120px;
        background: white;
        border-radius: 20px;
        margin: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
        border: 3px solid #be123c;
        animation: diceRoll 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    @keyframes diceRoll {
        0% { transform: rotate(0deg) scale(0.5); }
        50% { transform: rotate(360deg) scale(1.1); }
        100% { transform: rotate(720deg) scale(1); }
    }
    
    /* --- PASLAŞMA EKRANI --- */
    .handover-box {
        background: linear-gradient(135deg, #be123c, #db2777);
        color: white;
        padding: 50px 40px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(190, 18, 60, 0.4);
        border: 4px solid #fff;
        animation: pulse 2s ease-in-out infinite;
        margin-top: 50px;
        max-width: 550px;
        margin-left: auto;
        margin-right: auto;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 15px 50px rgba(190, 18, 60, 0.4); }
        50% { transform: scale(1.02); box-shadow: 0 20px 60px rgba(190, 18, 60, 0.6); }
    }
    .handover-emoji {
        font-size: 80px;
        margin-bottom: 20px;
        animation: bounce 1s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }

    /* --- 3D KART YAPISI --- */
    .card-wrapper {
        position: relative;
        width: 100%;
        max-width: 500px;
        margin: 40px auto;
        perspective: 1500px;
    }

    .white-card-box {
        background: linear-gradient(to bottom, #ffffff, #fffbf8);
        padding: 50px 35px 70px 35px;
        border-radius: 25px;
        box-shadow: 
            0 20px 60px rgba(190, 18, 60, 0.15),
            0 10px 20px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.9);
        text-align: center;
        border: 2px solid rgba(190, 18, 60, 0.2);
        position: relative;
        z-index: 10;
        animation: cardEntrance 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        transform-style: preserve-3d;
    }
    @keyframes cardEntrance {
        0% { 
            transform: rotateY(-90deg) translateZ(-200px);
            opacity: 0;
        }
        100% { 
            transform: rotateY(0deg) translateZ(0);
            opacity: 1;
        }
    }

    /* Kart Parlak Efekt */
    .white-card-box::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        animation: shine 3s infinite;
    }
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }

    /* Metinler */
    .card-title-text {
        color: #be123c;
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 25px;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        padding-bottom: 15px;
    }
    .card-title-text::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #be123c, transparent);
    }
    
    .card-content-text {
        color: #2d3748;
        font-size: 20px;
        line-height: 1.8;
        font-family: 'Montserrat', sans-serif;
        font-weight: 400;
        letter-spacing: 0.3px;
    }

    /* 3D STICKER (SAĞ ALT KÖŞE) */
    .sticker-3d {
        position: absolute;
        bottom: -50px;
        right: -40px;
        width: 180px;
        height: auto;
        z-index: 50;
        filter: drop-shadow(8px 12px 15px rgba(0,0,0,0.3));
        transform: rotate(-12deg);
        transition: transform 0.4s ease;
        pointer-events: none;
        animation: stickerFloat 3s ease-in-out infinite;
    }
    @keyframes stickerFloat {
        0%, 100% { transform: rotate(-12deg) translateY(0px); }
        50% { transform: rotate(-12deg) translateY(-8px); }
    }

    /* Butonlar */
    .stButton>button {
        background: linear-gradient(135deg, #be123c, #db2777);
        color: white;
        border-radius: 50px;
        height: 65px;
        font-size: 18px;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        border: none;
        box-shadow: 0 8px 25px rgba(190, 18, 60, 0.35);
        width: 100%;
        margin-top: 25px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    .stButton>button::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    .stButton>button:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(190, 18, 60, 0.5);
    }
    .stButton>button:active {
        transform: translateY(-2px);
    }
    
    /* Müzik Player */
    .music-box {
        position: fixed;
        bottom: 25px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        padding: 12px 30px;
        border-radius: 35px;
        box-shadow: 0 8px 30px rgba(190, 18, 60, 0.2);
        border: 2px solid rgba(190, 18, 60, 0.2);
        z-index: 100;
        font-family: 'Montserrat', sans-serif;
        font-size: 15px;
        font-weight: 500;
        color: #be123c;
        transition: all 0.3s ease;
    }
    .music-box:hover {
        transform: translateX(-50%) translateY(-3px);
        box-shadow: 0 12px 40px rgba(190, 18, 60, 0.3);
        border-color: #be123c;
    }

    /* Oyun Sonu */
    .game-summary {
        background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(255,240,245,0.98));
        padding: 50px 40px;
        border-radius: 30px;
        border: 3px solid #be123c;
        text-align: center;
        box-shadow: 0 20px 60px rgba(190, 18, 60, 0.3);
        animation: fadeIn 1s ease-in;
        margin-top: 40px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    .summary-title {
        font-family: 'Playfair Display', serif;
        color: #be123c;
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 25px;
    }
    .summary-stat {
        font-family: 'Montserrat', sans-serif;
        font-size: 18px;
        color: #555;
        margin: 15px 0;
        font-weight: 500;
    }

    /* Placeholder Image */
    .mini-photo-placeholder {
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #be123c, #db2777);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        color: white;
    }

    /* Mobil Responsive */
    @media (max-width: 768px) {
        .dice-title { font-size: 32px; }
        .card-content-text { font-size: 18px; }
        .card-title-text { font-size: 18px; }
        .sticker-3d { width: 130px; bottom: -35px; right: -25px; }
        .summary-title { font-size: 36px; }
        .dice-box { width: 100px; height: 100px; font-size: 50px; }
    }

    /* Gizle - Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SES EFEKTLERİ (Browser Audio API) ---
def play_sound(sound_type):
    """Tarayıcıda ses çalmak için JavaScript kodu"""
    sounds = {
        'dice': 'https://assets.mixkit.co/active_storage/sfx/2004/2004-preview.mp3',
        'card': 'https://assets.mixkit.co/active_storage/sfx/2570/2570-preview.mp3',
        'success': 'https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3',
        'transition': 'https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3'
    }
    
    if sound_type in sounds:
        st.markdown(f"""
        <audio autoplay style="display:none">
            <source src="{sounds[sound_type]}" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---
def get_image_base64(filename):
    """Görsel dosyasını base64'e çevirir"""
    possible_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    base_name = Path(filename).stem
    
    for ext in possible_extensions:
        filepath = f"{base_name}{ext}"
        if os.path.exists(filepath):
            try:
                with open(filepath, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                return f"data:image/{ext[1:]};base64,{encoded}"
            except:
                return None
    return None

def create_placeholder_image(emoji="💕"):
    """Görsel yoksa emoji placeholder"""
    return f'<div class="mini-photo-placeholder">{emoji}</div>'

def reset_game():
    """Oyunu sıfırla"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def init_deck():
    """Düzeltilmiş ve iyileştirilmiş kartlar"""
    raw_deck = [
        # SAYFA 1: KADER & BAŞLANGIÇ
        {"type": "SORU", "target": "Busra", "text": "Aksaray'daki o seminerde masana kedi atladığında attığın çığlığı hatırla... O gün kediden kaçan Büşra'dan, bugün Lila ve Simba'ya annelik yapan Büşra'ya dönüşmek nasıl bir yolculuktu?"},
        {"type": "SORU", "target": "Busra", "text": "Aksaray sonrası 'Kerem kesin yazar' diye beklerken yazmadığım o sessiz dönem... O günlerde bana ne kadar sinirlendin ve içinden neler geçirdin?"},
        {"type": "SORU", "target": "Kerem", "text": "Büşra'nın ayna karşısında kediyle attığı story bildirimi ekrana düştüğünde... Cevap yazmadan önce kaç dakika 'Ne yazsam?' diye düşündün ve ne kadar gergindin?"},
        {"type": "SORU", "target": "Both", "text": "Adıyaman depremi olmasa belki İstanbul'a hiç dönmeyecektim... Bizi tekrar bir araya getiren bu 'Kader' hakkında ne hissediyorsun? Tesadüf mü, yoksa kaçınılmaz mıydı?"},
        {"type": "İTİRAF", "target": "Both", "text": "Göktürk Starbucks'ta ilk kahveyi içerken karşındakine bakıp aklından geçen ama 'Henüz çok erken' diyerek söylemeye cesaret edemediğin ilk düşünce neydi?"},
        {"type": "SORU", "target": "Kerem", "text": "6 Temmuz'da kendi doğum gününü feda edip evlilik teklifi etmek... Bu tarihi seçerken aklındaki asıl mesaj neydi? 'En büyük hediyem sensin' mi?"},
        {"type": "SORU", "target": "Busra", "text": "Tekirdağ Uçmakdere'deki dağ evinde o an geldiğinde... Kerem diz çökmeden hemen önce durumu hissettin mi, yoksa dünya gerçekten durdu mu?"},
        {"type": "ANI", "target": "Both", "text": "Balkanlar tatilinde Üsküp yolunda arabada deliler gibi gülme krizine girdiğimiz gece... Bizi birbirimize asıl 'mühürleyen' o kahkahalar mıydı?"},
        
        # SAYFA 2: YUVA & GELECEK
        {"type": "HAYAL ET", "target": "Both", "text": "25 Nisan sabahı gözlerini açtığında, tüm düğün telaşı haricinde kalbinde hissetmek istediğin en baskın duygu ne?"},
        {"type": "HAYAL ET", "target": "Both", "text": "Kendi evimizi aldığımızda kapıdan girer girmez 'Burası bizim yuva' dedirtecek ilk detay veya eşya ne olmalı?"},
        {"type": "GERÇEKÇİLİK", "target": "Both", "text": "Evliliğimizin ilk yılında bizi en çok neyin zorlayacağını düşünüyorsun ve biz 'takım' olarak bunu nasıl aşacağız?"},
        {"type": "ROMANTİK", "target": "Both", "text": "Düğün dansımız sırasında herkes bizi izlerken kulağına fısıldamamı istediğin, sadece ikimizin duyacağı özel cümle ne?"},
        {"type": "DÜRÜSTLÜK", "target": "Both", "text": "Müstakbel eşin olarak şu an benimle ilgili kafandaki en büyük 'Acaba' veya endişe nedir?"},
        {"type": "EV HALİ", "target": "Both", "text": "Yeni evimizde 'Burası kesinlikle benim alanım, sakın müdahale etme' diyeceğin dokunulmaz bölge neresi?"},
        {"type": "EV HALİ", "target": "Both", "text": "Ev işleri söz konusu olduğunda ilk büyük tartışmamız neyden çıkar? Ortada bırakılan çoraplar mı, yoksa bulaşık makinesi mi?"},
        {"type": "MÜZİK", "target": "Both", "text": "Pejo 308 geride kaldı... Yeni arabamızda kontağı çevirdiğimiz an açıp dinleyeceğimiz 'bizi anlatan' ilk şarkı hangisi olmalı?"},

        # SAYFA 3: AİLE & BİZ
        {"type": "EĞLENCE", "target": "Both", "text": "Düğün gecesi (biz hariç) pistten inmeyen, en çok coşan veya en eğlenen sürpriz isim kim olacak?"},
        {"type": "EV HALİ", "target": "Both", "text": "Evlendiğimizin ilk sabahı o huzurlu Pazar kahvaltısını kim hazırlar? (Gerçekçi olalım)."},
        {"type": "AİLE", "target": "Both", "text": "Birbirimizin ailesiyle ilgili gözlemlediğin, seni en çok güldüren veya içini ısıtan özellik ne?"},
        {"type": "GELECEK", "target": "Both", "text": "Geleceği hayal et... Nasıl bir anne-baba olacağız? Birbirimizin ebeveynlik potansiyeline 10 üzerinden puan ver."},
        {"type": "EĞLENCE", "target": "Both", "text": "Düğün dansımızda heyecandan ayağına basma ihtimalim yüzde kaç? (Dürüst ol, alınmam)."},
        {"type": "EV HALİ", "target": "Both", "text": "İleride evde bir kriz çıktığında 'İyi Polis' kim, 'Kötü Polis' kim olacak?"},
        {"type": "YEMEK", "target": "Both", "text": "Diyetimi tek bir yemekle bozma hakkım olsa önüme ne koyardın da asla 'Hayır' diyemezdim?"},
        {"type": "BENZETME", "target": "Both", "text": "Beni bir film veya çizgi film karakterine benzetsen, huyum suyum en çok kime benziyor?"},

        # SAYFA 4: DERİN & GÖREV
        {"type": "MÜZİK", "target": "Kerem", "text": "Hayatının sonuna kadar sadece tek bir şarkımı dinleyebilecek olsan 'Just B' albümünden hangisini seçerdin ve neden?"},
        {"type": "GÖREV", "target": "Both", "text": "Telefonunu al, galerine gir ve benim en komik, en ifşa fotoğrafımı bulup göster. Hikayesini anlat."},
        {"type": "GÖREV", "target": "Both", "text": "Ayağa kalk! Düğün dansımızın kısa provasını yapıyoruz. Müzik yok, mırıldanmak serbest."},
        {"type": "GÖREV", "target": "Both", "text": "Beni 1 dakika 'İngilizce Öğretmeni Kerem' edasıyla, sınıfı yönetiyormuşum gibi taklit et."},
        {"type": "GÖREV", "target": "Kerem", "text": "'Just B' moduna geç! Bana şu an uydurduğun, içinde 'Lila', 'Simba' ve '14 Şubat' geçen 2 satırlık şarkı söyle."},
        {"type": "GÖREV", "target": "Both", "text": "Gözlerimi kapatacağım, avucuma parmağınla bir harf çiz. Bilirsem dile benden ne dilersen."},
        {"type": "GÖREV", "target": "Both", "text": "Neden beni sevdiğine dair 3 maddelik, çok hızlı ve ikna edici bir sunum yap."},
        {"type": "GÖREV", "target": "Both", "text": "Telefonunu çıkar, rastgele bir şarkı aç. Çalan şarkının ritmine göre dans etmeliyiz."},

        # SAYFA 5: AKSİYON
        {"type": "GÖREV", "target": "Both", "text": "1 dakika konuşmak yasak. Sadece gözlerimin içine bak. İlk gülen veya gözünü kaçıran kaybeder (ve öper)."},
        {"type": "GÖREV", "target": "Both", "text": "En sevdiğin huyumu veya özelliğimi hiç konuşmadan sadece hareketlerle anlat."},
        {"type": "GÖREV", "target": "Both", "text": "Hayatımda duyduğum en saçma veya en kötü iltifatı et. (Ne kadar yaratıcısın görelim)."},
        {"type": "GÖREV", "target": "Both", "text": "Masadaki veya odadaki herhangi bir objeyi al ve bana dünyanın en değerli şeyiymiş gibi sat."},
        {"type": "GÖREV", "target": "Both", "text": "Önümüzdeki 3 tur her cümleme 'Zümre Başkanım' veya 'Hocam' diye başlamak zorundasın."},
        {"type": "GÖREV", "target": "Both", "text": "Elimi sıkıca tut. 25 Nisan 2026 için bana şu an sesli, kalpten gelen bir söz ver."},
        {"type": "GÖREV", "target": "Both", "text": "Yaptığın veya yapacağın en güzel yemeğin tarifini, dünyanın en gizemli sırrını veriyormuşsun gibi anlat."},
        {"type": "GÖREV", "target": "Both", "text": "Sırtıma veya omuzlarıma 30 saniye masaj yap. Düğün yorgunluğu gitsin."},

        # SAYFA 6: EĞLENCE
        {"type": "GÖREV", "target": "Both", "text": "Taklidimi yap: 'Diyet yaparken gizlice mutfakta tıkınırken Büşra'ya yakalanan Kerem.'"},
        {"type": "GÖREV", "target": "Both", "text": "Telefonundan en sevdiğim şarkıyı aç ve sanki klip çekiyormuşuz gibi playback yap."},
        {"type": "GÖREV", "target": "Both", "text": "Daha önce hiç anlatmadığın küçük, komik bir sırrını ver."},
        {"type": "GÖREV", "target": "Both", "text": "İkimiz de kolumuza aynı dövmeyi yaptıracak olsak bu ne olurdu? Parmağınla koluma çizerek göster."},
        {"type": "GÖREV", "target": "Both", "text": "Bu sessiz ortamdaki imkanlarla yapabileceğin en romantik jesti yap."},
        {"type": "GÖREV", "target": "Both", "text": "'Seni seviyorum' cümlesini kurmadan beni sevdiğini 3 farklı şekilde ifade et."},
        {"type": "GÖREV", "target": "Both", "text": "Gözlerini kapat, sadece burnuma ve yanağıma dokunarak yüzümü ellerinle tanı."},
        {"type": "JOKER", "target": "Both", "text": "🃏 JOKER KARTI! Bunu sakla. Oyunun herhangi bir yerinde zor bir soruyu veya görevi 'Pas' geçmek için kullanabilirsin."},

        # SAYFA 7: ZİHİN OYUNLARI
        {"type": "GİZLİ", "target": "Both", "text": "Bu kartta ne yazdığını sesli okuma. Sadece yüzüme bak, çapkın bir gülümseme at ve konuyu tamamen değiştir."},
        {"type": "GİZLİ", "target": "Both", "text": "Bu kartı sesli okuma. Sadece bana sarıl ve 30 saniye bırakma. Nedenini sorsam bile 'Şşş' de."},
        {"type": "ŞİİR", "target": "Both", "text": "Gözlerimin içine bak ve şu dizeleri tonlayarak oku: 'Aksaray'da bir tohumdu, Üsküp'te kahkaha oldu, şimdi evimizde koca bir çınar oluyor.'"},
        {"type": "YASAK KELİME", "target": "Both", "text": "Önümüzdeki 5 dakika 'Evet' veya 'Hayır' demek yasak. Sorularıma bu kelimeleri kullanmadan cevap ver."},
        {"type": "AYNA", "target": "Both", "text": "Önümüzdeki 2 tur ben ne yaparsam (hareket, mimik, oturuş) aynısını yapmak zorundasın."},
        {"type": "ROL DEĞİŞİMİ", "target": "Both", "text": "Şu andan itibaren sen Kerem'sin, ben Büşra'yım. Bana (yani kendine) ilişkimizle ilgili merak ettiğin bir soru sor."},
        {"type": "TELEPATİ", "target": "Both", "text": "1 ile 10 arasında bir sayı tut. Gözlerimin içine bak ve o sayıyı zihninle göndermeye çalış."},
        {"type": "ZAMAN MAKİNESİ", "target": "Both", "text": "Şu an 2050 yılındayız, yaşlandık, torunlar var... Bana o günkü ses tonunla seslen ve bir su iste."},

        # SAYFA 8: FİNAL
        {"type": "GİZLİ", "target": "Both", "text": "Kartta ne yazdığını söyleme. Sadece gülümse ve 'Bunun cevabını düğün gecesi vereceğim' de."},
        {"type": "YALAN MAKİNESİ", "target": "Both", "text": "Kendinle veya ilişkimizle ilgili 2 doğru 1 yanlış detay söyle. Hangisinin yalan olduğunu gözlerinden anlamaya çalışacağım."},
        {"type": "DJ", "target": "Both", "text": "Bu kartı çeken o anki modumuza en uygun şarkıyı açmak zorunda. (Romantikse hareketli, durgunsak neşeli)."},
        {"type": "SESSİZ ÇIĞLIK", "target": "Both", "text": "Aksaray'da kediden korkup attığın çığlığı düşün... Şimdi içinden haykırmak istediğin mutluluğu fısıldayarak kulağıma söyle."},
        {"type": "FOTOĞRAFÇI", "target": "Both", "text": "Oyun dursun. Telefonu al ve tam şu anımızın, 14 Şubat'ın en doğal halinin bir fotoğrafını çek."},
        {"type": "GİZLİ", "target": "Both", "text": "Bu kartı okuma. Sadece elimi nezaketle öp ve alnına koy. Sonra hiçbir şey olmamış gibi oyuna devam et."},
        {"type": "İTİRAF", "target": "Both", "text": "'Bunu daha önce hiç söylemedim ama...' diye başlayan komik, ciddi veya şaşırtıcı bir itirafta bulun."},
        {"type": "FİNAL", "target": "Both", "text": "Sağ elini kalbime koy. Bu 14 Şubat gecesi ve yıldızlar şahit olsun ki; [Bu cümleyi içinden geldiği gibi tamamla ve 25 Nisan için söz ver]."}
    ]
    return raw_deck

# --- GÖRSELLERİ YÜKLE ---
img_sticker_busra = get_image_base64("busra")
img_sticker_kerem = get_image_base64("kerem")
img_sticker_biz = get_image_base64("biz")

# --- SESSION STATE ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'DICE'
if 'current_player' not in st.session_state:
    st.session_state.current_player = None
if 'deck' not in st.session_state:
    st.session_state.deck = init_deck()
    random.shuffle(st.session_state.deck)
if 'cards_drawn' not in st.session_state:
    st.session_state.cards_drawn = 0
if 'dice_rolled' not in st.session_state:
    st.session_state.dice_rolled = False

# --- OYUN AKIŞI ---

# 1. ZAR ATMA EKRANI
if st.session_state.game_state == 'DICE':
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='dice-container'>
        <div class='dice-title'>🎲 ZAR ATMA ZAMANI 🎲</div>
        <div class='dice-subtitle'>Her ikiniz de zar atın, yüksek çıkan başlasın!</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🎲 ZAR AT!", key="dice_button"):
            with st.spinner("Zarlar atılıyor..."):
                play_sound('dice')
                time.sleep(1)
                
                busra_dice = random.randint(1, 6)
                kerem_dice = random.randint(1, 6)
                
                st.session_state.dice_rolled = True
                
                # Eşitlik durumu
                while busra_dice == kerem_dice:
                    st.warning("🎲 Berabere! Tekrar atılıyor...")
                    time.sleep(1)
                    busra_dice = random.randint(1, 6)
                    kerem_dice = random.randint(1, 6)
                
                # Sonuçları göster
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                    <div style='text-align: center;'>
                        <h3 style='font-family: "Montserrat"; color: #be123c;'>Büşra</h3>
                        <div class='dice-box'>🎲 {busra_dice}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"""
                    <div style='text-align: center;'>
                        <h3 style='font-family: "Montserrat"; color: #be123c;'>Kerem</h3>
                        <div class='dice-box'>🎲 {kerem_dice}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                time.sleep(1)
                
                # Kazanan
                winner = "Büşra" if busra_dice > kerem_dice else "Kerem"
                st.session_state.current_player = winner
                
                st.success(f"🎊 {winner} kazandı ve oyuna başlıyor!")
                play_sound('success')
                time.sleep(2)
                
                st.session_state.game_state = 'PLAYING'
                st.rerun()

# 2. PASLAŞMA EKRANI
elif st.session_state.game_state == 'HANDOVER':
    target_person = "Büşra" if st.session_state.current_player == "Kerem" else "Kerem"
    
    st.markdown(f"""
    <div class='handover-box'>
        <div class='handover-emoji'>📱</div>
        <h1 style='font-size: 48px; margin: 0; font-family: "Playfair Display";'>TELEFONU VER!</h1>
        <h3 style='font-family: "Montserrat"; margin-top: 20px; font-weight: 400;'>
            Bu soru <b>{target_person}</b>'ya özel
        </h3>
        <p style='font-size: 18px; margin-top: 25px; line-height: 1.7; font-family: "Montserrat";'>
            Sürprizi bozmamak için okuma.<br>
            Hemen telefonu <b>{target_person.upper()}</b>'ya uzat!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"✅ Telefonu Aldım ({target_person})"):
        play_sound('transition')
        st.session_state.current_player = target_person
        st.session_state.current_card = st.session_state.pending_card
        st.session_state.game_state = 'PLAYING'
        st.rerun()

# 3. OYUN EKRANI
elif st.session_state.game_state == 'PLAYING':
    player = st.session_state.current_player
    total_cards = len(init_deck())
    remaining = len(st.session_state.deck)
    progress = ((total_cards - remaining) / total_cards) * 100
    
    # İlerleme barı
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-bar-bg'>
            <div class='progress-bar-fill' style='width: {progress}%'></div>
        </div>
        <div class='progress-text'>
            {total_cards - remaining} / {total_cards} kart çekildi • {remaining} kart kaldı
        </div>
    </div>
    """, unsafe_allow_html=True)

    if remaining > 0:
        # Kart çekme butonu
        if 'current_card' not in st.session_state:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"✨ Kart Çek ({player}) ✨", key="draw_card"):
                    with st.spinner("Kart hazırlanıyor..."):
                        play_sound('card')
                        time.sleep(0.6)
                    
                    card = st.session_state.deck.pop()
                    st.session_state.pending_card = card
                    st.session_state.cards_drawn += 1
                    
                    # Paslaşma kontrolü
                    if (player == "Kerem" and card['target'] == "Kerem") or \
                       (player == "Büşra" and card['target'] == "Busra"):
                        st.session_state.game_state = 'HANDOVER'
                    else:
                        st.session_state.current_card = card
                    
                    st.rerun()
        
        # Kartı göster
        if 'current_card' in st.session_state:
            card = st.session_state.current_card
            
            # Sticker seçimi
            sticker_html = ""
            if card['target'] == "Busra" and img_sticker_busra:
                sticker_html = f'<img src="{img_sticker_busra}" class="sticker-3d">'
            elif card['target'] == "Kerem" and img_sticker_kerem:
                sticker_html = f'<img src="{img_sticker_kerem}" class="sticker-3d">'
            elif card['target'] == "Both" and img_sticker_biz:
                sticker_html = f'<img src="{img_sticker_biz}" class="sticker-3d">'
            
            # Kart gösterimi
            st.markdown(f"""
            <div class="card-wrapper">
                <div class="white-card-box">
                    <div class="card-title-text">{card['type']}</div>
                    <div class="card-content-text">{card['text']}</div>
                </div>
                {sticker_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Özel uyarılar
            if "GİZLİ" in card['type']:
                st.toast("🤫 Bu kartı sesli okuma!", icon="🤫")
            elif "JOKER" in card['type']:
                st.toast("🃏 Joker kartını sakla!", icon="🃏")
            
            # Sonraki tur
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("➡️ Sonraki Kart", key="next_card"):
                    # Otomatik sıra değiştirme
                    new_player = "Büşra" if player == "Kerem" else "Kerem"
                    st.session_state.current_player = new_player
                    del st.session_state.current_card
                    play_sound('transition')
                    st.rerun()
    
    else:
        # OYUN BITTI
        st.balloons()
        play_sound('success')
        
        st.markdown(f"""
        <div class='game-summary'>
            <div class='summary-title'>🎊 OYUN BİTTİ! 🎊</div>
            <p style='font-family: "Montserrat"; font-size: 20px; color: #666; font-style: italic; margin: 25px 0;'>
                "{total_cards} kart, sonsuz anı, tek bir aşk hikayesi..."
            </p>
            <div class='summary-stat'>📊 Toplam kart: <b>{st.session_state.cards_drawn}</b></div>
            <div class='summary-stat'>💕 Paylaşılan anılar: <b>Paha biçilemez</b></div>
            <div class='summary-stat'>⏰ Hedefe bir adım daha yakın: <b>25 Nisan 2026</b></div>
            <div style='margin-top: 40px; font-size: 28px; color: #be123c; font-family: "Playfair Display"; font-weight: 700;'>
                İyi ki varsın Büşra ❤️
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Yeniden Başla"):
                reset_game()
                st.rerun()

# --- MÜZİK KUTUSU ---
st.markdown("""
<div class='music-box'>
    <a href="https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" target="_blank" 
       style="text-decoration: none; color: #be123c;">
        🎵 Romantic Playlist 🎵
    </a>
</div>
""", unsafe_allow_html=True)

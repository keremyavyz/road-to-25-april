import streamlit as st
import random
import time
import base64
import os
from pathlib import Path

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Road to 25 April | Elite Edition",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS: TASARIM, ANİMASYON VE 3D ETKİLER ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Lora:ital,wght@0,500;1,400&family=Montserrat:wght@300;600&display=swap');

    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 100%);
        background-attachment: fixed;
    }

    /* --- İLERLEME BARI --- */
    .progress-container {
        width: 100%;
        max-width: 450px;
        margin: 20px auto;
        background: rgba(255,255,255,0.6);
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .progress-bar {
        height: 12px;
        background: linear-gradient(90deg, #be123c, #db2777);
        border-radius: 10px;
        transition: width 0.5s ease;
        box-shadow: 0 2px 8px rgba(190, 18, 60, 0.4);
    }
    .progress-text {
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        color: #be123c;
        margin-top: 8px;
        font-weight: 600;
    }

    /* --- GİRİŞ EKRANI (BAŞLANGIÇ) --- */
    .start-screen-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 30px;
        border: 4px solid #be123c;
        text-align: center;
        box-shadow: 0 20px 50px rgba(190, 18, 60, 0.3);
        animation: fadeIn 1.5s ease-in;
        margin-top: 50px;
    }
    .start-title {
        font-family: 'Cinzel Decorative', cursive;
        color: #be123c;
        font-size: 36px;
        margin-bottom: 10px;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* --- ARA GEÇİŞ (PASLAŞMA) EKRANI --- */
    .handover-box {
        background-color: #be123c;
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 4px solid #d4af37;
        animation: pulse 2s infinite;
        margin-top: 50px;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    /* --- 3D KART YAPISI --- */
    .card-wrapper {
        position: relative;
        width: 100%;
        max-width: 450px;
        margin: 40px auto;
        perspective: 1000px;
    }

    .white-card-box {
        background: #ffffff;
        padding: 40px 25px 60px 25px;
        border-radius: 20px;
        box-shadow: 
            0 15px 35px rgba(190, 18, 60, 0.15),
            0 5px 15px rgba(0,0,0,0.05);
        text-align: center;
        border: 2px solid #d4af37;
        position: relative;
        z-index: 10;
        animation: cardFlip 0.6s ease-out;
    }
    @keyframes cardFlip {
        0% { transform: rotateY(90deg) scale(0.8); opacity: 0; }
        100% { transform: rotateY(0deg) scale(1); opacity: 1; }
    }

    /* Kart Dokusu */
    .white-card-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: #fffbf0;
        opacity: 0.6;
        border-radius: 18px;
        z-index: -1;
    }

    /* MİNİK MADALYON FOTOĞRAF */
    .mini-photo-frame {
        width: 110px;
        height: 110px;
        margin: -60px auto 20px auto;
        border-radius: 50%;
        border: 4px solid #d4af37;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        overflow: hidden;
        background-color: #fff;
        position: relative;
        z-index: 20;
    }
    .mini-photo-frame img { 
        width: 100%; 
        height: 100%; 
        object-fit: cover; 
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

    /* Metinler */
    .card-title-text {
        color: #9f1239;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 18px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #fce7f3;
        padding-bottom: 10px;
        display: inline-block;
    }
    
    .card-content-text {
        color: #374151;
        font-size: 22px;
        line-height: 1.6;
        font-family: 'Lora', serif;
        font-style: italic;
        font-weight: 500;
    }

    /* 3D STICKER (SAĞ ALT KÖŞE) */
    .sticker-3d {
        position: absolute;
        bottom: -40px;
        right: -30px;
        width: 150px;
        height: auto;
        z-index: 50;
        filter: drop-shadow(5px 10px 8px rgba(0,0,0,0.3));
        transform: rotate(-10deg);
        transition: transform 0.3s;
        pointer-events: none;
        animation: stickerBounce 2s ease-in-out infinite;
    }
    @keyframes stickerBounce {
        0%, 100% { transform: rotate(-10deg) translateY(0px); }
        50% { transform: rotate(-10deg) translateY(-5px); }
    }

    /* Butonlar */
    .stButton>button {
        background: linear-gradient(90deg, #be123c, #db2777);
        color: white;
        border-radius: 50px;
        height: 60px;
        font-size: 18px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(190, 18, 60, 0.4);
        width: 100%;
        margin-top: 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(190, 18, 60, 0.6);
    }
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    /* Müzik Player */
    .music-box {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.95);
        padding: 10px 25px;
        border-radius: 30px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        border: 1px solid #d4af37;
        z-index: 100;
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        color: #be123c;
        transition: all 0.3s ease;
    }
    .music-box:hover {
        transform: translateX(-50%) scale(1.05);
    }

    /* Oyun Sonu Özeti */
    .game-summary {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #d4af37;
        text-align: center;
        box-shadow: 0 15px 40px rgba(190, 18, 60, 0.25);
        animation: fadeIn 1s ease-in;
        margin-top: 30px;
    }
    .summary-title {
        font-family: 'Cinzel Decorative', cursive;
        color: #be123c;
        font-size: 32px;
        margin-bottom: 20px;
    }
    .summary-stat {
        font-family: 'Montserrat', sans-serif;
        font-size: 18px;
        color: #555;
        margin: 10px 0;
    }

    /* Mobil Responsive */
    @media (max-width: 768px) {
        .start-title { font-size: 28px; }
        .card-content-text { font-size: 18px; }
        .sticker-3d { width: 100px; bottom: -30px; right: -20px; }
        .mini-photo-frame { width: 90px; height: 90px; margin: -50px auto 15px auto; }
    }
</style>
""", unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---
def get_image_base64(filename):
    """Görsel dosyasını base64'e çevirir, bulamazsa None döner"""
    possible_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    base_name = Path(filename).stem
    
    for ext in possible_extensions:
        filepath = f"{base_name}{ext}"
        if os.path.exists(filepath):
            try:
                with open(filepath, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                return f"data:image/{ext[1:]};base64,{encoded}"
            except Exception as e:
                st.warning(f"Görsel yüklenirken hata: {filepath}")
                return None
    return None

def create_placeholder_image(emoji="💕"):
    """Görsel yoksa emoji placeholder döner"""
    return f'<div class="mini-photo-placeholder">{emoji}</div>'

def reset_game():
    """Tüm oyun durumunu sıfırlar"""
    for key in ['game_state', 'current_player', 'pending_card', 'current_card', 'deck', 'cards_drawn']:
        if key in st.session_state:
            del st.session_state[key]

def init_deck():
    """Desteyi oluşturur ve karıştırır"""
    raw_deck = [
        # SAYFA 1: KADER & BAŞLANGIÇ
        {"type": "SORU (BÜŞRA)", "target": "Busra", "text": "Aksaray'daki o seminerde masana kedi atladığında attığın o çığlığı hatırla... O gün kediden kaçan Büşra'dan, bugün Lila ve Simba'ya annelik yapan Büşra'ya dönüşmek sence nasıl bir yolculuktu?"},
        {"type": "SORU (BÜŞRA)", "target": "Busra", "text": "Aksaray sonrası 'Kerem kesin yazar' diye bekleyip de yazmadığım o sessiz dönem... O günlerde bana ne kadar sinirlendiğini ve içinden neler geçirdiğini dürüstçe anlatır mısın?"},
        {"type": "SORU (KEREM)", "target": "Kerem", "text": "Büşra'nın ayna karşısında kediyle attığı o story bildirimi ekrana düştüğünde... Kerem, cevap yazmadan önce kaç dakika 'Ne yazsam?' diye düşündün ve ne kadar gergindin?"},
        {"type": "SORU (KADER)", "target": "Both", "text": "Adıyaman depremi olmasa belki de İstanbul'a hiç dönmeyecektim... Bizi tekrar bir araya getiren bu 'Kader' hakkında ne hissediyorsun? Tesadüf mü, yoksa kaçınılmaz son mu?"},
        {"type": "İTİRAF", "target": "Both", "text": "Göktürk Starbucks'ta o ilk kahveyi içerken... Karşındaki kişiye bakıp aklından geçen ama 'Henüz çok erken' diyerek söylemeye cesaret edemediğin o ilk düşünce neydi?"},
        {"type": "SORU (KEREM)", "target": "Kerem", "text": "6 Temmuz'da, kendi doğum gününü feda edip evlilik teklifi etmek... Bu tarihi seçerken aklındaki asıl mesaj neydi? 'En büyük hediyem sensin' mi?"},
        {"type": "SORU (BÜŞRA)", "target": "Busra", "text": "Tekirdağ Uçmakdere'deki dağ evinde o an geldiğinde... Kerem diz çökmeden hemen önce durumu hissettin mi, yoksa o an dünya gerçekten durdu mu?"},
        {"type": "ANI", "target": "Both", "text": "Balkanlar tatilinde, Üsküp yolunda arabada deliler gibi gülme krizine girdiğimiz o gece... Sence bizi birbirimize asıl 'mühürleyen' an o kahkahalar mıydı?"},
        
        # SAYFA 2: YUVA & GELECEK
        {"type": "HAYAL ET", "target": "Both", "text": "25 Nisan sabahı gözlerini açtığında, tüm o düğün telaşı ve stresi haricinde kalbinde hissetmek istediğin en baskın duygu ne?"},
        {"type": "HAYAL ET", "target": "Both", "text": "Kendi evimizi aldığımızda, kapıdan içeri girer girmez 'Oh be, burası bizim kalemiz' dedirtecek o ilk detay veya eşya ne olmalı?"},
        {"type": "GERÇEKÇİLİK", "target": "Both", "text": "Evliliğimizin ilk yılında bizi en çok neyin zorlayacağını düşünüyorsun ve biz 'Takım' olarak bunu nasıl aşacağız?"},
        {"type": "ROMANTİK", "target": "Both", "text": "Düğün dansımız sırasında, herkes bizi izlerken kulağına fısıldamamı istediğin, sadece ikimizin duyacağı o özel cümle ne?"},
        {"type": "DÜRÜSTLÜK", "target": "Kerem", "text": "Müstakbel eşin olarak, şu an benimle ilgili kafandaki en büyük 'Acaba' veya endişe nedir?"},
        {"type": "EV HALİ", "target": "Both", "text": "Yeni evimizde, 'Burası kesinlikle benim alanım, sakın müdahale etme' diyeceğin o dokunulmaz bölge neresi?"},
        {"type": "EV HALİ", "target": "Both", "text": "Ev işleri söz konusu olduğunda sence ilk büyük kavgamız neyden çıkar? (Ortada bırakılan çoraplar, bir türlü boşalmayan bulaşık makinesi?)"},
        {"type": "MÜZİK", "target": "Both", "text": "Pejo 308 mazide kaldı... Alacağımız yeni arabada, kontağı çevirdiğimiz an son ses açıp dinleyeceğimiz 'Bizi anlatan' ilk şarkı hangisi olmalı?"},

        # SAYFA 3: AİLE & BİZ
        {"type": "EĞLENCE", "target": "Both", "text": "Düğün gecesi sence (biz hariç) pistten inmeyen, en çok coşan veya sarhoş olan o sürpriz isim kim olacak?"},
        {"type": "EV HALİ", "target": "Both", "text": "Evlendiğimizin ilk sabahı, o huzurlu Pazar kahvaltısını sence kim hazırlar? (Gerçekçi olalım)."},
        {"type": "AİLE", "target": "Both", "text": "Benim ailemle (özellikle Yusuf babamla) ilgili gözlemlediğin, seni en çok güldüren veya içini ısıtan özellik ne?"},
        {"type": "GELECEK", "target": "Both", "text": "Geleceği hayal et... Sence biz nasıl bir anne-baba olacağız? Birbirimizin ebeveynlik potansiyeline 10 üzerinden puan verelim."},
        {"type": "EĞLENCE", "target": "Both", "text": "Düğün dansımızda heyecandan ayağına basma ihtimalim sence yüzde kaç? (Dürüst ol, alınmam)."},
        {"type": "EV HALİ", "target": "Both", "text": "İleride evde bir kriz çıktığında sence 'İyi Polis' kim, 'Kötü Polis' kim olacak?"},
        {"type": "YEMEK", "target": "Kerem", "text": "Diyetimi ve sporumu tek bir yemekle bozma hakkım olsa, önüme ne koyardın da asla 'Hayır' diyemezdim?"},
        {"type": "BENZETME", "target": "Both", "text": "Beni bir çizgi film veya film karakterine benzetsen, huyum suyum en çok kime benziyor?"},

        # SAYFA 4: DERİN & GÖREV
        {"type": "MÜZİK (JUST B)", "target": "Kerem", "text": "Hayatının sonuna kadar sadece tek bir şarkımı dinleyebilecek olsan, 'Just B' albümünden hangisini seçerdin ve neden?"},
        {"type": "GÖREV (FOTOĞRAF)", "target": "Both", "text": "Telefonunu eline al, galerine gir ve benim en komik, en ifşa fotoğrafımı bulup göster. Hikayesini anlat."},
        {"type": "GÖREV (DANS)", "target": "Both", "text": "Ayağa kalk! Düğün dansımızın kısa bir provasını yapıyoruz. Müzik yok, mırıldanmak serbest."},
        {"type": "GÖREV (TAKLİT)", "target": "Both", "text": "Beni 1 dakika boyunca 'İngilizce Öğretmeni Kerem' edasıyla, sınıfı yönetiyormuşum gibi taklit et."},
        {"type": "GÖREV (DOĞAÇLAMA)", "target": "Kerem", "text": "'Just B' moduna geç! Bana şu an uydurduğun, içinde 'Lila', 'Simba' ve '14 Şubat' geçen 2 satırlık bir şarkı söyle."},
        {"type": "GÖREV (HARF)", "target": "Both", "text": "Gözlerimi kapatacağım, avucuma parmağınla bir harf çizeceksin. Bilirsem dile benden ne dilersen."},
        {"type": "GÖREV (SUNUM)", "target": "Both", "text": "Bana, neden beni sevdiğine dair 3 maddelik, çok hızlı ve ikna edici bir sunum yap."},
        {"type": "GÖREV (RİTİM)", "target": "Both", "text": "Telefonunu çıkar, rastgele bir şarkı aç. Çalan şarkının ritmine göre dans etmek zorundayız."},

        # SAYFA 5: AKSİYON
        {"type": "GÖREV (SESSİZLİK)", "target": "Both", "text": "1 dakika boyunca konuşmak yasak. Sadece gözlerimin içine bakacaksın. İlk gülen veya gözünü kaçıran kaybeder (ve öper)."},
        {"type": "GÖREV (SESSİZ SİNEMA)", "target": "Both", "text": "Benim en sevdiğin huyumu veya özelliğimi, hiç konuşmadan sadece hareketlerle anlat."},
        {"type": "GÖREV (TERS KÖŞE)", "target": "Both", "text": "Bana hayatımda duyduğum en saçma veya en kötü iltifatı et. (Ne kadar yaratıcısın görelim)."},
        {"type": "GÖREV (PAZARLAMA)", "target": "Both", "text": "Şu an masadaki veya odadaki herhangi bir objeyi eline al ve bana onu dünyanın en değerli şeyiymiş gibi satmaya çalış."},
        {"type": "GÖREV (HİTAP)", "target": "Both", "text": "Önümüzdeki 3 tur boyunca her cümleme 'Zümre Başkanım' veya 'Hocam' diye başlamak zorundasın."},
        {"type": "GÖREV (SÖZ VER)", "target": "Both", "text": "Elimi sıkıca tut. 25 Nisan 2026 için bana şu an sesli, kalpten gelen bir söz ver."},
        {"type": "GÖREV (TARİF)", "target": "Both", "text": "Bana yaptığın veya yapacağın en güzel yemeğin tarifini, dünyanın en gizemli sırrını veriyormuşsun gibi anlat."},
        {"type": "GÖREV (MASAJ)", "target": "Both", "text": "Sırtıma veya omuzlarıma 30 saniye masaj yap. (Sınav stresi ve düğün yorgunluğu gitsin)."},

        # SAYFA 6: EĞLENCE
        {"type": "GÖREV (YAKALANDIN)", "target": "Both", "text": "Taklidimi yap: 'Diyet yaparken gizlice mutfakta bir şeyler tıkınırken Büşra'ya yakalanan Kerem.'"},
        {"type": "GÖREV (PLAYBACK)", "target": "Both", "text": "Kendi telefonundan benim en sevdiğin şarkımı aç ve sanki klip çekiyormuşuz gibi playback yaparak söyle."},
        {"type": "GÖREV (SIR)", "target": "Both", "text": "Bana daha önce hiç anlatmadığın küçük, komik bir sırrını ver."},
        {"type": "GÖREV (DÖVME)", "target": "Both", "text": "Eğer ikimiz de kolumuza aynı dövmeyi yaptıracak olsak bu ne olurdu? Parmağınla koluma çizerek göster."},
        {"type": "GÖREV (ROMANTİZM)", "target": "Both", "text": "Bu sessiz ortamdaki imkanlarla yapabileceğin en romantik jesti yap."},
        {"type": "GÖREV (YASAK KELİME)", "target": "Both", "text": "Bana 'Seni seviyorum' cümlesini KURMADAN, beni sevdiğini 3 farklı şekilde ifade et."},
        {"type": "GÖREV (TANI)", "target": "Both", "text": "Gözlerini kapat, sadece burnuma ve yanağıma dokunarak yüzümü ellerinle tanı."},
        {"type": "JOKER KARTI", "target": "Both", "text": "🃏 Bu kartı sakla! Oyunun herhangi bir yerinde zor bir soruyu veya görevi 'Pas' geçmek için kullanabilirsin."},

        # SAYFA 7: ZİHİN OYUNLARI
        {"type": "İÇİNDEN OKU", "target": "Both", "text": "Bu kartta ne yazdığını SESLİ OKUMA. Sadece yüzüme bak, çapkın bir şekilde gülümse ve konuyu tamamen değiştir. (Beni meraktan çatlat)."},
        {"type": "İÇİNDEN OKU", "target": "Both", "text": "Bu kartı SESLİ OKUMA. Sadece bana sarıl ve 30 saniye boyunca hiç bırakma. Nedenini sorsam bile 'Şşş' de."},
        {"type": "ŞİİR MODU", "target": "Both", "text": "Gözlerimin içine bak ve şu dizeleri tonlayarak oku: 'Aksaray'da bir tohumdu, Üsküp'te kahkaha oldu, şimdi evimizde koca bir çınar oluyor.'"},
        {"type": "YASAK KELİME", "target": "Both", "text": "Önümüzdeki 5 dakika boyunca 'Evet' veya 'Hayır' demek yasak. Sorularıma bu kelimeleri kullanmadan cevap ver. Yanarsan ceza var!"},
        {"type": "AYNA", "target": "Both", "text": "Önümüzdeki 2 tur boyunca ben ne yaparsam (hareket, mimik, oturuş) aynısını yapmak zorundasın. Ben aynayım, sen yansımasın."},
        {"type": "ROL DEĞİŞİMİ", "target": "Both", "text": "Şu andan itibaren sen Kerem'sin, ben Büşra'yım. Bana (yani kendine) ilişkimizle ilgili merak ettiğin bir soru sor."},
        {"type": "TELEPATİ", "target": "Both", "text": "1 ile 10 arasında bir sayı tut. Gözlerimin en derinine bak ve o sayıyı bana zihninle göndermeye çalış."},
        {"type": "ZAMAN MAKİNESİ", "target": "Both", "text": "Şu an 2050 yılındayız, yaşlandık, torunlar var... Bana o günkü ses tonunla seslen ve benden bir su iste."},

        # SAYFA 8: FİNAL
        {"type": "İÇİNDEN OKU", "target": "Both", "text": "Kartta ne yazdığını söyleme. Sadece gülümse ve 'Bunun cevabını düğün gecesi vereceğim' de."},
        {"type": "YALAN MAKİNESİ", "target": "Both", "text": "Bana kendinle veya ilişkimizle ilgili 2 doğru 1 yanlış detay söyle. Hangisinin yalan olduğunu gözlerinden anlamaya çalışacağım."},
        {"type": "DJ KEREM", "target": "Both", "text": "Bu kartı çeken, o anki modumuza en uygun şarkıyı açmak zorunda. (Romantikse hareketli, durgunsak neşeli)."},
        {"type": "SESSİZ ÇIĞLIK", "target": "Both", "text": "Aksaray'da kediden korkup attığın o çığlığı düşün... Şimdi içinden haykırmak istediğin mutluluğu fısıldayarak kulağıma söyle."},
        {"type": "FOTOĞRAFÇI", "target": "Both", "text": "Oyun dursun. Telefonu al ve tam şu anımızın, 14 Şubat'ın en doğal halinin bir fotoğrafını çek."},
        {"type": "İÇİNDEN OKU", "target": "Both", "text": "Bu kartı okuma. Sadece elimi nezaketle öp ve alnına koy. Sonra hiçbir şey olmamış gibi oyuna devam et."},
        {"type": "BÜYÜK İTİRAF", "target": "Both", "text": "'Bunu daha önce hiç söylemedim ama...' diye başlayan komik, ciddi veya şaşırtıcı bir itirafta bulun."},
        {"type": "FİNAL KARTI (YEMİN)", "target": "Both", "text": "Sağ elini kalbime koy. Bu 14 Şubat gecesi ve yıldızlar şahit olsun ki; [Bu cümleyi içinden geldiği gibi tamamla ve 25 Nisan için bana söz ver]."}
    ]
    return raw_deck

# --- GÖRSELLERİ YÜKLE ---
img_sticker_busra = get_image_base64("busra")
img_sticker_kerem = get_image_base64("kerem")
img_sticker_biz = get_image_base64("biz")

img_mini_busra = get_image_base64("busra")
img_mini_kerem = get_image_base64("kerem")
img_mini_biz = get_image_base64("biz")

# --- OYUN DURUMU (SESSION STATE) ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'START'
if 'current_player' not in st.session_state:
    st.session_state.current_player = None
if 'pending_card' not in st.session_state:
    st.session_state.pending_card = None
if 'deck' not in st.session_state:
    st.session_state.deck = init_deck()
    random.shuffle(st.session_state.deck)
if 'cards_drawn' not in st.session_state:
    st.session_state.cards_drawn = 0

# --- ANA OYUN AKIŞI ---

# 1. BAŞLANGIÇ EKRANI
if st.session_state.game_state == 'START':
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='start-screen-box'>
        <div class='start-title'>💕 HAZIR MISINIZ? 💕</div>
        <div style='font-size: 20px; color: #555; font-family: "Montserrat"; margin: 15px 0;'>14 Şubat Gecesi Başlıyor...</div>
        <div style='margin-top:20px; font-size: 16px; color: #be123c; font-weight: 600;'>Road to 25 April</div>
        <div style='margin-top:10px; font-size: 14px; color: #888;'>64 kart • Sonsuz anı • 1 aşk hikayesi</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎲 KİMİN BAŞLAYACAĞINI SEÇ 🎲"):
        with st.spinner("Kader Çarkı Dönüyor..."):
            time.sleep(2)
        winner = random.choice(["Kerem", "Büşra"])
        st.session_state.current_player = winner
        st.session_state.game_state = 'PLAYING'
        st.success(f"🎊 {winner} başlıyor!")
        time.sleep(1)
        st.rerun()

# 2. PASLAŞMA EKRANI (Handover)
elif st.session_state.game_state == 'HANDOVER':
    
    target_person = "Büşra" if st.session_state.current_player == "Kerem" else "Kerem"
    
    st.markdown(f"""
    <div class='handover-box'>
        <h1 style='font-size: 50px; margin:0;'>🛑 HOP!</h1>
        <h3 style='font-family:"Montserrat"; margin-top:10px;'>Bu Soru Sana Geldi!</h3>
        <p style='font-size: 18px; margin-top:20px; line-height:1.5;'>
            Sürprizi bozmamak için okuma.<br>
            Telefonu hemen <b>{target_person.upper()}</b>'ya uzat!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"✅ Telefonu Aldım ({target_person})"):
        st.session_state.current_player = target_person
        st.session_state.current_card = st.session_state.pending_card
        st.session_state.game_state = 'PLAYING'
        st.rerun()

# 3. OYUN EKRANI (Playing)
elif st.session_state.game_state == 'PLAYING':
    
    player = st.session_state.current_player
    total_cards = 64
    remaining = len(st.session_state.deck)
    progress = ((total_cards - remaining) / total_cards) * 100
    
    # İlerleme Barı
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-bar' style='width: {progress}%'></div>
        <div class='progress-text'>İlerleme: {total_cards - remaining}/{total_cards} kart çekildi</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Başlık
    st.markdown("<h2 style='text-align: center; color: #be123c; font-family: \"Cinzel Decorative\"; margin-top: 10px;'>ROAD TO 25 APRIL 💍</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#777; font-size:14px;'>Sıra: <b style='color:#be123c;'>{player.upper()}</b> | Kalan: <b>{remaining}</b></p>", unsafe_allow_html=True)

    if remaining > 0:
        if st.button(f"✨ Kart Çek ({player}) ✨"):
            with st.spinner("Kart hazırlanıyor..."):
                time.sleep(0.5)
            
            card = st.session_state.deck.pop()
            st.session_state.pending_card = card
            st.session_state.cards_drawn += 1
            
            # Paslaşma Mantığı
            if player == "Kerem" and card['target'] == "Kerem":
                st.session_state.game_state = 'HANDOVER'
            elif player == "Büşra" and card['target'] == "Busra":
                st.session_state.game_state = 'HANDOVER'
            else:
                st.session_state.current_card = card
            
            st.rerun()
            
        # Kartı Göster
        if 'current_card' in st.session_state:
            card = st.session_state.current_card
            
            # Görsel Seçimi
            mini_photo_html = ""
            sticker_html = ""
            
            if card['target'] == "Busra":
                if img_mini_busra:
                    mini_photo_html = f'<img src="{img_mini_busra}">'
                else:
                    mini_photo_html = create_placeholder_image("👰")
                if img_sticker_busra:
                    sticker_html = f'<img src="{img_sticker_busra}" class="sticker-3d">'
            elif card['target'] == "Kerem":
                if img_mini_kerem:
                    mini_photo_html = f'<img src="{img_mini_kerem}">'
                else:
                    mini_photo_html = create_placeholder_image("🤵")
                if img_sticker_kerem:
                    sticker_html = f'<img src="{img_sticker_kerem}" class="sticker-3d">'
            else:  # Both
                if img_mini_biz:
                    mini_photo_html = f'<img src="{img_mini_biz}">'
                else:
                    mini_photo_html = create_placeholder_image("💑")
                if img_sticker_biz:
                    sticker_html = f'<img src="{img_sticker_biz}" class="sticker-3d">'
            
            # HTML Kart
            st.markdown(f"""
            <div class="card-wrapper">
                <div class="white-card-box">
                    <div class="mini-photo-frame">{mini_photo_html}</div>
                    <div class="card-title-text">{card['type']}</div>
                    <div class="card-content-text">{card['text']}</div>
                </div>
                {sticker_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Özel kart uyarıları
            if "İÇİNDEN OKU" in card['type']:
                st.toast("🤫 Şşş! Bu kartı sesli okuma!", icon="🤫")
            elif "JOKER" in card['type']:
                st.toast("🃏 Joker kartını sakla, sonra kullanabilirsin!", icon="🃏")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Sırayı Devret"):
                    new_player = "Büşra" if player == "Kerem" else "Kerem"
                    st.session_state.current_player = new_player
                    if 'current_card' in st.session_state:
                        del st.session_state.current_card
                    st.rerun()
            
            with col2:
                if st.button("🔀 Desteyi Karıştır"):
                    random.shuffle(st.session_state.deck)
                    st.success("Deste karıştırıldı!")
                    time.sleep(0.5)
                    st.rerun()

    else:
        # OYUN SONU
        st.balloons()
        
        st.markdown(f"""
        <div class='game-summary'>
            <div class='summary-title'>🎊 OYUN BİTTİ! 🎊</div>
            <div style='font-size: 18px; color: #555; font-family: "Lora"; font-style: italic; margin: 20px 0;'>
                "64 kart, sonsuz anı, tek bir aşk hikayesi..."
            </div>
            <div class='summary-stat'>📊 Toplam çekilen kart: <b>{st.session_state.cards_drawn}</b></div>
            <div class='summary-stat'>💕 Paylaşılan anılar: <b>Paha biçilemez</b></div>
            <div class='summary-stat'>⏰ Bir adım daha yaklaştınız: <b>25 Nisan 2026</b></div>
            <div style='margin-top: 30px; font-size: 24px; color: #be123c; font-family: "Cinzel Decorative";'>
                İyi ki varsın Büşra ❤️
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Yeniden Başla"):
                reset_game()
                st.rerun()
        with col2:
            if st.button("📸 Anı Defterine Kaydet"):
                st.info("Bu özellik yakında eklenecek!")

# --- MÜZİK KUTUSU ---
st.markdown("""
<div class='music-box'>
    <a href="https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" target="_blank" style="text-decoration:none; color:#be123c;">
        🎵 Romantik Müzik Aç 🎵
    </a>
</div>
""", unsafe_allow_html=True)

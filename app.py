import streamlit as st
import random
import time

# --- SAYFA AYARLARI (PREMIUM) ---
st.set_page_config(
    page_title="Road to 25 April | Elite Edition",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- GÖRSEL YÜKLEME FONKSİYONU ---
# (Eğer fotoğraflar yoksa hata vermesin diye try-except bloğu)
def show_image(image_name, caption_text=None):
    try:
        st.image(image_name, caption=caption_text, use_column_width=True)
    except Exception:
        st.warning(f"⚠️ '{image_name}' fotoğrafı bulunamadı. Lütfen GitHub'a yüklediğinden emin ol.")

# --- ÖZEL CSS (ELITE TASARIM & ANİMASYON) ---
st.markdown("""
<style>
    /* Google Fonts İçe Aktarma (Daha sofistike fontlar) */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Lora:ital,wght@0,500;1,400&display=swap');

    /* Ana Arka Plan - Romantik Gradyan */
    .stApp {
        background: linear-gradient(to bottom right, #fff0f5, #ffe4e1);
    }

    /* KART ANİMASYONU (Alttan süzülerek gelme) */
    @keyframes slideInUp {
      from {
        transform: translateY(50px);
        opacity: 0;
      }
      to {
        transform: translateY(0);
        opacity: 1;
      }
    }

    /* KART KONTEYNERİ (Lüks Görünüm) */
    .card-container {
        animation: slideInUp 0.8s ease-out; /* Animasyon burada */
        background-color: #ffffff;
        padding: 40px;
        border-radius: 25px;
        /* Derinlik hissi veren güçlü gölge */
        box-shadow: 0 20px 40px rgba(190, 18, 60, 0.2);
        text-align: center;
        /* Altın Sarısı Çerçeve */
        border: 3px solid #d4af37; 
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    /* Kartın üstüne ince bir parlama efekti */
    .card-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 10px;
        background: linear-gradient(to right, #be123c, #d4af37, #be123c);
    }

    /* KART BAŞLIĞI (Altın & Cinzel Font) */
    .card-title {
        color: #d4af37; /* Altın Rengi */
        font-family: 'Cinzel Decorative', cursive;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 25px;
        letter-spacing: 1px;
        text-transform: uppercase;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* KART İÇERİĞİ (Lora Font) */
    .card-content {
        color: #4b5563;
        font-size: 24px;
        line-height: 1.7;
        font-weight: 500;
        font-family: 'Lora', serif;
        font-style: italic;
    }

    /* ALT BİLGİ */
    .footer-text {
        color: #9ca3af;
        font-size: 14px;
        text-align: center;
        margin-top: 60px;
        font-family: 'Cinzel Decorative', cursive;
    }

    /* SAYAÇ */
    .counter {
        color: #be123c;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Cinzel Decorative', cursive;
    }

    /* BUTON TASARIMI (Lüks Buton) */
    .stButton>button {
        background: linear-gradient(45deg, #be123c, #9f1239);
        color: white;
        border-radius: 50px; /* Daha yuvarlak */
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border: 2px solid #d4af37; /* Altın çerçeveli buton */
        box-shadow: 0 5px 15px rgba(190, 18, 60, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(190, 18, 60, 0.5);
        background: linear-gradient(45deg, #9f1239, #be123c);
    }
    
    /* Fotoğrafların kenarlarını yumuşat */
    img {
        border-radius: 15px;
        border: 2px solid #d4af37;
        margin-bottom: 20px;
    }
    
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown("<h1 style='text-align: center; color: #be123c; font-family: \"Cinzel Decorative\", cursive; font-size: 3rem;'>ROAD TO 25 APRIL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37; font-family: \"Lora\", serif; font-style: italic;'>Kerem & Büşra | 14 Şubat Elite Edition ⚜️</p>", unsafe_allow_html=True)
st.divider()

# --- KART LİSTESİ (64 ADET - DEĞİŞMEDİ) ---
if 'deck' not in st.session_state:
    st.session_state.deck = [
        # SAYFA 1: KADER & BAŞLANGIÇ
        {"type": "SORU (BÜŞRA)", "text": "Aksaray'daki o seminerde masana kedi atladığında attığın o çığlığı hatırla... O gün kediden kaçan Büşra'dan, bugün Lila ve Simba'ya annelik yapan Büşra'ya dönüşmek sence nasıl bir yolculuktu?"},
        {"type": "SORU (BÜŞRA)", "text": "Aksaray sonrası 'Kerem kesin yazar' diye bekleyip de yazmadığım o sessiz dönem... O günlerde bana ne kadar sinirlendiğini ve içinden neler geçirdiğini dürüstçe anlatır mısın?"},
        {"type": "SORU (KEREM)", "text": "Büşra'nın ayna karşısında kediyle attığı o story bildirimi ekrana düştüğünde... Kerem, cevap yazmadan önce kaç dakika 'Ne yazsam?' diye düşündün ve ne kadar gergindin?"},
        {"type": "SORU (KADER)", "text": "Adıyaman depremi olmasa belki de İstanbul'a hiç dönmeyecektim... Bizi tekrar bir araya getiren bu 'Kader' hakkında ne hissediyorsun? Tesadüf mü, yoksa kaçınılmaz son mu?"},
        {"type": "İTİRAF", "text": "Göktürk Starbucks'ta o ilk kahveyi içerken... Karşındaki kişiye bakıp aklından geçen ama 'Henüz çok erken' diyerek söylemeye cesaret edemediğin o ilk düşünce neydi?"},
        {"type": "SORU (KEREM)", "text": "6 Temmuz'da, kendi doğum gününü feda edip evlilik teklifi etmek... Bu tarihi seçerken aklındaki asıl mesaj neydi? 'En büyük hediyem sensin' mi?"},
        {"type": "SORU (BÜŞRA)", "text": "Tekirdağ Uçmakdere'deki dağ evinde o an geldiğinde... Kerem diz çökmeden hemen önce durumu hissettin mi, yoksa o an dünya gerçekten durdu mu?"},
        {"type": "ANI", "text": "Balkanlar tatilinde, Üsküp yolunda arabada deliler gibi gülme krizine girdiğimiz o gece... Sence bizi birbirimize asıl 'mühürleyen' an o kahkahalar mıydı?"},
        
        # SAYFA 2: YUVA & GELECEK
        {"type": "HAYAL ET", "text": "25 Nisan sabahı gözlerini açtığında, tüm o düğün telaşı ve stresi haricinde kalbinde hissetmek istediğin en baskın duygu ne?"},
        {"type": "HAYAL ET", "text": "Kendi evimizi aldığımızda, kapıdan içeri girer girmez 'Oh be, burası bizim kalemiz' dedirtecek o ilk detay veya eşya ne olmalı?"},
        {"type": "GERÇEKÇİLİK", "text": "Evliliğimizin ilk yılında bizi en çok neyin zorlayacağını düşünüyorsun ve biz 'Takım' olarak bunu nasıl aşacağız?"},
        {"type": "ROMANTİK", "text": "Düğün dansımız sırasında, herkes bizi izlerken kulağına fısıldamamı istediğin, sadece ikimizin duyacağı o özel cümle ne?"},
        {"type": "DÜRÜSTLÜK", "text": "Müstakbel eşin olarak, şu an benimle ilgili kafandaki en büyük 'Acaba' veya endişe nedir?"},
        {"type": "EV HALİ", "text": "Yeni evimizde, 'Burası kesinlikle benim alanım, sakın müdahale etme' diyeceğin o dokunulmaz bölge neresi?"},
        {"type": "EV HALİ", "text": "Ev işleri söz konusu olduğunda sence ilk büyük kavgamız neyden çıkar? (Ortada bırakılan çoraplar, bir türlü boşalmayan bulaşık makinesi?)"},
        {"type": "MÜZİK", "text": "Pejo 308 mazide kaldı... Alacağımız yeni arabada, kontağı çevirdiğimiz an son ses açıp dinleyeceğimiz 'Bizi anlatan' ilk şarkı hangisi olmalı?"},

        # SAYFA 3: AİLE & BİZ
        {"type": "EĞLENCE", "text": "Düğün gecesi sence (biz hariç) pistten inmeyen, en çok coşan veya sarhoş olan o sürpriz isim kim olacak?"},
        {"type": "EV HALİ", "text": "Evlendiğimizin ilk sabahı, o huzurlu Pazar kahvaltısını sence kim hazırlar? (Gerçekçi olalım)."},
        {"type": "AİLE", "text": "Benim ailemle (özellikle Yusuf babamla) ilgili gözlemlediğin, seni en çok güldüren veya içini ısıtan özellik ne?"},
        {"type": "GELECEK", "text": "Geleceği hayal et... Sence biz nasıl bir anne-baba olacağız? Birbirimizin ebeveynlik potansiyeline 10 üzerinden puan verelim."},
        {"type": "EĞLENCE", "text": "Düğün dansımızda heyecandan ayağına basma ihtimalim sence yüzde kaç? (Dürüst ol, alınmam)."},
        {"type": "EV HALİ", "text": "İleride evde bir kriz çıktığında sence 'İyi Polis' kim, 'Kötü Polis' kim olacak?"},
        {"type": "YEMEK", "text": "Diyetimi ve sporumu tek bir yemekle bozma hakkım olsa, önüme ne koyardın da asla 'Hayır' diyemezdim?"},
        {"type": "BENZETME", "text": "Beni bir çizgi film veya film karakterine benzetsen, huyum suyum en çok kime benziyor?"},

        # SAYFA 4: DERİN & GÖREV BAŞLIYOR
        {"type": "MÜZİK (JUST B)", "text": "Hayatının sonuna kadar sadece tek bir şarkımı dinleyebilecek olsan, 'Just B' albümünden hangisini seçerdin ve neden?"},
        {"type": "GÖREV (FOTOĞRAF)", "text": "Telefonunu eline al, galerine gir ve benim en komik, en ifşa fotoğrafımı bulup göster. Hikayesini anlat."},
        {"type": "GÖREV (DANS)", "text": "Ayağa kalk! Düğün dansımızın kısa bir provasını yapıyoruz. Müzik yok, mırıldanmak serbest."},
        {"type": "GÖREV (TAKLİT)", "text": "Beni 1 dakika boyunca 'İngilizce Öğretmeni Kerem' edasıyla, sınıfı yönetiyormuşum gibi taklit et."},
        {"type": "GÖREV (DOĞAÇLAMA)", "text": "'Just B' moduna geç! Bana şu an uydurduğun, içinde 'Lila', 'Simba' ve '14 Şubat' geçen 2 satırlık bir şarkı söyle."},
        {"type": "GÖREV (HARF)", "text": "Gözlerimi kapatacağım, avucuma parmağınla bir harf çizeceksin. Bilirsem dile benden ne dilersen."},
        {"type": "GÖREV (SUNUM)", "text": "Bana, neden beni sevdiğine dair 3 maddelik, çok hızlı ve ikna edici bir sunum yap."},
        {"type": "GÖREV (RİTİM)", "text": "Telefonunu çıkar, rastgele bir şarkı aç. Çalan şarkının ritmine göre dans etmek zorundayız."},

        # SAYFA 5: AKSİYON
        {"type": "GÖREV (SESSİZLİK)", "text": "1 dakika boyunca konuşmak yasak. Sadece gözlerimin içine bakacaksın. İlk gülen veya gözünü kaçıran kaybeder (ve öper)."},
        {"type": "GÖREV (SESSİZ SİNEMA)", "text": "Benim en sevdiğin huyumu veya özelliğimi, hiç konuşmadan sadece hareketlerle anlat."},
        {"type": "GÖREV (TERS KÖŞE)", "text": "Bana hayatımda duyduğum en saçma veya en kötü iltifatı et. (Ne kadar yaratıcısın görelim)."},
        {"type": "GÖREV (PAZARLAMA)", "text": "Şu an masadaki veya odadaki herhangi bir objeyi eline al ve bana onu dünyanın en değerli şeyiymiş gibi satmaya çalış."},
        {"type": "GÖREV (HİTAP)", "text": "Önümüzdeki 3 tur boyunca her cümleme 'Zümre Başkanım' veya 'Hocam' diye başlamak zorundasın."},
        {"type": "GÖREV (SÖZ VER)", "text": "Elimi sıkıca tut. 25 Nisan 2026 için bana şu an sesli, kalpten gelen bir söz ver."},
        {"type": "GÖREV (TARİF)", "text": "Bana yaptığın veya yapacağın en güzel yemeğin tarifini, dünyanın en gizemli sırrını veriyormuşsun gibi anlat."},
        {"type": "GÖREV (MASAJ)", "text": "Sırtıma veya omuzlarıma 30 saniye masaj yap. (Sınav stresi ve düğün yorgunluğu gitsin)."},

        # SAYFA 6: EĞLENCE
        {"type": "GÖREV (YAKALANDIN)", "text": "Taklidimi yap: 'Diyet yaparken gizlice mutfakta bir şeyler tıkınırken Büşra'ya yakalanan Kerem.'"},
        {"type": "GÖREV (PLAYBACK)", "text": "Kendi telefonundan benim en sevdiğin şarkımı aç ve sanki klip çekiyormuşuz gibi playback yaparak söyle."},
        {"type": "GÖREV (SIR)", "text": "Bana daha önce hiç anlatmadığın küçük, komik bir sırrını ver."},
        {"type": "GÖREV (DÖVME)", "text": "Eğer ikimiz de kolumuza aynı dövmeyi yaptıracak olsak bu ne olurdu? Parmağınla koluma çizerek göster."},
        {"type": "GÖREV (ROMANTİZM)", "text": "Bu sessiz ortamdaki imkanlarla yapabileceğin en romantik jesti yap."},
        {"type": "GÖREV (YASAK KELİME)", "text": "Bana 'Seni seviyorum' cümlesini KURMADAN, beni sevdiğini 3 farklı şekilde ifade et."},
        {"type": "GÖREV (TANI)", "text": "Gözlerini kapat, sadece burnuma ve yanağıma dokunarak yüzümü ellerinle tanı."},
        {"type": "JOKER KARTI", "text": "Bu kartı sakla! Oyunun herhangi bir yerinde zor bir soruyu veya görevi 'Pas' geçmek için kullanabilirsin."},

        # SAYFA 7: ZİHİN OYUNLARI
        {"type": "İÇİNDEN OKU", "text": "Bu kartta ne yazdığını SESLİ OKUMA. Sadece yüzüme bak, çapkın bir şekilde gülümse ve konuyu tamamen değiştir. (Beni meraktan çatlat)."},
        {"type": "İÇİNDEN OKU", "text": "Bu kartı SESLİ OKUMA. Sadece bana sarıl ve 30 saniye boyunca hiç bırakma. Nedenini sorsam bile 'Şşş' de."},
        {"type": "ŞİİR MODU", "text": "Gözlerimin içine bak ve şu dizeleri tonlayarak oku: 'Aksaray'da bir tohumdu, Üsküp'te kahkaha oldu, şimdi evimizde koca bir çınar oluyor.'"},
        {"type": "YASAK KELİME", "text": "Önümüzdeki 5 dakika boyunca 'Evet' veya 'Hayır' demek yasak. Sorularıma bu kelimeleri kullanmadan cevap ver. Yanarsan ceza var!"},
        {"type": "AYNA", "text": "Önümüzdeki 2 tur boyunca ben ne yaparsam (hareket, mimik, oturuş) aynısını yapmak zorundasın. Ben aynayım, sen yansımasın."},
        {"type": "ROL DEĞİŞİMİ", "text": "Şu andan itibaren sen Kerem'sin, ben Büşra'yım. Bana (yani kendine) ilişkimizle ilgili merak ettiğin bir soru sor."},
        {"type": "TELEPATİ", "text": "1 ile 10 arasında bir sayı tut. Gözlerimin en derinine bak ve o sayıyı bana zihninle göndermeye çalış."},
        {"type": "ZAMAN MAKİNESİ", "text": "Şu an 2050 yılındayız, yaşlandık, torunlar var... Bana o günkü ses tonunla seslen ve benden bir su iste."},

        # SAYFA 8: FİNAL
        {"type": "İÇİNDEN OKU", "text": "Kartta ne yazdığını söyleme. Sadece gülümse ve 'Bunun cevabını düğün gecesi vereceğim' de."},
        {"type": "YALAN MAKİNESİ", "text": "Bana kendinle veya ilişkimizle ilgili 2 doğru 1 yanlış detay söyle. Hangisinin yalan olduğunu gözlerinden anlamaya çalışacağım."},
        {"type": "DJ KEREM", "text": "Bu kartı çeken, o anki modumuza en uygun şarkıyı açmak zorunda. (Romantikse hareketli, durgunsak neşeli)."},
        {"type": "SESSİZ ÇIĞLIK", "text": "Aksaray'da kediden korkup attığın o çığlığı düşün... Şimdi içinden haykırmak istediğin mutluluğu fısıldayarak kulağıma söyle."},
        {"type": "FOTOĞRAFÇI", "text": "Oyun dursun. Telefonu al ve tam şu anımızın, 14 Şubat'ın en doğal halinin bir fotoğrafını çek."},
        {"type": "İÇİNDEN OKU", "text": "Bu kartı okuma. Sadece elimi nezaketle öp ve alnına koy. Sonra hiçbir şey olmamış gibi oyuna devam et."},
        {"type": "BÜYÜK İTİRAF", "text": "'Bunu daha önce hiç söylemedim ama...' diye başlayan komik, ciddi veya şaşırtıcı bir itirafta bulun."},
        {"type": "FİNAL KARTI (YEMİN)", "text": "Sağ elini kalbime koy. Bu 14 Şubat gecesi ve yıldızlar şahit olsun ki; [Bu cümleyi içinden geldiği gibi tamamla ve 25 Nisan için bana söz ver]."}
    ]
    random.shuffle(st.session_state.deck)

# --- OYUN MANTIĞI VE GÖRSELLEŞTİRME ---
remaining = len(st.session_state.deck)

if remaining == 0:
    st.balloons()
    st.success("Tüm kartlar bitti! İyi ki varsın Büşra. Sonsuza kadar... ❤️")
    if st.button("Oyunu Yeniden Başlat 🔄"):
        del st.session_state.deck
        st.experimental_rerun()
else:
    st.markdown(f"<p class='counter'>Kalan Kart: {remaining}/64 ⚜️</p>", unsafe_allow_html=True)

    # --- BUTON VE ANİMASYON EFEKTİ ---
    if st.button("✨ Bir Kart Çek ✨", use_container_width=True):
        with st.spinner("Kart seçiliyor..."):
            time.sleep(0.6) # Animasyon için kısa bir bekleme
        card = st.session_state.deck.pop()
        st.session_state.current_card = card
    
    # --- KARTI GÖSTERME ALANI ---
    if 'current_card' in st.session_state:
        card = st.session_state.current_card
        
        # FOTOĞRAF MANTIĞI
        # Kart tipine göre hangi fotoğrafın gösterileceğini belirle
        photo_to_show = "biz.jpg" # Varsayılan fotoğraf
        caption = None
        
        if "(BÜŞRA)" in card['type']:
            photo_to_show = "busra.jpg"
            caption = "Güzeller güzeli müstakbel eşime..."
        elif "(KEREM)" in card['type']:
            photo_to_show = "kerem.jpg"
            caption = "Yakışıklı hocama bir soru..."
        
        # Kartın HTML yapısı (Animasyon sınıfı 'card-container' içinde)
        html_structure = f"""
        <div class="card-container">
            <div class="card-title">{card['type']}</div>
            <div class="card-content">{card['text']}</div>
        </div>
        """
        
        # Önce Fotoğrafı, Sonra Kart Metnini Göster
        # Not: HTML içine doğrudan resim gömmek yerine Streamlit'in image fonksiyonunu
        # kullanıyoruz ki mobil uyumu daha iyi olsun.
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">{card["type"]}</div>', unsafe_allow_html=True)
            
            # Fotoğrafı göster (Hata kontrolü ile)
            show_image(photo_to_show, caption)
            
            st.markdown(f'<div class="card-content">{card["text"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Uyarılar
        if "İÇİNDEN OKU" in card['type']:
            st.toast("🤫 Şşş! Bu kartı sesli okuma!", icon="🤫")

# --- FOOTER ---
st.markdown("<div class='footer-text'>For My Better Half, Büşra | Road to 25 April ❤️</div>", unsafe_allow_html=True)

import streamlit as st
import random
import time
import base64
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Road to 25 April | Elite Edition",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS: 3D KART, STICKER VE ANİMASYONLAR ---
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

    /* --- YENİ 3D KART TASARIMI --- */
    .card-wrapper {
        position: relative;
        width: 100%;
        max-width: 400px; /* Kart genişliği ideal boyutta */
        margin: 40px auto;
        perspective: 1000px; /* 3D derinlik için */
    }

    .white-card-box {
        background: #ffffff;
        padding: 30px 20px 50px 20px;
        border-radius: 20px;
        /* Gerçekçi Gölge */
        box-shadow: 
            0 15px 35px rgba(190, 18, 60, 0.15),
            0 5px 15px rgba(0,0,0,0.05);
        text-align: center;
        border: 2px solid #d4af37; /* Altın Çerçeve */
        position: relative;
        z-index: 10;
        transform-style: preserve-3d;
        transition: transform 0.6s;
        animation: floatUp 0.8s ease-out;
    }
    @keyframes floatUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* Kağıt Dokusu */
    .white-card-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: #fffbf0; /* Hafif krem rengi */
        opacity: 0.6;
        border-radius: 18px;
        z-index: -1;
    }

    /* MİNİK FOTOĞRAF (Madalyon) */
    .mini-photo-frame {
        width: 100px;
        height: 100px;
        margin: -50px auto 20px auto; /* Kartın tepesinden taşsın diye -50px */
        border-radius: 50%;
        border: 4px solid #d4af37;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        overflow: hidden;
        background-color

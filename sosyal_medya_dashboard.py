import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
st.title("Sosyal Medya Kullanım Dashboard'u")
st.write("Bu dashboard, sosyal medya kullanıcılarının hangi platformları kullandıkları, hangi günlerde kullandıkları ve kullanım esnasındaki ruh halleri üzerinden grafikler yardımıyla analiz yapmayı amaçlamaktadır. ")

df = pd.read_csv(r"C:\Users\aaa\Desktop\streamlit\Dashboard_Sosyal_Medya.csv", encoding="utf-8-sig")
st.subheader("Veri Setinin İlk 5 Satırı")
st.dataframe(df.head())
st.sidebar.header("Filtreler")
platformlar = sorted(df["Platform"].dropna().unique())
secili_platform = st.sidebar.multiselect( "Platform Seçiniz:", platformlar )
gunler = sorted(df["Gun"].dropna().unique())
secili_gunler = st.sidebar.multiselect( "Gün Seçiniz:", gunler)
ruh_hali = sorted(df["Ruh_Hali"].dropna().unique())
secili_ruh_hali =st.sidebar.multiselect("Ruh Hali Seçiniz:", ruh_hali)
#----------------------------------------------------------------------
df_filtreli = df.copy()
if secili_platform:
    df_filtreli = df_filtreli[df_filtreli["Platform"].isin(secili_platform)]
if len(secili_gunler) > 0:
    df_filtreli = df_filtreli[df_filtreli["Gun"].isin(secili_gunler)]
if secili_ruh_hali:
    df_filtreli = df_filtreli[df_filtreli["Ruh_Hali"].isin(secili_ruh_hali)]
st.subheader("Filtrelenmiş Veri")
st.write(f"Toplam Kayıt Sayısı: **{df_filtreli.shape[0]}**")
st.dataframe(df_filtreli)
#---------------------------------------------------------------------
#BAR GRAFİĞİ
st.subheader("Bar Grafiği")
st.write("Platformlar ve Ortalama Kullanım Süresi (dk)")
df_gruplar = df_filtreli.groupby("Platform")["Kullanim_Suresi_Dk"].mean()
fig, ax = plt.subplots()
ax.bar(df_gruplar.index, df_gruplar.values, color="teal", edgecolor= "black")
ax.grid(axis="both", linestyle="--", alpha=1)
ax.set_axisbelow(True)
ax.set_xlabel("Platform")
ax.set_ylabel("Ortalama Kullanım Süresi (dk)")
st.pyplot(fig)
# BAR GRAFİĞİ YORUM KUTUSU EKLEME
st.subheader("Bar Grafik Yorumu")
yorum_bar = st.text_area(
    label = "Yazılacak Yorum:",
    placeholder="Yorum Kısmı...",
    height=200,
    key="yorum_1"
)
if st.button("Yorumu Gönder", key="buton_1"):
    if yorum_bar.strip() == "":
        st.warning("Yorum alanı boş bırakılamaz. Lütfen bir şeyler yazınız.")
    else:
        st.success("Yorumunuz başarıyla kaydedildi.")
        st.write("Yazılan Yorum:")
        st.info(yorum_bar)
#DAĞILIM GRAFİĞİ
st.subheader("Dağılım Grafiği")
st.write("Günler ve Kullanıcıların Paylaşım Sayısı")
fig1, ax1 = plt.subplots()
ax1.scatter(df_filtreli["Gun"], df_filtreli["Paylasim_Sayisi"], color = 
"darkblue", alpha= 0.9, s=50)
ax1.set_axisbelow(True)
ax1.set_xlabel("Günler")
ax1.set_ylabel("Kullanıcıların Paylaşım Sayısı")
ax1.set_title("Gün Bazlı Kullanıcıların Paylaşım Sayısı")
ax1.grid(True)
st.pyplot(fig1)
# DAĞILIM GRAFİĞİ YORUM KUTUSU EKLEME
st.subheader("Dağılım Grafik Yorumu")
yorum_dagilim = st.text_area(
    label = "Yazılacak Yorum:",
    placeholder="Yorum Kısmı...",
    height=200,
    key="yorum_2"
)
if st.button("Yorumu Gönder", key="buton_2"):
    if yorum_dagilim.strip() == "":
        st.warning("Yorum alanı boş bırakılamaz. Lütfen bir şeyler yazınız.")
    else:
        st.success("Yorumunuz başarıyla kaydedildi.")
        st.write("Yazılan Yorum:")
st.info(yorum_dagilim)
#-----------------------------------------------------------------
st.subheader("Özet Göstergeler")
if df_filtreli.empty:
    st.warning("Bu filtrelerle hiç gönderi bulunamadı. Lütfen filtreleri değiştirip tekrar deneyiniz.")
else:
    ort_kullanim_suresi = df_filtreli["Kullanim_Suresi_Dk"].mean()
ort_paylasim_sayisi = df_filtreli["Paylasim_Sayisi"].mean()
toplam_kayit =df_filtreli.shape[0]
col1, col2, col3 =st.columns(3)
col1.metric("Ortalama Sosyal Medya Kullanım Süresi (dk)", 
f"{ort_kullanim_suresi:.0f}")
col2.metric("Ortalama Paylaşım Sayısı", f"{ort_paylasim_sayisi:.0f}")
col3.metric("Toplam Kayıt Sayısı", toplam_kayit)

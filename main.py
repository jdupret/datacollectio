import base64

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
from appart_a_louer import scrap_appart_a_louer
from appart_meuble import scrap_appart_meuble
from terrain_a_vendre import srappe_terrain_a_vendre


# Fonction Background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
            <style>
            .stApp {{
                background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
                background-size: cover
            }}
            </style>
        """,
        unsafe_allow_html=True
    )


add_bg_from_local('background.jpg')

# Page Principale
st.title("Projet de Data Collection Groupe 5")
st.write(
    "This app performs webscraping of data from expat-dakar over multiples pages. "
    "And we can also download scraped data from the app directly without scraping them."
)
st.markdown("- Python libraries: base64, pandas, streamlit, requests, bs4")
st.markdown("- Data source: at-Dakar.")

# Barre de Menu lattérale
st.sidebar.title("Menu")

# création d'une liste de 1 à 100
list1 = [i for i in range(1, 201)]

option1 = st.sidebar.selectbox(
    "Pages indexes",
    list1,
)

option2 = st.sidebar.selectbox(
    "Options", (
        "Scrape data using beautifulSoup",
        "Download scraped data",
        "Dashbord of the data",
        "Fill the form"
    )
)


def load(dataframe, title, key, key1):
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title, key1):
        # st.header(title)

        st.subheader('Display data dimension')
        st.write('Data dimension: ' +
                 str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

        csv = dataframe.to_csv().encode('utf-8')

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key=key)


appart_a_louer = pd.DataFrame()
appart_meuble = pd.DataFrame()
terrain_a_vendre = pd.DataFrame()

if option2 == "Scrape data using beautifulSoup":
    # scrapper les données avec beautifulSoup
    appart_a_louer = scrap_appart_a_louer(option1)
    appart_meuble = scrap_appart_meuble(option1)
    terrain_a_vendre = srappe_terrain_a_vendre(option1)

    # afficher les boutons
    load(appart_a_louer, "Appartements à louer", 1, 101)
    load(appart_meuble, "Appartement meublés", 2, 102)
    load(terrain_a_vendre, "Terrains à vendre", 3, 103)

# charger les data déjà scrappés
if option2 == "Download scraped data":
    web_appart_a_louer = pd.read_csv("expat_dakar_appart_alouer.csv")
    web_appart_meuble = pd.read_csv("expat_dakar_appart_meuble.csv")
    web_terrain_a_vendre = pd.read_csv("expat_dakar_terrain_a_vendre.csv")

    # afficher les boutons
    load(web_appart_a_louer, "Appartements à louer", 4, 104)
    load(web_appart_meuble, "Appartement meublés", 5, 105)
    load(web_terrain_a_vendre, "Terrains à vendre", 6, 106)

# Insertion du formulaire
if option2 == "Fill the form":
    st.markdown('<iframe src="https://ee.kobotoolbox.org/i/nQd4n5J5" style="width:100%; height:100vh;"></iframe>',
                unsafe_allow_html=True)

# Dashbaord
if option2 == "Dashbord of the data":
    appart_a_louer = scrap_appart_a_louer(option1)
    appart_meuble = scrap_appart_meuble(option1)
    terrain_a_vendre = srappe_terrain_a_vendre(option1)
    appart_a_louer['prix'] = appart_a_louer['prix'].astype('float')
    appart_plus_chers = appart_a_louer.sort_values(by='prix', ascending=False)
    appart_plus_chers = appart_plus_chers[:5]
    
    fig, ax = plt.subplots()
    ax.bar(appart_plus_chers['adresse'], appart_plus_chers['prix'])
    plt.xlabel('Article')
    plt.ylabel('Prix')
    plt.xticks(rotation=45)
    plt.title('Population des villes')
    plt.tight_layout()

    st.pyplot(fig)
    # st.bar_chart(appart_plus_chers, )
    # st.bar_chart(appart_plus_chers, x="detail", y="prix")

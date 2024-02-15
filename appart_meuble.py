# importation de packages
import time

import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs


# caching des données
@st.cache_data
def scrap_appart_meuble(nbr_pages=10):
    df= pd.DataFrame()
    for p in range(1,98):
        url = f'https://www.expat-dakar.com/appartements-meubles?page={p}'
        resp = get(url)
        soup = bs(resp.text, 'html.parser')
        links_a = soup.find_all('a', class_ ='listing-card__inner')
        links = [link['href'] for link in links_a]
        data = [ ]
        for link in links:
            res= get(link)
            Soup = bs(res.text ,'html.parser')
            try :
                adresse = Soup.find('span', class_ = 'listing-item__address-location').text.strip()
                prix = Soup.find('span', class_ ='listing-card__price__value 1').text.strip().replace('\u202f', '').replace(' F Cfa', '')
                detail = Soup.find('div', class_ ='listing-item__description').text
                lien_image = soup.find("img", class_="listing-card__image__resource").get("src")
                try:
                    inf = Soup.find_all('dd', class_ = 'listing-item__properties__description')
                    nombre_chambre = inf[0].text.strip()
                except:
                    nombre_chambre  =''
                try:
                    superficie = inf[2].text.strip().replace(' m²', '')
                except:
                    superficie = ''

                obj = {
                    'detail': detail,
                    'nombre_chambre': nombre_chambre,
                    'superficie': superficie,
                    'adresse': adresse,
                    'prix': prix,
                    'lien_image': lien_image
                }
                data.append(obj)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis =0).reset_index(drop = True)    
    return df
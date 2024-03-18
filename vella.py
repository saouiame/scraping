from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tqdm import tqdm
import re
import random

def trouver_nombres(texte):
    # Utilisation d'une expression régulière pour trouver les nombres dans le texte
    nombres = re.findall(r'\d+', texte)
    # renvoyer les nombres trouvés
    return [int(nombre) for nombre in nombres]

def get_titles_urls(driver):
    article_urls = []

    try:
        # Récupérer la page web pour la catégorie donnée
        driver.get("https://www.marrakechbestof.com/categorie-bon-plan/hebergements/")
        # Attendre que les éléments se chargent
        articles = WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.list.listing a")))
        
        for art in articles:
            try:
                url = art.get_attribute("href")
                article_urls.append(url)
            except Exception as e:
                print(f"Une erreur s'est produite lors de la récupération de l'URL de l'article : {e}")
        

    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération des URLs des articles de la catégorie : {e}")

    return article_urls

def get_article_info(url, driver):
    try:
        # Récupérer la page web pour l'article spécifique
        driver.get(url)
        # Attendre que les éléments se chargent
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > main")))
        # Récupérer les éléments nécessaires
        article = driver.find_element(By.CSS_SELECTOR, "body > main")
       
        title = ""
        nombre_chambre= ""
        nombre_Equipements_enfants  = ""
        nombr_Equipements_spéciaux = ""
        prix_par_nuit = ""
        Temps_jusqu_au_centreville_minute = ""
        
        # Essayer de trouver chaque élément et assigner les valeurs
        try:
            title = article.find_element(By.CSS_SELECTOR, "section.bloc.slider.project-slider > article > section > div > h1 ").text.strip()
        except Exception as e:
            print(f"Erreur lors de la récupération du titre : {e}")
        try:
            nombre_chambre = len(article.find_elements(By.CSS_SELECTOR , "#details > p:nth-child(7) > br")) + 2
        except Exception as e:
            print(f"Erreur lors de la récupération du nombre de chambres : {e}")
            
        try:
            nombre_Equipements_enfants  = len (article.find_elements(By.CSS_SELECTOR, "#details > p:nth-child(10) > br")) + 1
            
        except Exception as e:
            print(f"Erreur lors de la récupération de la nombre_Equipements_enfants : {e}")
            
        try:
           nombr_Equipements_spéciaux  = len (article.find_elements(By.CSS_SELECTOR, "#details > p:nth-child(16) > br")) + 1
            
        except Exception as e:
            print(f"Erreur lors de la récupération de la nombr_Equipements_spéciaux: {e}")
            
        try:
            
            prix_par_nuit = random.randint(100, 250)
            '''
            # Cliquer sur l'élément avec la classe "activate"
            activate_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.activate")))
            activate_element.click()
            
            # Attendre que l'élément contenant le prix par nuit soit présent dans le DOM
            prix_par_nuit_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.activate > div > p:nth-child(1) > strong")))
            prix_par_nuit = trouver_nombres(prix_par_nuit_element.text.strip())[0]
            '''
        except Exception as e:
            print(f"Erreur lors de la récupération de la prix_par_nuit: {e}")
            
        try:
            Temps_jusqu_au_centreville_minute  = random.randint(15, 50)
            
        except Exception as e:
            print(f"Erreur lors de la récupération de la Temps_jusqu_au_centreville_minute: {e}")      
        
        article_info = {
            "titre": title,
            "nombre_chambre": nombre_chambre,
            "nombre_Equipements_enfants": nombre_Equipements_enfants,
            "nombr_Equipements_spéciaux": nombr_Equipements_spéciaux,
            "prix_par_nuit": prix_par_nuit,
            "Temps_jusqu_au_centreville_minute": Temps_jusqu_au_centreville_minute,
        }
        
        return article_info
    
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération des informations de l'article '{url}' : {e}")
        return None

def main():
    # Spécifiez le chemin absolu vers geckodriver
    geckodriver_path = "/usr/bin/geckodriver"
    
    # Configuration du pilote Firefox avec le chemin spécifié
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path=geckodriver_path, options=options)
    try:
        article_urls = get_titles_urls(driver)
        vella_list = []
        for url in tqdm(article_urls, desc="Progression dans les infos des vales"):
            article_info = get_article_info(url, driver)
            if article_info is not None:
                vella_list.append(article_info)
        
        # Créer un DataFrame à partir de la liste des infos
        df = pd.DataFrame(vella_list)
        
        # Nom du fichier Excel
        nom_fichier = "infos_vales.xlsx"
        
        # Tentative de sauvegarde dans un fichier Excel avec gestion d'erreurs
        try:
            df.to_excel(nom_fichier, index=False)
            print(f"Les informations ont été enregistrées dans '{nom_fichier}' avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des informations dans '{nom_fichier}': {e}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        driver.quit()

if _name_ == "_main_":
    main()

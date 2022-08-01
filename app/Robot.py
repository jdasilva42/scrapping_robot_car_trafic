from importlib.resources import path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import os
import time
import pandas as pd
import glob
import sqlite3




class Robot:
    """classe Robot
    
    """

    
    def __init__(self,PATH,url):        
        
        self.PATH = PATH
        self.url  = url
        self._Robot_init()
        self._Robot_start()
        self._Robot_processing()
        self._Robot_form_SQL()
        self._Robot_POST_SQL()
        self._Robot_clean()



    def _Robot_init(self):
        """Initialisation du Robot

        Args:
            PATH (_str_): _Répertoire vers le fichier téléchargé csv_
        """
        
        option = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : self.PATH,'excludeSwitches':'enable-logging'}
        option.add_experimental_option("prefs",prefs)
        option.add_argument('headless')
        self.option = option
    
    def _Robot_start(self):
        """Activation du Robot. Téléchargement du fichier csv and fermeture du robot.

        Args:
            url (_str_): _url du site_
        """
        time.sleep(5)
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["acceptInsecureCerts"] = True
        driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities=capabilities,options=self.option)
        driver.get(self.url)        
        driver.find_element(By.CLASS_NAME,"ods-dataset-export-link__link").click()
        time.sleep(5)
        driver.close()



    def _Robot_processing(self):
        """Récupère le fichier csv. Produit les données necessaires.
        Sauvegarde au format pkl. Si un pkl existe déja un nouveau pkl(1) est crée.

        Args:
            PATH (_str_): _PATH vers le cache directory_
        """
        filePATH = glob.glob(os.path.join(self.PATH, "*.csv"))
        df = pd.read_csv(filePATH[0],delimiter=';')

        df['date'] = df['Horodatage'].astype(str).str[:10]
        df['time'] = df['Horodatage'].astype(str).str[11:19]
        df['datetime'] = pd.to_datetime(df[['date', 'time']].agg('-'.join, axis=1), format='%Y-%m-%d-%H:%M:%S')
        
        df[['Y','X']] = df['geo_point_2d'].str.split(',',expand=True)
        
        drop_list=['Horodatage','date','time','geo_point_2d']
        df = df.drop(drop_list,axis=1)

        if glob.glob(self.PATH + "/*.pkl"):
            df.to_pickle(os.path.join(self.PATH,"Cache_data(1).pkl"))
        else:
            df.to_pickle(os.path.join(self.PATH,"Cache_data.pkl"))

    def _Robot_form_SQL(self):
        """Création de la dataframe pour intégration à la base de données SQL.
        Si plusieurs fichiers pkl existent, ils sont concat et les dupplicants supprimés.

        Args:
            PATH (_str_): _PATH vers le cache directory_
        """
        files = glob.glob(os.path.join(self.PATH, '*.pkl'))

        if len(files)>1:
            df_all = pd.DataFrame()
            for file in files:
                df = pd.read_pickle(file)
                df_all = pd.concat([df_all,df])
            df_all=df_all.drop_duplicates()

            self.data = df_all

        else :

            df_all = pd.read_pickle(files[0])
            

            self.data = df_all

    def _Robot_POST_SQL(self):
        """Intégration des données dataframe vers la base de données SQL.

        Args:
            PATH(_str_): _PATH vers le fichier .db_
        """

        self.data=self.data.drop_duplicates()
        os.makedirs(self.PATH, exist_ok=True)

        con = sqlite3.connect(os.path.join(self.PATH,'database.db'))
        self.data.to_sql('Nantes_Trafic_routier', con=con,if_exists='append')
        con.close()

    def _Robot_clean(self):
        """Vidage des fichiers contenus dans le Cache Dir.

        Args:
            PATH (_str_): _PATH vers le fichier cache Dir_
        """
        filePATHcsv = glob.glob(os.path.join(self.PATH, "*.csv"))
        if filePATHcsv:
            os.remove(filePATHcsv[0])
        
        filePATHpkl = glob.glob(os.path.join(self.PATH, "*.pkl"))
        if filePATHpkl:
            for file in filePATHpkl:
                os.remove(file)






        
        




        












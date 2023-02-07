import requests
import os
from bs4 import BeautifulSoup
import configparser
from mail import alert


class MootseRunner():
    """ Scrapping de Mootse (le moodle de Télécom Saint-Étienne) """
    def __init__(self, path) -> None:
        # Initialisation ConfigParser
        config = configparser.ConfigParser()
        config.read(path+"config.ini")

        # Initialisation de la session
        session = requests.Session()
        login_response = session.post("***REMOVED***/login/index.php")

        # Extraction du token
        soup = BeautifulSoup(login_response.text, "html.parser")
        token = soup.select_one("input[name=logintoken]")["value"]

        # Connexion
        login_data = {
            "username": config["login Mootse"]["username"],
            "password": config["login Mootse"]["password"],
            "logintoken": token
        }
        session.post("***REMOVED***/login/index.php", data=login_data)

        with open('url.txt', 'r', encoding="utf-8") as f1:
            for line in f1:
                parts = line.strip().split(" : ")
                temp = session.get(parts[0])
                temp = BeautifulSoup(temp.text, "html.parser")
                temp = temp.tbody
                with open("pages/" + parts[1], "r", encoding="utf-8") as f2:
                    contents = f2.read()
                    if contents != str(temp):
                        with open("pages/" + parts[1], "w", encoding="utf-8") as f2:
                            f2.write(str(temp))
                            alert(parts[1], path)


class MootseInit():
    """ Initialisation de Mootse (le moodle de Télécom Saint-Étienne) """
    def __init__(self, path) -> None:
        # Initialisation ConfigParser
        config = configparser.ConfigParser()
        config.read(path+"config.ini")

        # Initialisation de la session
        session = requests.Session()
        login_response = session.post("***REMOVED***/login/index.php")

        # Extraction du token
        soup = BeautifulSoup(login_response.text, "html.parser")
        token = soup.select_one("input[name=logintoken]")["value"]

        # Connexion
        login_data = {
            "username": config["login Mootse"]["username"],
            "password": config["login Mootse"]["password"],
            "logintoken": token
        }
        session.post("***REMOVED***/login/index.php", data=login_data)

        # Scrapping des url des notes
        notes_url = "***REMOVED***/grade/report/overview/index.php"
        notes_response = session.get(notes_url)
        notes_soup = BeautifulSoup(notes_response.text, "html.parser")

        # Nettoyage du scrapping
        tbody = notes_soup.tbody
        links = tbody.find_all("a")
        contents = [link["href"] + " : " + link.text for link in links]

        with open(path+"url.txt", "w", encoding="utf-8") as f:
            for content in contents:
                f.write(content + "\n")

        if not os.path.exists(path+"pages"):
            os.makedirs(path+"pages")

        with open(path+'url.txt', 'r', encoding="utf-8") as f1:
            for line in f1:
                parts = line.strip().split(" : ")
                temp = session.get(parts[0])
                temp = BeautifulSoup(temp.text, "html.parser")
                temp = temp.tbody
                with open(path+"pages/" + parts[1], "w", encoding="utf-8") as f2:
                    f2.write(str(temp))

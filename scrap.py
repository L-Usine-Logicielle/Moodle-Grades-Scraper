import requests
from bs4 import BeautifulSoup
import configparser


class Mootse():
    """ Scrapping de Mootse (le moodle de Télécom Saint-Étienne) """
    def __init__(self) -> None:
        # Initialisation ConfigParser
        config = configparser.ConfigParser()
        config.read("config.ini")
        login_url = config["login settings"]["login_url"]
        # Initialisation de la session
        session = requests.Session()
        login_response = session.post(login_url)

        # Extraction du token
        soup = BeautifulSoup(login_response.text, "html.parser")
        token = soup.select_one("input[name=logintoken]")["value"]

        # Connexion
        login_data = {
            "username": config["login settings"]["username"],
            "password": config["login settings"]["password"],
            "logintoken": token
        }
        session.post(login_url, data=login_data)

        # Scrapping des notes
        notes_url = "***REMOVED***/grade/report/overview/index.php"
        notes_response = session.get(notes_url)
        notes_soup = BeautifulSoup(notes_response.text, "html.parser")

        # Nettoyage du scrapping
        tbody = notes_soup.tbody
        links = tbody.find_all("a")
        contents = [link["href"] + " : " + link.text for link in links]
        with open("url.txt", "w", encoding="utf-8") as f:
            for content in contents:
                f.write(content + "\n")

        # Passage sur chaque matière
        with open("url.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" : ")
                url = parts[0]
                tag = parts[1]
                response = session.get(url)
                test = BeautifulSoup(response.text, "html.parser")

                """ douteux """
                tbody = test.tbody
                links = tbody.find_all("td")
                chaine = [str(l) for l in links]

                with open("temp.txt", "r", encoding="utf-8")as f2:
                    for line in f2:
                        if f2 != ('\n' + tag + chaine):
                            self.alert(tag)

                with open("temp.txt", "w", encoding="utf-8") as f3:
                    f3.write('\n' + tag)
                    for c in chaine:
                        f3.write(c)

        def alert(self, tag):
            print(f"nouvelle note dans : {tag}")

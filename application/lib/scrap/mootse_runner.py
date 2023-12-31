from traceback import format_exc

from bs4 import BeautifulSoup

from config.config import (DISCORD_WEBHOOK_URL, MAIL_PASSWORD, MAIL_PORT,
                           MAIL_RECIPIENTS, MAIL_SERVER, MAIL_USERNAME, MOOTSE_MASTER_URL)
from lib.database import DatabaseConnector
from lib.discord import DiscordNotifier
from lib.mail import MailNotifier
from lib.scrap.mootse_utils import MootseUtils
from lib.metrics import MetricsExpoter

class MootseRunner(MootseUtils):
    """ Scrapping de Mootse (le moodle de Télécom Saint-Étienne) """

    def __init__(self) -> None:
        super().__init__()
        self.db = DatabaseConnector()
        self.exporter = MetricsExpoter(MOOTSE_MASTER_URL)

    def __alert(self, subject: str) -> None:
        if MAIL_RECIPIENTS:
            recipients = MAIL_RECIPIENTS.split(";")
            try:
                mail = MailNotifier(
                    MAIL_USERNAME,
                    MAIL_PASSWORD,
                    MAIL_SERVER,
                    MAIL_PORT
                )
                mail.alert(subject, recipients)
            except:
                self.logger.critical(
                    "Impossible d'envoyer les alertes mails.", exc_info=format_exc())

        if DISCORD_WEBHOOK_URL:
            try:
                discord = DiscordNotifier(DISCORD_WEBHOOK_URL)
                discord.alert(subject)
                try:
                    self.exporter.send_metric("discord-webhook-sent-count")
                except:
                    self.logger.debug("Impossible d'envoyer les métriques.", exc_info=format_exc())
            except:
                self.logger.critical(
                    "Impossible d'envoyer l'alerte Discord.", exc_info=format_exc())

    def __check_for_new_notes(self, session):

        topics = self.db.get_topics()
        for record in topics:
            url = record[2]
            temp = session.get(url)
            temp = BeautifulSoup(temp.text, "html.parser")
            temp = temp.tbody.text

            if record[1] != temp:
                self.logger.info(
                    f"Nouvelle note détectée en : {record[0]}.")
                self.db.update_topic(url, temp)
                try:
                    self.exporter.send_metric(record[0])
                except:
                    self.logger.debug("Impossible d'envoyer les métriques.", exc_info=format_exc())
                self.__alert(record[0])

    def run_check(self):
        try:
            session = self.create_mootse_session()
            self.login_to_mootse(session)
        except:
            self.logger.critical(
                "Erreur lors de la connexion à Mootse.", exc_info=format_exc())
            exit(-1)

        try:
            self.__check_for_new_notes(session)
        except:
            self.logger.critical(
                "Impossible de récupérer les nouvelles notes.", exc_info=format_exc())
            exit(-1)

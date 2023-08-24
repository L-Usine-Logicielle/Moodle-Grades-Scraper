from logging import getLogger, INFO, Formatter, StreamHandler
import requests
import socket


class MetricsExpoter():
    def __init__(self, url: str) -> None:
        self.url = url
        self.logger = getLogger(__name__)
        self.logger.setLevel(INFO)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def send_metric(self, metric: str, value: int = 1) -> None:
        if self.url:
            response =requests.put(f"{self.url}/metrics/{socket.gethostname()}-{metric}?increment={value}")
            try:
                response.raise_for_status()
                self.logger.debug(f"Métrique '{socket.gethostname()}-{metric}' envoyée à Moodle Master.")
            except requests.exceptions.HTTPError as err:
                raise Exception(f"Une erreur s'est produite : {err}") from err
from logging import INFO, Formatter, StreamHandler, getLogger
from socket import gethostname
from traceback import format_exc

from requests import put


class MetricsExpoter():
    def __init__(self, url: str) -> None:
        self.url = url
        self.logger = getLogger(__name__)
        self.logger.setLevel(INFO)
        formatter = Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def send_metric(self, metric: str, value: int = 1) -> None:
        if self.url:
            response = put(
                f"{self.url}/metrics/{gethostname()}--{metric}?increment={value}", timeout=15)
            try:
                response.raise_for_status()
                self.logger.debug(
                    f"Métrique '{gethostname()}--{metric}' envoyée à Moodle Master.")
            except:
                self.logger.critical(
                    "Une erreur s'est produite lors de l'envoi de l'envoi de la métrique", exc_info=format_exc())

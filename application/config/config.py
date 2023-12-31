from config.loader import load_variables

SCAN_INTERVAL = int(load_variables("SCAN_INTERVAL"))
PROMO = load_variables("PROMO")
MOOTSE_URL = load_variables("MOOTSE_URL")
MOOTSE_USERNAME = load_variables("MOOTSE_USERNAME")
MOOTSE_PASSWORD = load_variables("MOOTSE_PASSWORD")
MAIL_USERNAME = load_variables("MAIL_USERNAME")
MAIL_PASSWORD = load_variables("MAIL_PASSWORD")
MAIL_SERVER = load_variables("MAIL_SERVER")
MAIL_PORT = load_variables("MAIL_PORT")
MAIL_RECIPIENTS = load_variables("MAIL_RECIPIENTS")
DISCORD_WEBHOOK_URL = load_variables("DISCORD_WEBHOOK_URL")
DB_HOST = load_variables("DB_HOST")
DB_USER = load_variables("DB_USER")
DB_PASSWORD = load_variables("DB_PASSWORD")
DB_PORT = load_variables("DB_PORT")
MOOTSE_MASTER_URL = load_variables("MOOTSE_MASTER_URL")

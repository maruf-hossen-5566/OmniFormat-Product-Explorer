import os
from dotenv import load_dotenv

load_dotenv()


def get_proxy():
    user = os.getenv("DATAIMPULSE_USER")
    pwd = os.getenv("DATAIMPULSE_PASS")
    host = os.getenv("DATAIMPULSE_HOST")
    port = os.getenv("DATAIMPULSE_PORT")

    if not all([user, pwd, host, port]):
        raise ValueError("! Missing proxy environment variables.")

    return f"http://{user}:{pwd}@{host}:{port}"

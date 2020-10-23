import requests
import sys
import logging

logger = logging.getLogger(__name__)

HEALTH_URL = "http://127.0.0.1:8080/health"

try:
    response = requests.get(HEALTH_URL).json()
except:
    logger.error(f"Encountered an Error when making the request to the localhost")
    sys.exit(1)

if response["metadatabase"]["status"] == response["scheduler"]["status"] == "healthy":
    sys.exit(0)
else:
    logger.error(
        f"Airflow Health Status: metadatabase='{response['metadatabase']['status']}', scheduler='{response['scheduler']['status']}'"
    )
    sys.exit(1)

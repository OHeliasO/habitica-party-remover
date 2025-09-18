import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_USER_ID = os.getenv("HABITICA_USER_ID")
API_TOKEN = os.getenv("HABITICA_API_TOKEN")
API_GROUP_ID = os.getenv("HABITICA_GROUP_ID")
API_CLIENT= os.getenv("HABITICA_CLIENT")



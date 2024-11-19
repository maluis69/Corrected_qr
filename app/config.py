# Load environment variables
import os
from pathlib import Path
from dotenv import load_dotenv

# The dotenv package loads environment variables from a .env file into the environment.
# This is useful for keeping secrets and configurations out of source code.
load_dotenv()

# Environment Variables for Configuration

# QR_DIRECTORY specifies the directory where QR codes are saved.
# If not specified in the environment, it defaults to './qr_codes'.
QR_DIRECTORY = Path(os.getenv('QR_CODE_DIR', './qr_codes'))

# Ensure the QR directory exists
if not QR_DIRECTORY.exists():
    QR_DIRECTORY.mkdir(parents=True, exist_ok=True)

# FILL_COLOR determines the color of the QR code itself. Defaults to 'red'.
FILL_COLOR = os.getenv('FILL_COLOR', 'red')

# BACK_COLOR sets the background color of the QR code. Defaults to 'white'.
BACK_COLOR = os.getenv('BACK_COLOR', 'white')

# SERVER_BASE_URL is the base URL for the server. This might be used for constructing
# URLs in responses. Defaults to 'http://localhost:80'.
SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:80')

# SERVER_DOWNLOAD_FOLDER specifies the directory exposed by the server for downloads,
# such as QR codes. This could be a path routed by your server for static files.
SERVER_DOWNLOAD_FOLDER = os.getenv('SERVER_DOWNLOAD_FOLDER', 'downloads')

# SECRET_KEY is used in cryptographic operations, such as signing JWT tokens.
# It should be a long, random string that is kept secret. If not provided, the application will raise an error.
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment. Please set a secure value in the .env file.")

# ALGORITHM specifies the algorithm used for JWT encoding/decoding. Defaults to "HS256".
# Ensure you use a secure algorithm that matches your cryptographic needs.
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# ACCESS_TOKEN_EXPIRE_MINUTES defines how long (in minutes) an access token remains valid.
# Defaults to 30 minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ADMIN_USER and ADMIN_PASSWORD are placeholder credentials for basic authentication.
# In production, use a secure authentication method and do not hardcode credentials.
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secret')

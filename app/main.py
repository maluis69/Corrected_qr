from fastapi import FastAPI
from app.config import QR_DIRECTORY
from app.routers import qr_code, oauth  # Ensure these modules have a 'router' object
from app.services.qr_service import create_directory
from app.utils.common import setup_logging

# Setup logging based on configuration
setup_logging()

# Ensure the QR code directory exists
create_directory(QR_DIRECTORY)

# Initialize the FastAPI application
app = FastAPI(
    title="QR Code Manager API",
    description=(
        "A FastAPI-based application for managing QR codes. "
        "This API allows you to create, list, and delete QR codes securely using OAuth authentication."
    ),
    version="1.0.0",
    redoc_url=None,  # Disable ReDoc if not needed
    contact={
        "name": "API Support",
        "url": "https://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Include routers for the application
app.include_router(qr_code.router)  # QR code management routes
app.include_router(oauth.router)   # OAuth authentication routes

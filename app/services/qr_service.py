import os
from typing import List
import qrcode
import logging
from pathlib import Path
from app.config import SERVER_BASE_URL, SERVER_DOWNLOAD_FOLDER

def list_qr_codes(directory_path: Path) -> List[str]:
    """
    Lists all QR code images in the specified directory by returning their filenames.
    Parameters:
    - directory_path (Path): The filesystem path to the directory containing QR code images.

    Returns:
    - A list of filenames (str) for QR codes found in the directory.
    """
    try:
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        return [f for f in os.listdir(directory_path) if f.endswith('.png')]
    except FileNotFoundError as e:
        logging.error(str(e))
        raise
    except Exception as e:
        logging.error(f"An error occurred while listing QR codes: {e}")
        raise

def generate_qr_code(data: str, path: Path, fill_color: str = 'red', back_color: str = 'white', size: int = 10):
    """
    Generates a QR code based on the provided data and saves it to a specified file path.
    Parameters:
    - data (str): The data to encode in the QR code.
    - path (Path): The filesystem path where the QR code image will be saved.
    - fill_color (str): Color of the QR code.
    - back_color (str): Background color of the QR code.
    - size (int): The size of each box in the QR code grid.
    """
    logging.debug("QR code generation started")
    try:
        qr = qrcode.QRCode(version=1, box_size=size, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(str(path))
        logging.info(f"QR code successfully saved to {path}")
    except Exception as e:
        logging.error(f"Failed to generate/save QR code: {e}")
        raise

def delete_qr_code(file_path: Path):
    """
    Deletes the specified QR code image file.
    Parameters:
    - file_path (Path): The filesystem path of the QR code image to delete.
    """
    try:
        if file_path.is_file():
            file_path.unlink()  # Delete the file
            logging.info(f"QR code {file_path.name} deleted successfully")
        else:
            logging.error(f"QR code {file_path.name} not found for deletion")
            raise FileNotFoundError(f"QR code {file_path.name} not found")
    except Exception as e:
        logging.error(f"Error occurred while deleting {file_path.name}: {e}")
        raise

def create_directory(directory_path: Path):
    """
    Ensures the existence of a directory at the specified path.
    If the directory already exists, no changes are made.
    Parameters:
    - directory_path (Path): The filesystem path of the directory to create.
    Raises:
    - PermissionError: If the process lacks the necessary permissions.
    - Exception: For other unexpected errors.
    """
    logging.debug('Attempting to create directory')
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory ensured: {directory_path}")
    except PermissionError as e:
        logging.error(f"Permission denied when trying to create directory {directory_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error creating directory {directory_path}: {e}")
        raise

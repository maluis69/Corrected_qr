from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.schema import QRCodeRequest, QRCodeResponse
from app.services.qr_service import generate_qr_code, list_qr_codes, delete_qr_code
from app.utils.common import decode_filename_to_url, encode_url_to_filename, generate_links
from app.config import QR_DIRECTORY, SERVER_BASE_URL, FILL_COLOR, BACK_COLOR, SERVER_DOWNLOAD_FOLDER
from pathlib import Path
import logging

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
QR_DIRECTORY = Path(QR_DIRECTORY)

@router.post("/qr-codes/", response_model=QRCodeResponse, status_code=status.HTTP_201_CREATED, tags=["QR Codes"])
async def create_qr_code(request: QRCodeRequest, token: str = Depends(oauth2_scheme)):
    logging.info(f"[CREATE] Request received to generate QR code for: {request.url}")
    encoded_url = encode_url_to_filename(request.url)
    qr_filename = f"{encoded_url}.png"
    qr_code_full_path = QR_DIRECTORY / qr_filename
    qr_code_download_url = f"{SERVER_BASE_URL}/{SERVER_DOWNLOAD_FOLDER}/{qr_filename}"
    links = generate_links("create", qr_filename, SERVER_BASE_URL, qr_code_download_url)

    if qr_code_full_path.exists():
        logging.info("[CREATE] QR code already exists.")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "QR code already exists.", "links": links}
        )

    generate_qr_code(request.url, qr_code_full_path, FILL_COLOR, BACK_COLOR, request.size)
    return QRCodeResponse(message="QR code created successfully.", qr_code_url=qr_code_download_url, links=links)

@router.get("/qr-codes/", response_model=List[QRCodeResponse], tags=["QR Codes"])
async def list_qr_codes_endpoint(token: str = Depends(oauth2_scheme)):
    logging.info("[LIST] Request received to list all QR codes.")
    try:
        qr_files = list_qr_codes(QR_DIRECTORY)
    except Exception as e:
        logging.error(f"[LIST] Failed to list QR codes: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve QR codes")

    responses = [
        QRCodeResponse(
            message="QR code available",
            qr_code_url=decode_filename_to_url(qr_file[:-4]),
            links=generate_links("list", qr_file, SERVER_BASE_URL, f"{SERVER_BASE_URL}/{SERVER_DOWNLOAD_FOLDER}/{qr_file}")
        )
        for qr_file in qr_files if qr_file.endswith(".png")
    ]
    return responses

@router.delete("/qr-codes/{qr_filename}", status_code=status.HTTP_200_OK, tags=["QR Codes"])
async def delete_qr_code_endpoint(qr_filename: str, token: str = Depends(oauth2_scheme)):
    logging.info(f"[DELETE] Request received to delete QR code: {qr_filename}")
    qr_code_path = QR_DIRECTORY / qr_filename
    if not qr_code_path.is_file():
        logging.warning(f"[DELETE] QR code not found: {qr_filename}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QR code not found")

    delete_qr_code(qr_code_path)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from core.logging_config import logger
from services.csv_service import gerar_csv


BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTOS_FILE = (
    BASE_DIR /
    "data" /
    "documentos.json"
)

EXPORTACOES_DIR = (
    BASE_DIR /
    "data" /
    "exportacoes"
)


router = APIRouter(
    prefix="/exportar",
    tags=["Exportação"]
)


@router.get("/csv")
def exportar_csv():

    caminho_csv = gerar_csv(
        DOCUMENTOS_FILE,
        EXPORTACOES_DIR,
    )

    logger.info(
        "Catálogo de documentos exportado para CSV."
    )

    return FileResponse(
        path=caminho_csv,
        media_type="text/csv",
        filename=caminho_csv.name,
    )
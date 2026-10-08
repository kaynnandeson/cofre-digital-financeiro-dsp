from pathlib import Path

from fastapi import APIRouter

from core.logging_config import logger
from services.json_repository import verificar_integridade_global


BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTOS_FILE = (
    BASE_DIR /
    "data" /
    "documentos.json"
)

ARQUIVOS_DIR = (
    BASE_DIR /
    "data" /
    "arquivos"
)


router = APIRouter(
    tags=["Integridade"]
)


@router.get("/integridade")
def obter_integridade_global():

    resultado = verificar_integridade_global(
        DOCUMENTOS_FILE,
        ARQUIVOS_DIR,
    )

    logger.info(
        "Verificação global de integridade realizada."
    )

    return resultado
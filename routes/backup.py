from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from core.logging_config import logger
from services.backup_service import criar_backup, listar_backups


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

BACKUPS_DIR = (
    BASE_DIR /
    "data" /
    "backups"
)


router = APIRouter(
    tags=["Backups"]
)


@router.post(
    "/backup",
    status_code=status.HTTP_201_CREATED,
)
def gerar_backup():

    try:
        resultado = criar_backup(
            DOCUMENTOS_FILE,
            ARQUIVOS_DIR,
            BACKUPS_DIR,
        )

        logger.info(
            f"Backup criado: {resultado['backup']}"
        )

        return resultado

    except Exception as erro:

        logger.error(
            f"Erro ao criar backup: {erro}"
        )

        raise HTTPException(
            status_code=500,
            detail="Erro ao criar backup.",
        )

@router.get("/backups")
def obter_backups():

    backups = listar_backups(
        BACKUPS_DIR
    )

    logger.info(
        "Listagem de backups realizada."
    )

    return backups
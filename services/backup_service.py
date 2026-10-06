import zipfile
from datetime import datetime
from pathlib import Path

from services.json_repository import ler_json


def criar_backup(
    arquivo_json: Path,
    diretorio_arquivos: Path,
    diretorio_backups: Path,
) -> dict:

    documentos = ler_json(arquivo_json)

    diretorio_backups.mkdir(
        parents=True,
        exist_ok=True,
    )

    data_hora = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    nome_backup = f"backup_{data_hora}.zip"

    caminho_backup = (
        diretorio_backups /
        nome_backup
    )

    arquivos_incluidos = 0
    arquivos_nao_localizados = []

    with zipfile.ZipFile(
        caminho_backup,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as backup:

        if arquivo_json.exists():
            backup.write(
                arquivo_json,
                arcname="metadata/documentos.json",
            )

        for documento in documentos:

            nome_armazenado = documento.get(
                "nome_armazenado"
            )

            if not nome_armazenado:
                continue

            caminho_arquivo = (
                diretorio_arquivos /
                nome_armazenado
            )

            if caminho_arquivo.exists():

                backup.write(
                    caminho_arquivo,
                    arcname=f"documentos/{nome_armazenado}",
                )

                arquivos_incluidos += 1

            else:
                arquivos_nao_localizados.append(
                    documento.get("id")
                )

    return {
        "backup": nome_backup,
        "arquivos_incluidos": arquivos_incluidos,
        "arquivos_nao_localizados": arquivos_nao_localizados,
        "tamanho": caminho_backup.stat().st_size,
    }

def listar_backups(diretorio_backups: Path) -> list[dict]:

    if not diretorio_backups.exists():
        return []

    backups = []

    for arquivo in diretorio_backups.glob("*.zip"):
        backups.append({
            "nome": arquivo.name,
            "tamanho": arquivo.stat().st_size,
        })

    return backups
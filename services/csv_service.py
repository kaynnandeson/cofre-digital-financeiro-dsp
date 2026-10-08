import csv
from datetime import datetime
from pathlib import Path

from services.json_repository import ler_json


CAMPOS_CSV = [
    "id",
    "nome_original",
    "nome_armazenado",
    "extensao",
    "tipo_mime",
    "tamanho",
    "categoria",
    "descricao",
    "data_upload",
    "sha256",

    # Campos financeiros
    "tipo",
    "competencia",
    "valor",
    "centro_de_custo",
    "responsavel",
]


def gerar_csv(
    arquivo_json: Path,
    diretorio_exportacoes: Path,
) -> Path:

    documentos = ler_json(arquivo_json)

    diretorio_exportacoes.mkdir(
        parents=True,
        exist_ok=True,
    )

    data_hora = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    nome_arquivo = (
        f"documentos_{data_hora}.csv"
    )

    caminho_csv = (
        diretorio_exportacoes /
        nome_arquivo
    )

    with open(
        caminho_csv,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=CAMPOS_CSV,
        )

        escritor.writeheader()

        for documento in documentos:
            linha = {
                campo: documento.get(campo, "")
                for campo in CAMPOS_CSV
            }

            escritor.writerow(linha)

    return caminho_csv
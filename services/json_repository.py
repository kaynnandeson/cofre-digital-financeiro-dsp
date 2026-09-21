import json
import hashlib
import shutil
from pathlib import Path
from typing import Any
from fastapi import UploadFile

from core.logging_config import logger

def garantir_arquivo(arquivo: Path) -> None:
    arquivo.parent.mkdir(parents=True, exist_ok=True)

    if not arquivo.exists():
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

        logger.info("Arquivo JSON criado: %s", arquivo.name)


def ler_json(arquivo: Path) -> list[dict[str, Any]]:
    garantir_arquivo(arquivo)

    try:
        with open(arquivo, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as erro:
        logger.error(
            "JSON inválido em %s: %s",
            arquivo.name,
            erro,
        )

        raise ValueError(
            f"O arquivo {arquivo.name} contém JSON inválido."
        ) from erro


def escrever_json(
    arquivo: Path,
    dados: list[dict[str, Any]],
) -> None:
    garantir_arquivo(arquivo)

    with open(arquivo, "w", encoding="utf-8") as file:
        json.dump(
            dados,
            file,
            ensure_ascii=False,
            indent=4,
        )

    logger.debug(
        "Arquivo %s atualizado com %d registro(s).",
        arquivo.name,
        len(dados),
    )


def buscar_por_id(
    arquivo: Path,
    registro_id: int,
) -> dict[str, Any] | None:
    dados = ler_json(arquivo)

    for item in dados:
        if item["id"] == registro_id:
            return item

    return None


def adicionar(
    arquivo: Path,
    novo_registro: dict[str, Any],
) -> dict[str, Any]:
    dados = ler_json(arquivo)
    
    novo_id = 1
    if dados:
        novo_id = max(item.get("id", 0) for item in dados) + 1
        
    novo_registro["id"] = novo_id
    dados.append(novo_registro)
    
    escrever_json(arquivo, dados)
    return novo_registro


def atualizar(
    arquivo: Path,
    registro_id: int,
    novo_registro: dict[str, Any],
) -> bool:
    dados = ler_json(arquivo)

    for indice, item in enumerate(dados):
        if item["id"] == registro_id:
            novo_registro["id"] = registro_id
            dados[indice] = novo_registro

            escrever_json(
                arquivo,
                dados,
            )

            return True

    return False


def remover(
    arquivo: Path,
    registro_id: int,
) -> bool:
    dados = ler_json(arquivo)

    nova_lista = [
        item
        for item in dados
        if item["id"] != registro_id
    ]

    if len(nova_lista) == len(dados):
        return False

    escrever_json(
        arquivo,
        nova_lista,
    )

    return True


def filtrar(
    arquivo: Path,
    criterios: dict[str, Any],
) -> list[dict[str, Any]]:
    dados = ler_json(arquivo)
    resultados = []
    
    for item in dados:
        corresponde = True
        for chave, valor in criterios.items():
            if valor is not None and item.get(chave) != valor:
                corresponde = False
                break
        
        if corresponde:
            resultados.append(item)
            
    return resultados


def salvar_arquivo_fisico(
    arquivo_upload: UploadFile, 
    diretorio_destino: Path, 
    nome_armazenado: str
) -> Path:
    diretorio_destino.mkdir(parents=True, exist_ok=True)
    caminho_completo = diretorio_destino / nome_armazenado

    with open(caminho_completo, "wb") as buffer:
        shutil.copyfileobj(arquivo_upload.file, buffer)

    logger.info("Ficheiro físico guardado em: %s", caminho_completo)
    return caminho_completo


def deletar_arquivo_fisico(caminho_arquivo: Path) -> bool:
    if caminho_arquivo.exists():
        caminho_arquivo.unlink()
        logger.info("Ficheiro físico apagado: %s", caminho_arquivo.name)
        return True
        
    logger.warning("Tentativa de apagar ficheiro inexistente: %s", caminho_arquivo.name)
    return False


def calcular_hash_sha256(caminho_arquivo: Path) -> str:
    sha256_hash = hashlib.sha256()

    with open(caminho_arquivo, "rb") as f:
        for byte_block in iter(
            lambda: f.read(4096),
            b""
        ):
            sha256_hash.update(byte_block)

    hash_calculado = sha256_hash.hexdigest()

    logger.debug(
        "Hash SHA 256 calculado para %s: %s",
        caminho_arquivo.name,
        hash_calculado
    )

    return hash_calculado
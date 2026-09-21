from pathlib import Path
from datetime import datetime

from fastapi import (
    APIRouter,
    HTTPException, 
    UploadFile,
    File,
    Form,
    Query,
    status
)
from fastapi.responses import FileResponse

from core.logging_config import logger
from models.documento import Documento

from services.json_repository import (
    adicionar,
    atualizar,
    buscar_por_id,
    ler_json,
    remover,
    salvar_arquivo_fisico,
    calcular_hash_sha256,
    deletar_arquivo_fisico,
    filtrar
)

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTOS_FILE = BASE_DIR / "data" / "documentos.json"
ARQUIVOS_DIR = BASE_DIR / "data" / "arquivos"

router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"]
)

@router.post(
    "",
    response_model=Documento,
    status_code=status.HTTP_201_CREATED
)
def criar_documento(
    arquivo: UploadFile = File(...),
    categoria: str = Form(...),
    descricao: str = Form(...),
    tipo: str = Form(...),
    competencia: str = Form(...),
    valor: float = Form(...),
    centro_de_custo: str = Form(...),
    responsavel: str = Form(...),
):
    nome_original = arquivo.filename

    if not nome_original:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo deve possuir um nome."
        )

    extensao = Path(nome_original).suffix.lower()

    documentos = ler_json(DOCUMENTOS_FILE)

    novo_id = 1

    if documentos:
        novo_id = max(
            item.get("id", 0)
            for item in documentos
        ) + 1

    nome_armazenado = f"{novo_id}{extensao}"

    caminho_arquivo = salvar_arquivo_fisico(
        arquivo,
        ARQUIVOS_DIR,
        nome_armazenado
    )

    tamanho = caminho_arquivo.stat().st_size

    sha256 = calcular_hash_sha256(
        caminho_arquivo
    )

    documento = Documento(
        id=novo_id,
        nome_original=nome_original,
        nome_armazenado=nome_armazenado,
        extensao=extensao,
        tipo_mime=arquivo.content_type or "application/octet-stream",
        tamanho=tamanho,
        categoria=categoria,
        descricao=descricao,
        data_upload=datetime.now(),
        sha256=sha256,
        tipo=tipo,
        competencia=competencia,
        valor=valor,
        centro_de_custo=centro_de_custo,
        responsavel=responsavel,
    )

    adicionar(
        DOCUMENTOS_FILE,
        documento.model_dump(mode="json")
    )

    logger.info(
        "Documento criado: id=%s, nome=%s",
        novo_id,
        nome_original,
    )

    return documento


@router.get(
    "",
    response_model=list[Documento],
)
def listar_documentos(
    extensao: str | None = Query(
        default=None
    ),
    centro_de_custo: str | None = Query(
        default=None
    ),
    competencia: str | None = Query(
        default=None
    ),
):
    criterios = {
        "extensao": extensao,
        "centro_de_custo": centro_de_custo,
        "competencia": competencia,
    }

    documentos = filtrar(
        DOCUMENTOS_FILE,
        criterios,
    )

    logger.info(
        "Listagem/filtragem de documentos: %d resultado(s).",
        len(documentos),
    )

    return documentos


@router.get(
    "/{documento_id}",
    response_model=Documento,
)
def obter_documento(documento_id: int):
    documento = buscar_por_id(
        DOCUMENTOS_FILE,
        documento_id,
    )

    if not documento:
        logger.warning(
            "Documento não encontrado: %s",
            documento_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado.",
        )

    return documento

@router.get(
    "/{documento_id}/download"
)
def baixar_documento(documento_id: int):
    documento = buscar_por_id(
        DOCUMENTOS_FILE,
        documento_id
    )

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado."
        )

    caminho_arquivo = (
        ARQUIVOS_DIR /
        documento["nome_armazenado"]
    )

    if not caminho_arquivo.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo físico não encontrado."
        )

    return FileResponse(
        path=caminho_arquivo,
        media_type=documento["tipo_mime"],
        filename=documento["nome_original"]
    )

@router.put(
    "/{documento_id}",
    response_model=Documento,
)
def atualizar_documento(
    documento_id: int,
    documento: Documento,
):
    dados = documento.model_dump(mode="json")

    dados["id"] = documento_id

    if not atualizar(
        DOCUMENTOS_FILE,
        documento_id,
        dados,
    ):
        logger.warning(
            "Tentativa de atualizar documento inexistente: %s",
            documento_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado.",
        )

    logger.info(
        "Documento atualizado: %s",
        documento_id,
    )

    return dados


@router.delete(
    "/{documento_id}",
    status_code=status.HTTP_200_OK,
)
def excluir_documento(documento_id: int):
    documento = buscar_por_id(
        DOCUMENTOS_FILE,
        documento_id,
    )

    if not documento:
        logger.warning(
            "Tentativa de remover documento inexistente: %s",
            documento_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado.",
        )

    caminho_arquivo = (
        ARQUIVOS_DIR /
        documento["nome_armazenado"]
    )

    deletar_arquivo_fisico(caminho_arquivo)

    remover(
        DOCUMENTOS_FILE,
        documento_id,
    )

    logger.info(
        "Documento removido: %s",
        documento_id,
    )

    return {
        "mensagem": "Documento removido com sucesso."
    }
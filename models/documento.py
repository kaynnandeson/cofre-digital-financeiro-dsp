from pydantic import BaseModel, Field
from enum import Enum
from datetime import date, datetime

class Extensao(str, Enum):
    PDF = ".pdf"
    CSV = ".csv"
    XML = ".xml"
    COMPROVANTE = "comprovante"

class Documento(BaseModel):
    id: int = Field(
        gt=0,
        description="Identificador único do documento."
    )

    nome_original: str = Field(
        min_length=5,
        max_length=50
    )
    
    nome_armazenado: str = Field(
        min_length=5,
        max_length=50
    )

    extensao: Extensao = Field(
        default=Extensao.COMPROVANTE
    )

    tipo_mime: str = Field(
        min_length=5,
        max_length=50
    )

    tamanho: float
    categoria: str = Field(
        min_length=3,
        max_length=30
    )

    descricao: str = Field(
        min_length=10,
        max_length=1000
    )

    data_upload: datetime
    sha256: str = Field(
        min_length=3

    )

    tipo: str = Field(
        min_length=3,
        max_length=30
    )

    competencia: str = Field(
        min_length=3,
        max_length=100
    )
    
    valor: float
    centro_de_custo: str
    responsavel: str = Field(
        min_length=5,
        max_length=50
    )
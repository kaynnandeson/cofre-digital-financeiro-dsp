from fastapi import FastAPI

from routes.documentos import router as documentos_router
from routes.integridade import router as integridade_router
from routes.exportacao import router as exportacao_router
from routes.backup import router as backup_router

app = FastAPI()


app.include_router(documentos_router)
app.include_router(integridade_router)
app.include_router(exportacao_router)
app.include_router(backup_router)
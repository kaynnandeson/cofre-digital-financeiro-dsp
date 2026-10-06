from fastapi import FastAPI

from routes.documentos import router as documentos_router
from routes.integridade import router as integridade_router


app = FastAPI()


app.include_router(documentos_router)
app.include_router(integridade_router)
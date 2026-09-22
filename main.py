from fastapi import FastAPI

from routes.documentos import router as documentos_router

app = FastAPI()

app.include_router(documentos_router)
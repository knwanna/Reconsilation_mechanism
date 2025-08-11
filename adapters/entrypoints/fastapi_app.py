from ports.entrypoints import create_app
from fastapi import FastAPI

def create_fastapi_app(repo) -> FastAPI:
    return create_app(repo)
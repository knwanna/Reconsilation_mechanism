from ports.entrypoints import create_app
from fastapi import FastAPI

# This adapter bridges the port interface with FastAPI specifics
def create_fastapi_app(repo) -> FastAPI:
    return create_app(repo)

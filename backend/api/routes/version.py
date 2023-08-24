from fastapi import APIRouter
from .models.version import VersionGet, VersionPost

versions = APIRouter(prefix="/secret/{name}/version")

@versions.get("", response_model=list[VersionGet])
async def get_versions(name: str):
    pass


@versions.get("/{number}", response_model=VersionGet)
async def get_version(number: str, name: str):
    pass


@versions.post("", response_model=VersionGet)
async def create_version(name: str):
    pass


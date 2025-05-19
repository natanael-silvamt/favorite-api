from src.contrib.repository import RepositoryBase


class ClientRepository(RepositoryBase):
    pass


async def client_repository() -> ClientRepository:
    return ClientRepository()

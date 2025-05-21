import pytest
from fastapi import status

from tests.client.factories import client_out_data

# @pytest.mark.usefixtures('mock_usecase_create')
# async def test_post_client_should_create_a_client(client, post_url, client_out, headers) -> None:
#     response = client.post('/clients', headers=headers, json=client_out_data())

#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json() == client_out.model_dump()

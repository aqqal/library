from fastapi import APIRouter, Request, Depends, Response
from app.auth import validate_token

import httpx
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(
	prefix="/semanticSearch",
	dependencies=[Depends(validate_token)]
)

@router.api_route('/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def forward(request: Request, path: str):
	method = request.method
	body = await request.body()
	headers = request.headers

	url = os.getenv('SEMANTIC_SEARCH_URL')
	url = url + "/" + path

	async with httpx.AsyncClient() as client:
		response = await client.request(method, url, data=body, headers=headers)

	return Response(content=response.content, status_code=response.status_code, headers=response.headers)
from fastapi import APIRouter
from app.schemas.example import ExampleResponse

router = APIRouter(prefix='/example', tags=['example'])


@router.get('/', response_model=ExampleResponse)
def read_example() -> dict:
    return {'message': 'Hello from taskflow'}

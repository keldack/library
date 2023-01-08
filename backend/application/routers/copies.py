from fastapi import APIRouter, HTTPException, status, Request, Response

from application.schemas.copies import CopyInputSchema, PatchCopyInputSchema
from domain.models import Book, Copy
from domain.usecases.copies import CreateCopy, ReadCopies, ReadCopy, PatchCopy, DeleteCopy
from domain.usecases.exceptions import KeyDoesNotExist

router = APIRouter()

from fastapi import APIRouter

router = APIRouter(
    prefix="/copies",
    tags=["copies"]
)

@router.get("")
async def get_all_copies():
    """Get all copies"""
    copies = ReadCopies().execute()
    return [copy.to_schema() for copy in copies]


@router.get("/{copy_id}")
async def get_copy_by_id(copy_id: int):
    """Get a copy of a book by its id"""
    try:
        copy = ReadCopy().execute(copy_id)
        return copy.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_copy(request: Request, response: Response, schema: CopyInputSchema):
    """Create a copy"""
    try:
        copy: Copy = schema.to_domain()
        copy = CreateCopy().execute(copy)
        response.headers["Location"] = f"{request.base_url}copies/{copy.id}"
        return copy.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.patch("/{copy_id}")
async def patch_copy(copy_id: int, schema: PatchCopyInputSchema):
    """Modify a copy"""
    try:
        copy = Copy(id = copy_id, place = schema.place)
        copy = PatchCopy().execute(copy)
        return copy.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))        


@router.delete("/{copy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_copy(copy_id: int):
    """Delete a copy"""
    try:
        DeleteCopy().execute(copy_id)
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
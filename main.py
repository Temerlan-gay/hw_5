from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_404_NOT_FOUND, HTTP_302_FOUND

app = FastAPI()

templates = Jinja2Templates(directory="templates")

books = [
    {
        "id": 1,
        "title": "Harry Potter",
        "author": "Rowling"
    },
    {
        "id": 2,
        "title": "The Hobbit",
        "author": "Tolkien"
    }
]


def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


@app.get("/books", response_class=HTMLResponse)
def books_list(request: Request):
    return templates.TemplateResponse(
        "books/index.html",
        {
            "request": request,
            "books": books
        }
    )


@app.get("/books/{id}", response_class=HTMLResponse)
def book_detail(request: Request, id: int):
    book = get_book(id)

    if not book:
        return HTMLResponse(
            content="Not Found",
            status_code=HTTP_404_NOT_FOUND
        )

    return templates.TemplateResponse(
        "books/detail.html",
        {
            "request": request,
            "book": book
        }
    )


@app.get("/books/{id}/edit", response_class=HTMLResponse)
def edit_book_page(request: Request, id: int):
    book = get_book(id)

    if not book:
        return HTMLResponse(
            content="Not Found",
            status_code=HTTP_404_NOT_FOUND
        )

    return templates.TemplateResponse(
        "books/edit.html",
        {
            "request": request,
            "book": book
        }
    )


@app.post("/books/{id}/edit")
def edit_book(
    id: int,
    title: str = Form(...),
    author: str = Form(...)
):
    book = get_book(id)

    if not book:
        return HTMLResponse(
            content="Not Found",
            status_code=HTTP_404_NOT_FOUND
        )

    book["title"] = title
    book["author"] = author

    return RedirectResponse(
        url=f"/books/{id}",
        status_code=HTTP_302_FOUND
    )


@app.post("/books/{id}/delete")
def delete_book(id: int):
    book = get_book(id)

    if not book:
        return HTMLRцвesponse(
            content="Not Found",
            status_code=HTTP_404_NOT_FOUND
        )

    books.remove(book)

    return RedirectResponse(
        url="/books",
        status_code=HTTP_302_FOUND
    )
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import review

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    """Return landing page with reviews injected dynamically"""
    reviews = review.get_reviews()
    # Convert reviews into HTML snippet
    review_html = "".join(
        f"<div class='p-3 my-2 bg-gray-100 rounded shadow'>{r.message}</div>" for r in reviews
    )
    # Inject into index.html (very basic string replace)
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read().replace("{{reviews_here}}", review_html or "<p>No reviews yet.</p>")
    return HTMLResponse(content=html)

@app.get("/docs-page")
async def read_docs():
    return FileResponse("static/docs.html")


@app.get("/docs-page")
async def read_docs():
    return FileResponse("static/docs.html")

@app.post("/submit-review")
async def submit_review(message: str = Form(...)):
    review.add_review(message)
    return JSONResponse({"status": "success", "message": "Review submitted!"})
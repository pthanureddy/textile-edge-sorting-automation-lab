from __future__ import annotations

from fastapi import FastAPI

from textile_edge_sorting.models import ClassificationRequest, ClassificationResponse
from textile_edge_sorting.pipeline import process_textile_item

app = FastAPI(title="Textile Edge Sorting Automation Lab", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/classify", response_model=ClassificationResponse)
async def classify(request: ClassificationRequest) -> ClassificationResponse:
    return process_textile_item(request.serial_frame, request.image_ppm)

import os
import io
import base64

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import Response
from openai import OpenAI

app = FastAPI(title="HDREAL Processor")

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

HDREAL_PROMPT = """HDreal — mantener exactamente la foto original, no modificar ni reinterpretar ningún objeto, mueble, textura, color, vetas ni proporciones. Solo aumentar definición y calidad de imagen y extender el lienzo para adaptar a formato 9:16, rellenando únicamente las zonas fuera de la foto original. Sin zoom, sin recorte y sin alterar la imagen original. Fotografía realista, natural, sin apariencia de IA."""


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "HDREAL Processor"
    }


@app.post("/process")
async def process_image(
    image: UploadFile = File(...),
    format: str = Form("9:16")
):

    image_bytes = await image.read()

    result = client.images.edit(
        model="gpt-image-2",
        image=io.BytesIO(image_bytes),
        prompt=HDREAL_PROMPT
    )

    image_base64 = result.data[0].b64_json
    output = base64.b64decode(image_base64)

    return Response(
        content=output,
        media_type="image/png"
    )

import os
import base64
import io

from mcp.server.mcpserver import MCPServer
from openai import OpenAI

mcp = MCPServer(
    "HDREAL",
    instructions="Procesador de imágenes HDREAL para fotografías de Cambá."
)

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

HDREAL_PROMPT = """HDreal — mantener exactamente la foto original, no modificar ni reinterpretar ningún objeto, mueble, textura, color, vetas ni proporciones. Solo aumentar definición y calidad de imagen y extender el lienzo para adaptar a formato 9:16, rellenando únicamente las zonas fuera de la foto original. Sin zoom, sin recorte y sin alterar la imagen original. Fotografía realista, natural, sin apariencia de IA."""


@mcp.tool()
def hdreal_process_image(
    image_base64: str,
    format: str = "9:16"
) -> str:
    """
    Procesa una fotografía mediante HDREAL.

    Formatos:
    - 4:5 para carruseles y publicaciones
    - 9:16 para reels e historias
    - 1:1 para publicaciones cuadradas

    La instrucción HDREAL es fija y no debe modificarse.
    """

    image_bytes = base64.b64decode(image_base64)

    result = client.images.edit(
        model="gpt-image-2",
        image=io.BytesIO(image_bytes),
        prompt=HDREAL_PROMPT
    )

    output_base64 = result.data[0].b64_json

    return output_base64


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000"))
    )

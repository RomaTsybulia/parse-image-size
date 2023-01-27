import asyncio

from PIL import ImageFile
from httpx import AsyncClient


async def get_image_size(url, client):
    if url == "nan":
        return ["There is no image url"]

    resume_header = {"Range": "bytes=0-2000000"}
    data = await client.get(url, headers=resume_header, timeout=None)
    picture = ImageFile.Parser()
    picture.feed(data.content)
    if picture.image:
        size = str(picture.image.size).replace(", ", "x")
        for bracket in ["(", ")"]:
            size = size.replace(bracket, "")

        return [size]
    else:
        return ["Image not found"]


async def parse_image_sizes(urls: list[str]):
    async with AsyncClient(timeout=None) as client:
        image_sizes = await asyncio.gather(
            *[get_image_size(url, client) for url in urls]
        )

        return image_sizes


if __name__ == "__main__":
    """
    Test urls
    """
    url_list = [
        "https://data.sanitino.eu/PRODUCT-20240/4a457da85a2fdc9cb9219e2b?size=feed-1080",
        "https://data.sanitino.eu/PRODUCT-47765/58a1a3d7842e0515b103755c?size=feed-1080",
        "https://data.sanitino.eu/PRODUCT-56372/764c369a72c207d3db0c93aa?v=b040ef90&size=feed-1080",
        "https://data.sanitino.eu/PRODUCT-90692/5a30dff9395b0570fbff18a5?v=5c35de00&size=feed-1080",
    ]
    print(asyncio.run(parse_image_sizes(url_list)))

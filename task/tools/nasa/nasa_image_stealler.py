import asyncio
from typing import Any
import aiohttp
import requests

from task._constants import NASA_API_KEY, NASA_API, DIAL_ENDPOINT, NASA_IMG_STEALER
from task.tools.base import BaseTool
from task.tools.nasa.models.image import ImageList, Image


class NasaImageStealerTool(BaseTool):

    TOOL_CONFIG = {
        "type": "function",
        "function": {
            "name": NASA_IMG_STEALER,
            "description": "This tool provides description of the largest NASA image by Mars sol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sol": {
                        "type": "integer",
                        "description": "Sol of Mars."
                    }
                },
                "required": ["sol"]
            }
        }
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    def execute(self, arguments: dict[str, Any]) -> str:
        try:
            sol = int(arguments["sol"])
            image_list = self._fetch_image_list(sol)

            largest_picture_url = asyncio.run(self._get_largest_picture_async(image_list))

            return self._get_image_description(largest_picture_url)
        except Exception as e:
            return str(e)

    def _fetch_image_list(self, sol: int) -> ImageList:
        if not NASA_API_KEY:
            raise RuntimeError("NASA API Key is blank")

        url = f"{NASA_API}?sol={sol}&api_key={NASA_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        images = [Image(id=photo["id"], sol=photo["sol"], img_src=photo["img_src"])
                  for photo in data["photos"]]

        return ImageList(photos=images)

    async def _get_largest_picture_async(self, image_list: ImageList) -> str:
        """Async version that fetches all content lengths concurrently"""
        if not image_list.photos:
            raise RuntimeError("No images found")

        await self._get_all_content_lengths_async(image_list.photos)

        largest_image = max(image_list.photos, key=lambda x: x.content_length)
        return largest_image.img_src

    async def _get_all_content_lengths_async(self, images: list[Image]):
        """Fetch content lengths for all images concurrently"""
        connector = aiohttp.TCPConnector(
            limit=20,
            limit_per_host=10,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={'User-Agent': 'NASA-Image-Fetcher/1.0'}
        ) as session:
            tasks = [
                self._get_content_length_async(session, image)
                for image in images
            ]
            await asyncio.gather(*tasks)

    async def _get_content_length_async(self, session: aiohttp.ClientSession, image: Image):
        """Async method to get content length for a single image"""
        async with session.head(
                image.img_src,
                allow_redirects=True,
                max_redirects=10
        ) as response:
            image.content_length = int(response.headers.get("Content-Length", 0))

    def _get_image_description(self, url: str) -> str:
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }

        request_data = {
            "model": "gpt-4o-mini-2024-07-18",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url
                            }
                        }
                    ]
                }
            ]
        }

        endpoint = DIAL_ENDPOINT.format(model="gpt-4o-mini-2024-07-18")
        response = requests.post(url=endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            return f"URL: {url}\nDescription: {data['choices'][0]['message']['content']}"
        else:
            return f"Error: {response.status_code} {response.text}"

import io
import os
import base64
import asyncio

from os import getenv
from PIL import Image
from os.path import exists
from fastapi import FastAPI
from uvicorn import Config, Server
from starlette.responses import JSONResponse, Response, FileResponse
from starlette.middleware.base import BaseHTTPMiddleware

from model.image_gen import KandinskyImageGen

from .schemas import Text2Img, MixImages
from .auth_middleware import AuthMiddleware

class GeneratorRestAPI(FastAPI):    
    image_gen: KandinskyImageGen

    def __init__(
            self, 
        ) -> None:
        super().__init__()
        
        # Initialize model
        self.image_gen = KandinskyImageGen()
        self.image_gen.load_model()

        # Enable token access
        auth_middleware = AuthMiddleware(os.getenv('TOKEN'))
        self.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

        # Register routes
        self.add_api_route("/text2img", self.text2img, methods=["POST"])
        self.add_api_route("/mix2images", self.mix2images, methods=["POST"])
        self.add_api_route("/", self.homepage_get, methods=["GET"])
        self.add_api_route("/img/{file_name}", self.image_get, methods=["GET"])

    async def homepage_get(self):
        return JSONResponse({'RestAPI': 'Kandinskiy 2.1 Model',\
            'website': 'https://web.devoid.pics/'}, status_code=200)
    
    async def text2img(self, payload: Text2Img):
        image_bytes = await self.image_gen.text2img(
            prompt = payload.prompt,
            steps = payload.steps,
            guidance_scale = payload.guidance_scale,
            h = payload.height,
            w = payload.width,
            sampler = payload.sampler,
            prior_cf_scale = payload.prior_cf_scale,
            prior_steps = payload.prior_steps,
            negative_prior_prompt = payload.negative_prior_prompt,
            negative_decoder_prompt = payload.negative_decoder_prompt
        )
        return Response(content=image_bytes, media_type="image/jpg")

    async def mix2images(self, payload: MixImages):
        if len(payload.images_texts) != 4:
            print(payload.images_texts)
            raise ValueError('Images texts are not required size')
        
        bytesIO = io.BytesIO(base64.b64decode(payload.images_texts[1]))
        i1 = Image.open(bytesIO)
        bytesIO = io.BytesIO(base64.b64decode(payload.images_texts[2]))
        i2 = Image.open(bytesIO)

        with open('aaboba.png', 'wb') as i:
            i.write(base64.b64decode(payload.images_texts[1]))
            print('written')

        payload.images_texts = [payload.images_texts[0], i1, i2, payload.images_texts[3]]

        image_bytes = await self.image_gen.mix2images(
            images_texts = payload.images_texts,
            weights = payload.weights,
            steps = payload.steps,
            guidance_scale = payload.guidance_scale,
            h = payload.height,
            w = payload.width,
            sampler = payload.sampler,
            prior_cf_scale = payload.prior_cf_scale,
            prior_steps = payload.prior_steps,
            negative_prior_prompt = payload.negative_prior_prompt,
            negative_decoder_prompt = payload.negative_decoder_prompt
        )
        return Response(content=image_bytes, media_type="image/jpg")
    
    async def image_get(self, file_name: str):
        '''Returns the image with the given id'''
        path = f"{getenv('IMAGES_PATH')}/{file_name}"
        if not exists(path):
            return JSONResponse({"content": "Image not found"}, status_code=404)
        return FileResponse(path, media_type='image/jpg')

    def start(self, loop = None):
        if loop is None:
            loop = asyncio.get_running_loop()
        port = int(getenv('API_PORT'))
        server_config = Config(self, host=getenv('API_HOST'), port=port, loop=loop)
        server = Server(config=server_config)
        loop.create_task(server.serve())
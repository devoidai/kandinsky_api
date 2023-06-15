import io
import logging
import datetime

from PIL import Image
from os import getenv
from kandinsky2 import get_kandinsky2, Kandinsky2_1

from .converters import image_to_bytes

class KandinskyImageGen:
    model: Kandinsky2_1

    def __init__(self) -> None:
        self.model = None

    def load_model(self):
        logging.info('Loading Kandinsky model...')
        self.model = get_kandinsky2('cuda', task_type='text2img', model_version='2.1', use_flash_attention=False)
        logging.info('Model Kandinsky 2.1 loaded')

    async def text2img(
            self,
            prompt: str,
            steps: int = 30,
            guidance_scale: int = 4, #(1 - Prompt игнорируется; 30 - Четко следовать запросу)
            h = 512,
            w = 512,
            sampler = 'p_sampler',
            prior_cf_scale = 4,
            prior_steps = '5',
            negative_prior_prompt = '',
            negative_decoder_prompt = ''
        ) -> None:
        images = self.model.generate_text2img(
            prompt = prompt,
            num_steps = steps,
            guidance_scale = guidance_scale,
            h = h,
            w = w,
            sampler = sampler,
            prior_cf_scale = prior_cf_scale,
            prior_steps = prior_steps,
            negative_prior_prompt = negative_prior_prompt,
            negative_decoder_prompt = negative_decoder_prompt
        )
        tz = datetime.timezone.utc
        ft = "%Y_%m_%dT%H_%M_%S"
        time = datetime.datetime.now(tz=tz).strftime(ft)
        file_name = f'{time}.jpg'
        images[0].save(f"{getenv('IMAGES_PATH')}{file_name}")
        return image_to_bytes(images[0])

    async def mix2images(
            self,
            images_texts: list,
            weights: list,
            steps: int = 30,
            guidance_scale: int = 4, #(1 - Prompt игнорируется; 30 - Четко следовать запросу)
            h = 512,
            w = 512,
            sampler = 'p_sampler',
            prior_cf_scale = 4,
            prior_steps = '5',
            negative_prior_prompt = '',
            negative_decoder_prompt = ''
        ) -> None:
        images = self.model.mix_images(
            images_texts = images_texts,
            weights = weights,
            num_steps = steps,
            guidance_scale = guidance_scale,
            h = h,
            w = w,
            sampler = sampler,
            prior_cf_scale = prior_cf_scale,
            prior_steps = prior_steps,
            negative_prior_prompt = negative_prior_prompt,
            negative_decoder_prompt = negative_decoder_prompt
        )
        tz = datetime.timezone.utc
        ft = "%Y_%m_%dT%H_%M_%S"
        time = datetime.datetime.now(tz=tz).strftime(ft)
        file_name = f'{time}.jpg'
        images[0].save(f"{getenv('IMAGES_PATH')}{file_name}")
        return image_to_bytes(images[0])
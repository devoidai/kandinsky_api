from pydantic import BaseModel
from typing import Union, List

class Text2Img(BaseModel):
    prompt: str
    steps: Union[int, None] = 30
    guidance_scale: Union[int, None] = 4
    height: Union[int, None] = 512
    width: Union[int, None] = 512
    sampler: Union[str, None] = 'p_sampler'
    prior_cf_scale: Union[int, None] = 4
    prior_steps: Union[str, None] = '5'
    negative_prior_prompt: Union[str, None] = ''
    negative_decoder_prompt: Union[str, None] = ''

class MixImages(BaseModel):
    images_texts: list # str, base64_image, base64_image, str
    weights: list # float, float, float, float
    steps: Union[int, None] = 30
    guidance_scale: Union[int, None] = 4
    height: Union[int, None] = 512
    width: Union[int, None] = 512
    sampler: Union[str, None] = 'p_sampler'
    prior_cf_scale: Union[int, None] = 4
    prior_steps: Union[str, None] = '5'
    negative_prior_prompt: Union[str, None] = ''
    negative_decoder_prompt: Union[str, None] = ''
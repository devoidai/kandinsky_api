from fastapi import Request
from starlette.responses import JSONResponse

class AuthMiddleware:
    token: str
        
    def __init__(self, token):
        self.token = token
        
    async def __call__(self, request: Request, call_next):
        '''Verifies the token in the request header'''
        try:
            token = request.headers["authorization"]
            if self.token == token:
                response = await call_next(request)
                return response
            else:
                print('INVALID AUTHORIZATION')
            return JSONResponse(content='Invalid Authorization', status_code=401)
        except KeyError as er:
            return JSONResponse(content='Invalid Authorization', status_code=401)

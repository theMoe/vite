from fastapi import Header, HTTPException

async def get_token_header(x_access_token: str = Header(...)):
    if x_access_token != "":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_hook_token_header(x_access_token: str = Header(...)):
    if x_access_token != "":
        raise HTTPException(status_code=400, detail="X-Token header for incoming posts invalid")

def get_dex_api_url(version):
    return 'https://api.vitex.net/api/v' + str(version)

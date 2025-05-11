import json
from fastapi.responses import JSONResponse

class UTF8JSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":")
        ).encode("utf-8")

def fix_encoding(text):
    try:
        return text.encode('latin1').decode('utf-8')
    except:
        return text
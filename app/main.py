from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import Form
from src.emissao_nodriver import processar_certidao

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home (request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"request": request}
    )

@app.get("/manual")
def manual(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="manual.html",
        context={"request": request}
    )

@app.get("/planilha")
def planilha(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="planilha.html",
        context={"request": request}
    )

@app.post("/emitir-manual")
async def emitir_manual(
    request: Request,
    tipo: str = Form(...),
    documento: str = Form(...),
    data_nascimento: str = Form("")
):
    resultado = await processar_certidao(
        tipo=tipo,
        documento=documento,
        data_nascimento=data_nascimento
    )

    return templates.TemplateResponse(
        request=request,
        name="resultado.html",
        context={
            "request": request,
            "resultado": resultado
        }
    )
import sys
import asyncio
import shutil
import os

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.leitor_planilha import ler_planilha_certidoes

from src.emissao_nodriver import processar_certidao

from fastapi.responses import FileResponse
from pathlib import Path

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
    resultado = await asyncio.to_thread(
        lambda: asyncio.run(processar_certidao(
            tipo=tipo,
            documento=documento,
            data_nascimento=data_nascimento
        ))
    )

    return templates.TemplateResponse(
         request=request,
         name="resultado.html",
         context={
              "request": request,
              "resultado": resultado
         }
    )
@app.post("/processar-planilha")
async def processar_planilha(
    request: Request,
    planilha: UploadFile = File(...)):
    os.makedirs("entrada_planilhas", exist_ok=True)

    caminho_arquivo = f"entrada_planilhas/{planilha.filename}"

    with open(caminho_arquivo, "wb") as buffer:
        shutil.copyfileobj(planilha.file, buffer)

    registros, erros = ler_planilha_certidoes(caminho_arquivo)

    resultados_processados = []

    for registro in registros:
        resultado = await asyncio.to_thread(
            lambda registro=registro: asyncio.run(processar_certidao(
                tipo=registro["tipo"],
                documento=registro["documento"],
                data_nascimento=registro["data_nascimento"]
            ))
        )

        resultados_processados.append(resultado)

    total_sucessos = sum(
        1 for resultado in resultados_processados
        if resultado["sucesso"]
    )

    total_arquivos_encontrados = sum(
        1 for resultado in resultados_processados
        if resultado["arquivo_encontrado"]
    )

    return templates.TemplateResponse(
        request=request,
        name="resultado_planilha.html",
        context={
            "request": request,
            "arquivo": caminho_arquivo,
            "total_registros_validos": len(registros),
            "total_erros_validacao": len(erros),
            "total_processados": len(resultados_processados),
            "total_sucessos": total_sucessos,
            "total_arquivos_encontrados": total_arquivos_encontrados,
            "erros": erros,
            "resultados": resultados_processados
        }
    )

@app.get("/baixar-certidao/{nome_arquivo}")
def baixar_certidao(nome_arquivo: str):
    pasta_certidoes = Path("certidoes_emitidas")
    caminho_arquivo = pasta_certidoes / nome_arquivo

    if not caminho_arquivo.exists():
        return {"erro": "Arquivo não encontrado"}
    
    return FileResponse(
        path=caminho_arquivo,
        filename=nome_arquivo,
        media_type="application/pdf"
    )
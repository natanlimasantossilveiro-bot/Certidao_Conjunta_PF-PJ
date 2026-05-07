import json
from pathlib import Path
from datetime import datetime

CAMINHO_HISTORICO = Path("dados/historico_emissoes.json")


def garantir_arquivo_historico():
    CAMINHO_HISTORICO.parent.mkdir(parents=True, exist_ok=True)

    if not CAMINHO_HISTORICO.exists():
        CAMINHO_HISTORICO.write_text("[]", encoding="utf-8")


def carregar_historico():
    garantir_arquivo_historico()

    conteudo = CAMINHO_HISTORICO.read_text(encoding="utf-8")

    if not conteudo.strip():
        return []
    
    return json.loads(conteudo)

def salvar_no_historico(resultado):
    historico = carregar_historico()

    registro = {
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": resultado.get("tipo", ""),
        "documento": resultado.get("documento", ""),
        "status_final": resultado.get("status_final", ""),
        "mensagem_final": resultado.get("mensagem_final", ""),
        "sucesso": resultado.get("sucesso", False),
        "arquivo_encontrado": resultado.get("arquivo_encontrado", False),
        "caminho_certidao": resultado.get("caminho_certidao", ""),
        "url_print": resultado.get("url_print", "")
    }

    historico.append(registro)

    CAMINHO_HISTORICO.write_text(
        json.dumps(historico, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )
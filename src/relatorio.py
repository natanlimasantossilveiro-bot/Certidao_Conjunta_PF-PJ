import csv
from datetime import datetime
import os

def gerar_relatorio_csv(resultados_processados):
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_relatorios = "relatorios"
    os.makedirs(pasta_relatorios, exist_ok=True)
    nome_arquivo = os.path.join(
        pasta_relatorios,
        f"relatorio_certidoes_{data_hora}.csv"
    )

    fieldnames=[
        "linha_processada",
        "tipo",
        "documento",
        "data_nascimento",
        "status_emissao",
        "mensagem_emissao",
        "status_pdf",
        "mensagem_pdf",
        "status_final",
        "mensagem_final",
        "caminho_certidao"
    ]

    with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo_csv:
        writer = csv.DictWriter(
            arquivo_csv,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()

        for resultado in resultados_processados:
            writer.writerow(resultado)

    return nome_arquivo
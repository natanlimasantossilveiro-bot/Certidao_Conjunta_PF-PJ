import asyncio

from src.leitor_planilha import ler_planilha_certidoes
from src.emissao_nodriver import processar_certidao


async def main():
    caminho_planilha = input("Informe o caminho da planilha Excel: ").strip()

    registros, erros = ler_planilha_certidoes(caminho_planilha)

    print("\n=== ERROS ENCONTRADOS NA PLANILHA ===")
    if erros:
        for erro in erros:
            print(f"Linha {erro['linha']}: {', '.join(erro['erros'])}")
    else: 
        print("Nenhum erro encontrado.")

    print("\n=== INICIANDO PROCESSAMENTO ===")

    resultados_processados = []

    for registro in registros:
        print(f"\nProcessando linha {registro['linha']}...")
        print(f"Tipo: {registro['tipo']}")
        print(f"Documento: {registro['documento']}")

        resultado = await processar_certidao(
            tipo=registro["tipo"],
            documento=registro["documento"],
            data_nascimento=registro["data_nascimento"],
        )

        resultados_processados.append(resultado)
    
        print(f"Status emissão: {resultado['status_emissao']}")
        print(f"Mensagem emissão: {resultado['mensagem_emissao']}")
        print(f"Status PDF: {resultado['status_pdf']}")
        print(f"Mensagem PDF: {resultado['mensagem_pdf']}")
        print("----------------------------------------------")


    total_registros = len(resultados_processados)

    sucesso_confirmado = sum(
        1 for resultado in resultados_processados
        if resultado["status_final"] == "sucesso_confirmado"
    )

    sucesso_provavel = sum(
        1 for resultado in resultados_processados
        if resultado["status_final"] == "sucesso_provavel"
    )

    erro_receita = sum(
        1 for resultado in resultados_processados
        if resultado["status_final"] == "erro_receita"
    )

    falha_indefinida = sum(
        1 for resultado in resultados_processados
        if resultado["status_final"] == "falha_indefinida"
    )

    print(f"Total de registros válidos: {total_registros}")
    print(f"Sucesso confirmado: {sucesso_confirmado}")
    print(f"Sucesso provável: {sucesso_provavel}")
    print(f"Erro na Receita: {erro_receita}")
    print(f"Falha Indefinida: {falha_indefinida}")

if __name__ == "__main__":
    asyncio.run(main())
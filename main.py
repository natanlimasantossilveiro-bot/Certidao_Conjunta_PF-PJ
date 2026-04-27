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

    for registro in registros:
        print(f"\nProcessando linha {registro['linha']}...")
        print(f"Tipo: {registro['tipo']}")
        print(f"Documento: {registro['documento']}")

        resultado = await processar_certidao(
            tipo=registro["tipo"],
            documento=registro["documento"],
            data_nascimento=registro["data_nascimento"],
        )
    
        print(f"Status emissão: {resultado['status_emissao']}")
        print(f"Mensagem emissão: {resultado['mensagem_emissao']}")
        print(f"Status PDF: {resultado['status_pdf']}")
        print(f"Mensagem PDF: {resultado['mensagem_pdf']}")
        print("----------------------------------------------")

if __name__ == "__main__":
    asyncio.run(main())
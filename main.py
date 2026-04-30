import asyncio

from src.leitor_planilha import ler_planilha_certidoes
from src.emissao_nodriver import processar_certidao
from src.relatorio import gerar_relatorio_csv

async def executar_modo_planilha():
    print("Modo de emissão por planilha selecionado")

    caminho_planilha = input("Informe o caminho da planilha Excel: ").strip()

    registros, erros = ler_planilha_certidoes(caminho_planilha)

    print("\n=== ERROS ENCONTRADOS NA PLANILHA ===")

    if erros:
        for erro in erros:
            print(f"Linha {erro['linha']}: {', '.join(erro['erros'])}")
    else:
        print('Nenhum erro encontrado.')

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
        print(f"Status final: {resultado['status_final']}")
        print(f"Mensagem final: {resultado['mensagem_final']}")
        print(f"Sucesso: {'Sim' if resultado['sucesso'] else 'Não'}")
        print(f"Caminho da certidão: {resultado['caminho_certidao'] or 'Não localizada/movida.'}")
        print("-----------------------------------------------")

    total_registros = len(resultados_processados)

    total_sucessos = sum(
        1 for resultado in resultados_processados
        if resultado["sucesso"]
    )

    total_arquivos_encontrados = sum(
        1 for resultado in resultados_processados
        if resultado["arquivo_encontrado"]
    )

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

    print(f"Total de Registros Válidos: {total_registros}")
    print(f"Total de Sucessos: {total_sucessos}")
    print(f"Arquivos Encontrados: {total_arquivos_encontrados}")
    print(f"Sucesso Confirmado: {sucesso_confirmado}")
    print(f"Sucesso Provável: {sucesso_provavel}")
    print(f"Erro na Receita: {erro_receita}")
    print(f"Falha Indefinida: {falha_indefinida}")

    nome_relatorio = gerar_relatorio_csv(resultados_processados)
    print(f"Relatório CSV gerado com sucesso: {nome_relatorio}")
        

async def main():

    print("=== SISTEMA DE EMISSÃO DE CERTIDÕES ===")
    print("1 - Emitir por planilha")
    print("2 - Emitir manualmente")

    modo = input("Escolha o modo de emissão: ").strip()

    if modo == "1":
        await executar_modo_planilha()

    elif modo == "2":

        print("Modo de emissão manual selecionado")
        
        tipo = input("Informe o tipo de certidão (pf/pj): ").strip().lower()

        if tipo not in ["pf", "pj"]:
            print("Tipo inválido. Escolha 'pf' ou 'pj'.")
            return
        
        documento = input("Informe o CPF/CNPJ: ").strip()

        data_nascimento = ""

        if tipo == "pf":


            data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()

        resultado = await processar_certidao(
            tipo=tipo,
            documento=documento,
            data_nascimento=data_nascimento,
        )

        print("\n=== RESULTADO DA EMISSÃO MANUAL ===")
        print(f"Status final: {resultado['status_final']}")
        print(f"Mensagem final: {resultado['mensagem_final']}")
        print(f"Sucesso: {'Sim' if resultado['sucesso'] else 'Não'}")
        print(f"Arquivo encontrado: {'Sim' if resultado['arquivo_encontrado'] else 'Não'}")
        print(f"Caminho da certidão: {resultado['caminho_certidao'] or 'Não localizada/movida.'}")

    else:
        print("Opção inválida. Escolha 1 para planilha ou 2 para manual.")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(1))
    finally:
        loop.close()
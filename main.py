from src.leitor_planilha import ler_planilha_certidoes


def main():
    caminho_planilha = input("Informe o caminho da planilha Excel: ").strip()

    registros, erros = ler_planilha_certidoes(caminho_planilha)

    print("\n===ERROS ENCONTRADOS NA PLANILHA ===")
    if erros:
        for erro in erros:
            print(f"Linha{erro['linha']}: {','. join(erro['erros'])}")
    else: 
        print("Nenhum erro encontrado .")

    print("\n=== INICIANDO PROCESSAMENTO ===")

    for registro in registros:
        print(f"\nProcessando linha {registro['linha']}...")
        print(f"Tipo: {registro['tipo']}")
        print(f"Documento: {registro['documento']}")

        processar_certidao(
            tipo=registro["tipo"],
            documento=registro["documento"],
            data_nascimento=registro["data_nascimento"]
        )
    
    print("\nProcessamento finalizado.")

if __name__ == "__main__":
    main()
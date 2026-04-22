from src.navegador import abrir_navegador
from src.emissao import (
    clicar_botao_aceitar_cookies,
    selecionar_tipo_certidao,
    preencher_dados_pf,
    preencher_dados_pj,
    clicar_botao_emitir
)


def main():
    nome_certidao = input(
        "Informe qual é o tipo de certidão que gostaria de emitir (pf/pj): "
    ).strip().lower()

    if nome_certidao not in ["pf", "pj"]:
        print(
            "Opção inválida. Por favor, escolha 'pf' para pessoa física ou 'pj' para pessoa jurídica."
        )
        return

    driver = abrir_navegador()
    clicar_botao_aceitar_cookies(driver)
    selecionar_tipo_certidao(driver, nome_certidao)

    if nome_certidao == "pf":
        cpf = input("Informe o CPF da Pessoa Física: ").strip()
        data_nascimento = input("Informe a data de nascimento da Pessoa Física: ").strip()
        
        preencher_dados_pf(driver, cpf, data_nascimento)
        clicar_botao_emitir(driver)

        print("Dados preenchidos e tentativa de clique no botão Emitir Certidão realizada.")
        input("Pressione Enter para finalizar o processo")

    elif nome_certidao == "pj":
        cnpj = input("Informe o CNPJ da Pessoa Jurídica: ").strip()

        preencher_dados_pj(driver, cnpj)
        clicar_botao_emitir(driver)

        print("Dados preenchidos e tentativa de clique no botão Emitir Certidão realizada.")          
        input("Pressione Enter para finalizar o processo")

if __name__ == "__main__":
    main()
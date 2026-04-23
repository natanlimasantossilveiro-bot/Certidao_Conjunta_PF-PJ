import asyncio
from src.emissao_nodriver import (
    abrir_pagina_receita,
    selecionar_tipo_certidao,
    preencher_dados_pf,
    clicar_botao_emitir,
    clicar_botao_emitir_validado,
    verificar_mensagem_erro
)


async def main():
    nome_certidao = input(
        "Informe qual é o tipo de certidão que gostaria de emitir (pf/pj): "
    ).strip().lower()

    if nome_certidao not in ["pf", "pj"]:
        print(
            "Opção inválida. Por favor, escolha 'pf' para pessoa física ou 'pj' para pessoa jurídica."
        )
        return
    
    browser, page = await abrir_pagina_receita()
    await selecionar_tipo_certidao(page, nome_certidao)
    
    if nome_certidao == "pf":
        cpf = input("Informe o CPF da Pessoa Física: ").strip()
        data_nascimento = input("Informe a data de nascimento da Pessoa Física: ").strip()

        await preencher_dados_pf(page, cpf, data_nascimento)
        await clicar_botao_emitir(page)
        await clicar_botao_emitir_validado(page)
        await verificar_mensagem_erro(page)

    input("Pressione Enter para finalizar o processo...")
    await browser.stop()

if __name__ == "__main__":
    asyncio.run(main())        
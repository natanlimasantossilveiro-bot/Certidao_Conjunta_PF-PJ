import nodriver as nd

async def abrir_pagina_receita():
    browser = await nd.start(headless=False)  # Inicia o navegador em modo não headless
    page = await browser.get("https://servicos.receitafederal.gov.br/servico/certidoes/#/home")
    await page.wait(3)
    return browser, page


async def selecionar_tipo_certidao(page, tipo):
    if tipo.lower() == "pf":
        await page.evaluate("""
            (() => {
                const botao = document.querySelector('a[href="#/home/cpf"]');
                if (botao) {
                    botao.click();
                    return "PF clicado";
                }
                return "Botão PF não encontrado";
            })()
        """)
    elif tipo.lower() == "pj":
        await page.evaluate("""
            (() => {
                const botao = document.querySelector('a[href="#/home/cnpj"]');
                if (botao) {
                    botao.click();
                    return "PJ clicado";
                }
                return "Botão PJ não encontrado";
            })()
        """) 
    else:
        raise ValueError("Tipo de certidão inválido. Use 'pf' ou 'pj'.")
    await page.wait(3)


async def preencher_dados_pf(page, cpf, data_nascimento):
    await page.evaluate(f"""
        (() => {{
            const campoCpf = document.querySelector('input[name="niContribuinte"]');
            if (campoCpf) {{
                campoCpf.value = "{cpf}";
                campoCpf.dispatchEvent(new Event('input', {{ bubbles: true }}));
                campoCpf.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}

            const campoData = document.querySelector('input[name="dataNascimento"]');
            if (campoData) {{
                campoData.value = "{data_nascimento}";
                campoData.dispatchEvent(new Event('input', {{ bubbles: true }}));
                campoData.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}

            return "Campos PF preenchidos";
        }})()
    """)
    await page.wait(2)

async def clicar_botao_emitir(page):
    resultado = await page.evaluate("""
        (() => {
            const botoes = Array.from(document.querySelectorAll('button'));
            const botaoEmitir = botoes.find(btn => btn.innerText.includes('Emitir Certidão'));

            if (botaoEmitir) {
                botaoEmitir.click();
                return "Botão Emitir clicado";
            }

            return "Botão Emitir não encontrado";
        })()
    """)
    print(resultado)
    await page.wait(5)

async def verificar_mensagem_erro(page):
    mensagem = await page.evaluate("""
        (() => {
            const bodyText = document.body.innerText;
            if (bodyText.includes('Não foi possível concluir a ação')) {
                return 'Mensagem de erro encontrada na tela.';
            }
            return 'Nenhuma mensagem de erro encontrada.';
        })()
    """)

    print(mensagem)

async def clicar_botao_emitir_validado(page):
    resultado = await page.evaluate("""
        (() => {
            const bodyText = document.body.innerText;

            if (!bodyText.includes('Certidão Válida Encontrada')) {
                return 'Nenhum modal de certidão válida encontrado.';
            }

            const botoes = Array.from(document.querySelectorAll('button'));
            const botaoEmitirNova = botoes.find(btn => btn.innerText.includes('Emitir Nova Certidão'));

            if (botaoEmitirNova) {
                botaoEmitirNova.click();
                return 'Modal encontrado. Botão Emitir Nova Certidão clicado.';
            }

            return 'Modal encontrado, mas botão Emitir Nova Certidão não foi localizado.';
        })()
    """)

    print(resultado)
    await page.wait(5)
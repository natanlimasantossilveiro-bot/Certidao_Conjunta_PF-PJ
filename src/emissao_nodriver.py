import nodriver as nd
import os
import shutil
from pathlib import Path
import time

def listar_pdfs_downloads():
    downloads = Path.home() / "Downloads"
    return set(downloads.glob("*.pdf"))

def mover_certidao_para_pasta(nome_arquivo, pdfs_antes):
    downloads = Path.home() / "Downloads"
    pasta_destino = Path("certidoes_emitidas")
    pasta_destino.mkdir(exist_ok=True)


    arquivo_recente = None

    for tentativa in range(30):
        pdfs_depois = listar_pdfs_downloads()
        novos_pdfs = pdfs_depois - pdfs_antes

        if novos_pdfs:
            arquivo_recente = max(novos_pdfs, key=os.path.getctime)
            print(f"Novo PDF detectado: {arquivo_recente}")
            break

        print(f"Aguardando aparecer novo PDF. Tentativa {tentativa + 1}/30...")
        time.sleep(1)

    if arquivo_recente is None:
        print("Nenhum novo PDF foi encontrado na pasta Downloads após 30 segundos de espera.")
        return None

    novo_caminho = pasta_destino /nome_arquivo
    print(f"Movendo PDF para: {novo_caminho}")

    for tentativa in range(30):
        try:
            
            shutil.move(arquivo_recente, novo_caminho)
            print("PDF movido com sucesso.")
            print(f"Origem: {arquivo_recente}")
            print(f"Destino final: {novo_caminho}")
            return novo_caminho
        except PermissionError:
            print(f"PDF ainda está sendo usado pelo navegador. Tentativa {tentativa + 1}/30...")
            time.sleep(1)

    print("Não foi possível mover o PDF: arquivo ainda em uso.")
    return None


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

async def preencher_dados_pj(page, cnpj):
    await page.evaluate(f"""
        (() => {{
            const campoCnpj = document.querySelector('input[name="niContribuinte"]');

            if (campoCnpj) {{
                campoCnpj.value = "{cnpj}";
                campoCnpj.dispatchEvent(new Event('input', {{ bubbles: true }}));
                campoCnpj.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}

            return "Campos PJ preenchidos";
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

async def verificar_resultado_emissao(page):
    resultado = await page.evaluate("""
        (() => {
            const bodyText = document.body.innerText;

            if (bodyText.includes('Certidão Válida Encontrada')) {
                const botoes = Array.from(document.querySelectorAll('button'));

                const botaoEmitirNova = botoes.find(botao =>
                    botao.innerText.includes('Emitir Nova Certidão')
                );

                if (botaoEmitirNova) {
                    botaoEmitirNova.click();

                    return {
                        status: 'emitindo_nova_certidao',
                        mensagem: 'Certidão válida encontrada. Cliquei em Emitir Nova Certidão.'
                    };
                }

                return {
                    status: 'certidao_valida_sem_botao',
                    mensagem: 'Certidão válida encontrada, mas o botão Emitir Nova Certidão não foi localizado.'
                };
            }

            if (bodyText.includes('Não foi possível concluir a ação')) {
                const linhas = bodyText.split('\\n');
                const linhaErro = linhas.find(linha =>
                    linha.includes('Não foi possível concluir a ação')
                );
                return {
                    status: 'erro_receita',
                    mensagem: linhaErro || 'A Receita Federal retornou uma mensagem de erro.'
                };
            }

            if (bodyText.includes('Certidão emitida')) {
                return {
                    status: 'certidao_emitida',
                    mensagem: 'Certidão aparentemente emitida com sucesso.'
                };
            }

            return {
                status: 'resultado_indefinido',
                mensagem: 'Não foi possível identificar claramente o resultado da emissão.'
            };
        })()
    """)

    print("Retorno bruto: ", resultado)
    print("Tipo do retorno: ", type(resultado))

    if (
        isinstance(resultado, list)
        and len(resultado) > 0
        and isinstance(resultado[0], list)
        and len(resultado[0]) == 2
    ):
        resultado = {
            chave: dados["value"]
            for chave, dados in resultado
        }

    while isinstance(resultado, list):
        resultado = resultado[0]

    if isinstance(resultado, str):
        resultado={
            "status": "retorno_em_texto",
            "mensagem": resultado
        }

    print("Resultado da emissão:")
    print(f"Status: {resultado['status']}")
    print(f"Mensagem: {resultado['mensagem']}")

    await page.wait(2)

    return resultado

async def verificar_pdf_ou_mudanca_pagina(page, url_antes):
    for tentativa in range(10):
        await page.wait(1)

        url_depois = page.url

        if url_depois != url_antes:
            break

    print("Verificando resultado final...")
    print(f"URL antes: {url_antes}")
    print(f"Url depois: {url_depois}")

    if url_depois != url_antes:
        print("A URL mudou após a emissão.")

        if ".pdf" in url_depois.lower():
            print("PDF detectado pela URL.")
            return {
                "status": "pdf_detectado",
                "mensagem": "A certidão parece ter sido aberta em PDF."
            }
        return {
            "status": "url_alterada",
            "mensagem": "A página mudou após a emissão."
        }
    
    print("A URL não mudou. Verificando o conteúdo da página...")
    
    texto_pagina = await page.evaluate("""
        (() => {
            return document.body.innerText;
        })()
    """)

    if "Não foi possível concluir a ação" in str(texto_pagina):
        print("Erro da Receita detectado durante a verificação final.")
        return {
            "status": "erro_receita_tardia",
            "mensagem": "A Receita Federal exibiu mensagem de erro após a emissão."
        }

    if "pdf" in str (texto_pagina).lower():
        print("Possível PDF detectado pelo conteúdo da página.")
        return {
            "status":"possivel_pdf",
            "mensagem": "A página contém referência a PDF."
        }
    print("Nenhuma mudança clara detectada.")
    return {
        "status": "sem_mudanca_clara",
        "mensagem": "A URL não mudou e nenhum PDF foi identificado claramente"
    }

def determinar_status_final(status_emissao, status_pdf):
    if status_emissao in ["emitindo_nova_certidao", "certidao_emitida"]:
        return {
            "status_final": "sucesso_confirmado",
            "mensagem_final": "A emissão foi concluída com forte indicação de sucesso."
        }
    if (
        status_emissao == "resultado_indefinido"
        and status_pdf in ["url_alterada", "pdf_detectado", "possivel_pdf"]
    ):
        return {
            "status_final": "sucesso_provavel",
            "mensagem_final": "A emissão não foi identificada claramente por texto, mas o fluxo avançou normalmente."
        }
    
    if status_emissao == "erro_receita" or status_pdf =="erro_receita_tardia":
        return {
            "status_final": "erro_receita",
            "mensagem_final": "A Receita Federal retornou uma mensagem de erro durante a emissão."
        }
    
    return {
        "status_final": "falha_indefinida",
        "mensagem_final": "Não foi possível confirmar com segurança o resultado final da emissão."
    }

async def processar_certidao(tipo, documento, data_nascimento=""):
    browser, page = await abrir_pagina_receita()
    pdfs_antes = listar_pdfs_downloads()

    try:
        await selecionar_tipo_certidao(page, tipo)

        if tipo == "pf":
            await preencher_dados_pf(page, documento, data_nascimento)

        elif tipo == "pj":
            await preencher_dados_pj(page, documento)

        url_antes = page.url

        await clicar_botao_emitir(page)

        resultado = await verificar_resultado_emissao(page)

        resultado_pdf = await verificar_pdf_ou_mudanca_pagina(page, url_antes)

        caminho_certidao = None

        if resultado_pdf["status"] in ["pdf_detectado", "url_alterada", "possivel_pdf"]:
            nome_pdf = f"Certidao-{documento}.pdf"
            caminho_certidao = mover_certidao_para_pasta(nome_pdf, pdfs_antes)

        resultado_final = determinar_status_final(
            resultado["status"],
            resultado_pdf["status"]
        )

        return {
            "linha_processada": True,
            "tipo": tipo,
            "documento": documento,
            "data_nascimento": data_nascimento,
            "status_emissao": resultado["status"],
            "mensagem_emissao": resultado["mensagem"],
            "status_pdf": resultado_pdf["status"],
            "mensagem_pdf": resultado_pdf["mensagem"],
            "status_final": resultado_final["status_final"],
            "mensagem_final": resultado_final["mensagem_final"],
            "sucesso": resultado_final["status_final"] in [
                "sucesso_confirmado",
                "sucesso_provavel",
            ],

            "arquivo_encontrado": bool(caminho_certidao),
            "caminho_certidao": str(caminho_certidao) if caminho_certidao else "",
        }

    finally:
        try:
            if browser:
                browser.stop()
        except Exception as erro:
            print(f"Aviso ao fechar navegador: {erro}")
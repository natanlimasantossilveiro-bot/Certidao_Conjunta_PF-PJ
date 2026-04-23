import asyncio
import nodriver as nd

async def main():
    browser = await nd.start()
    page = await browser.get("https://servicos.receitafederal.gov.br/servico/certidoes/#/home")

    await page.sleep(3)

    print("Página aberta com sucesso.")

    try:
        input("Pressione Enter para encerrar...")
    finally:
        await browser.stop()

asyncio.run(main())
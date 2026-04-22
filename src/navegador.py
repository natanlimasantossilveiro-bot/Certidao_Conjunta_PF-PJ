import os
from selenium import webdriver

caminho_downloads = r"C:\Automacao_Python\Certidoes_PF_PR\Certidao_Conjunta\downloads"

def abrir_navegador():
    options = webdriver.ChromeOptions()

    prefs = {
        "download.default_directory": caminho_downloads,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    driver.get("https://servicos.receitafederal.gov.br/servico/certidoes/#/home")
    return driver
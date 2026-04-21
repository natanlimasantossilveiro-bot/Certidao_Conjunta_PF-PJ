import os
from selenium import webdriver

caminho_downloads = r"C:\Automacao_Python\Certidoes_PF_PR\Certidao_Conjunta\downloads"

options = webdriver.ChromeOptions()

prefs = {
    "download.default_directory": caminho_downloads,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}

options.add_experimental_option("prefs", prefs)

def abrir_navegador():
    driver = webdriver.Chrome(options=options)
    driver.get("https://servicos.receitafederal.gov.br/servico/certidoes/#/home")
    return driver
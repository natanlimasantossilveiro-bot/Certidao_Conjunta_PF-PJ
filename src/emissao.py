from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clicar_botao_aceitar_cookies(driver):
        wait = WebDriverWait(driver, 10)

        try:
                botao_aceitar_cookies = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Aceitar"]'))
                )
                botao_aceitar_cookies.click()
        except Exception:
                print("Botão de aceitar cookies não encontrado ou já foi aceito.")

def selecionar_tipo_certidao(driver, tipo):
        wait = WebDriverWait(driver, 10)

        if tipo.lower() == "pf":
                botao = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#/home/cpf"]'))
                )
                botao.click()
        elif tipo.lower() == "pj":
                botao = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#/home/cnpj"]'))
                )
                botao.click()
        else:
                raise ValueError("Tipo inválido. Use 'pf' ou 'pj'.")
        
def preencher_dados_pf(driver, cpf, data_nascimento):
        wait = WebDriverWait(driver, 10)

        campo_cpf = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="niContribuinte"][placeholder="Informe o CPF"]'))
        )
        campo_cpf.send_keys(cpf)

        campo_data = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="dataNascimento"][placeholder="Informe a data de nascimento"]'))
        )
        campo_data.send_keys(data_nascimento)

def preencher_dados_pj(driver, cnpj):
        wait = WebDriverWait(driver, 10)

        campo_cnpj = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="niContribuinte"][placeholder="Informe o CNPJ"]'))
        )
        campo_cnpj.send_keys(cnpj)


def clicar_botao_emitir(driver):
        wait = WebDriverWait(driver, 10)

        botao_emitir = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"].btn-acao-3'))
        )
        botao_emitir.click()
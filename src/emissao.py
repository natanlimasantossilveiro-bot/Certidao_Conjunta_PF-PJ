import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
        
def digitar_devagar(campo, texto, intervalo=0.15):
        for caractere in texto:
                campo.send_keys(caractere)
                time.sleep(intervalo)
        
def preencher_dados_pf(driver, cpf, data_nascimento):
        wait = WebDriverWait(driver, 10)

        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) == 11:
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        campo_cpf = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="niContribuinte"][placeholder="Informe o CPF"]'))
        )
        campo_cpf.click()
        campo_cpf.clear()
        time.sleep(0.5)
        digitar_devagar(campo_cpf, cpf)
        time.sleep(0.5)
        campo_cpf.send_keys(Keys.TAB)
        time.sleep(0.5)

        campo_data = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="dataNascimento"][placeholder="Informe a data de nascimento"]'))
        )
        campo_data.click()
        campo_data.clear()
        time.sleep(0.5)
        digitar_devagar(campo_data, data_nascimento)
        time.sleep(0.5)
        campo_data.send_keys(Keys.TAB)
        time.sleep(2)

def preencher_dados_pj(driver, cnpj):
        wait = WebDriverWait(driver, 10)

        campo_cnpj = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="niContribuinte"][placeholder="Informe o CNPJ"]'))
        )
        campo_cnpj.click()
        campo_cnpj.clear()
        time.sleep(0.5)
        campo_cnpj.send_keys(cnpj)
        time.sleep(0.5)
        campo_cnpj.send_keys(Keys.TAB)
        time.sleep(2)


def clicar_botao_emitir(driver):
        wait = WebDriverWait(driver, 15)

        botao_emitir = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"].btn-acao-3'))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_emitir)
        time.sleep(1)

        try:
                ActionChains(driver).move_to_element(botao_emitir).pause(0.5).click().perform()
                print("Tentativa de clique com ActionChains realizada.")
        except Exception:
                try:
                        botao_emitir.click()
                        print("Tentativa de clique normal realizada.")
                except Exception:
                        driver.execute_script("arguments[0].click();", botao_emitir)
                        print("Tentativa de clique com JavaScript realizada.")
        time.sleep(5)

        try:
                mensagem_erro = driver.find_element(By.XPATH, "//*[contains(text(), 'Não foi possível concluir a ação')]")
                print(f"Mensagem de erro encontrada: {mensagem_erro.text}")
        except Exception:
                print("Nenhuma mensagem de erro encontrada após o clique.")
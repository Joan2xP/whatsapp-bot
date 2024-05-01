import re
from playwright.sync_api import Playwright, sync_playwright, expect

class User:
    def __init__(self, name, phone) -> None:
        self.name = name
        self.phone = phone
    

def generate_data():
    data = []

    data.append(User("carles", "+34 640 33 19 78"))
    data.append(User("Abril", "+34 640 51 88 65"))

    return data



    

USERS_DATA = generate_data()

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.whatsapp.com/")
    
    contacto = page.get_by_role("textbox", name="Cuadro de texto para ingresar")
    expect(contacto).to_be_visible(timeout=100000)
    
    user: User
    for user in USERS_DATA:
        contacto.fill(user.name)
        page.keyboard.down('Enter')
        page.get_by_title('Adjuntar').click()

        page.query_selector("div[role=application] ul div:nth-child(2) li input[type=file]").set_input_files("/home/joanpp/Downloads/donde-dejar-exhibidores.jpg")
        
        enviar = page.locator("div[aria-label=Enviar]")
        enviar.wait_for()
        enviar.click()
        page.wait_for_timeout(2000)

  


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

from playwright.sync_api import Playwright, sync_playwright, expect
import re


def run(playwright: Playwright, data: list[dict[str,str]]) -> None:
    """Send messages to the users in the data list the data has the following structure:
    [
        {
            'image_path': 'path/to/image',
            'phones': ['phone1', 'phone2',...]
        },
        ...
    ]
    """
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.whatsapp.com/")
    
    contacto = page.get_by_role("textbox", name="Cuadro de texto para ingresar")
    expect(contacto).to_be_visible(timeout=100000)
    div_search_pattern = re.compile("^Buscar$")
    div_search = page.get_by_text(div_search_pattern)

    
    
    for message in data:
        phones = message['phones']
        image_path = message['image_path']
        for phone in phones:
            contacto.fill(phone)
            page.keyboard.down('Enter')
            page.get_by_title('Adjuntar').click()

            page.query_selector("div[role=application] ul div:nth-child(2) li input[type=file]").set_input_files(image_path)
            
            enviar = page.locator("div[aria-label=Enviar]")
            enviar.click()      
            
            expect(div_search).to_contain_text(div_search_pattern)

    # ---------------------
    context.close()
    browser.close()

def exec(messages):
    with sync_playwright() as playwright:
        run(playwright, messages) 

if __name__ == "__main__":
    pass
    # mock_messages = [{"image_path": "output_10.png", "phones": ["12345678", "12345679"]},
    #                  {"image_path": "output_11.png", "phones": ["12345678", "12345679"]},
    #                  {"image_path": "output_12.png", "phones": ["12345678", "12345679"]},
    #                  {"image_path": "output_13.png", "phones": ["12345678", "12345679"]}]
    # exec(mock_messages)
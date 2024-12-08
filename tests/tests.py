from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import random
import json
import time
import os

MAIN_PAGE_URL = "https://localhost:8443"
CART_URL = "https://localhost:8443/koszyk?action=show"

download_dir = os.path.abspath('./DownloadsFolder')
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False
}

options = Options()
options.add_argument('--ignore-certificate-errors')
options.page_load_strategy = 'eager'
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.set_window_position(0, 0)
driver.maximize_window()
actions = ActionChains(driver)

wait = WebDriverWait(driver, 20)


def parse_product_list(data):
    products = json.loads(data)
    product_dict = {product['name']: product['quantity'] for product in products}

    return product_dict


def search_product(name):
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.ui-autocomplete-input")))
    search_input.send_keys(name)
    time.sleep(0.4)

    first_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-corner-all")))
    first_result.click()
    time.sleep(0.4)


def add_products(json_file_path):
    driver.get(MAIN_PAGE_URL)

    with open(json_file_path, 'r') as file:
        data = file.read()
        products = parse_product_list(data)

    for product_name, quantity in products.items():
        search_product(product_name)

        opis_element = driver.find_element(By.XPATH, "//a[contains(., 'Opis')]")
        actions.move_to_element(opis_element).perform()

        time.sleep(1)

        quantity_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn-touchspin:nth-child(1)")))

        for _ in range(quantity - 1):
            quantity_input.click()
            time.sleep(0.4)

        add_to_cart_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart")))
        add_to_cart_button.click()
        time.sleep(0.4)

        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close")))
        close_button.click()
        time.sleep(0.4)


def add_random_products(name):
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.ui-autocomplete-input")))
    search_input.clear()
    search_input.send_keys(name)
    time.sleep(0.4)

    search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ui-corner-all span")))
    random_result = random.choice(search_results)
    random_result.click()
    time.sleep(0.4)

    add_to_cart_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart")))
    add_to_cart_button.click()
    time.sleep(0.4)

    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close")))
    close_button.click()
    time.sleep(0.4)


def remove_from_cart(amount):
    driver.get(CART_URL)

    cart_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.cart-items li.cart-item")))

    for i in range(amount):
        remove_button = cart_items[i].find_element(By.CSS_SELECTOR, "a.remove-from-cart")
        remove_button.click()
        time.sleep(0.4)

        wait.until(EC.staleness_of(cart_items[i]))

        cart_items = driver.find_elements(By.CSS_SELECTOR, "ul.cart-items li.cart-item")


def register_user():
    driver.get(MAIN_PAGE_URL)
    user_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.user-info > a")))
    user_button.click()
    time.sleep(0.4)

    register_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.no-account > a")))
    register_button.click()
    time.sleep(0.4)

    fill_registration()
    time.sleep(0.4)


def fill_registration():
    gender_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='field-id_gender-1']")))
    gender_button.click()
    time.sleep(0.4)

    textbox_name = wait.until(EC.presence_of_element_located((By.ID, "field-firstname")))
    textbox_name.send_keys("Name")
    time.sleep(0.4)

    textbox_surname = wait.until(EC.presence_of_element_located((By.ID, "field-lastname")))
    textbox_surname.send_keys("Surname")
    time.sleep(0.4)

    textbox_mail = wait.until(EC.presence_of_element_located((By.ID, "field-email")))
    textbox_mail.send_keys("emaiil@email.com")
    time.sleep(0.4)

    textbox_password = wait.until(EC.presence_of_element_located((By.ID, "field-password")))
    textbox_password.send_keys("password")
    time.sleep(0.4)

    textbox_birthday = wait.until(EC.presence_of_element_located((By.ID, "field-birthday")))
    textbox_birthday.send_keys("2000-01-01")
    time.sleep(0.4)

    checkbox_offer = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Otrzymuj oferty od naszych partnerów')]")))
    checkbox_offer.click()
    time.sleep(0.4)

    checkbox_personal_data = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Wiadomość o przetwarzaniu danych osobowych')]")))
    checkbox_personal_data.click()
    time.sleep(0.4)

    checkbox_newsletter = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Zapisz się do newslettera')]")))
    checkbox_newsletter.click()
    time.sleep(0.4)

    checkbox_policy = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[contains(., 'Zgadzam się z regulaminem i polityką prywatności')]")))
    checkbox_policy.click()
    time.sleep(0.4)

    save_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.form-control-submit.float-xs-right")))
    save_button.click()


def order():
    start_order()
    fill_address()
    choose_delivery_method()
    choose_payment_method_and_finalize()


def start_order():
    driver.get(CART_URL)
    finialize_order_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary")))
    finialize_order_button.click()
    time.sleep(0.4)


def fill_address():
    texbox_adress = wait.until(EC.element_to_be_clickable((By.ID, "field-address1")))
    texbox_adress.send_keys("adres")
    time.sleep(0.4)

    textbox_postcode = wait.until(EC.presence_of_element_located((By.ID, "field-postcode")))
    textbox_postcode.send_keys("00-000")
    time.sleep(0.4)

    textbox_city = wait.until(EC.presence_of_element_located((By.ID, "field-city")))
    textbox_city.send_keys("Gdansk")
    time.sleep(0.4)

    textbox_phone = wait.until(EC.presence_of_element_located((By.ID, "field-phone")))
    textbox_phone.send_keys("000000000")
    time.sleep(0.4)

    continue_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "footer.form-footer.clearfix > button.continue.btn.btn-primary.float-xs-right")))
    continue_button.click()
    time.sleep(0.4)


def choose_delivery_method():
    delivery_method_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='delivery_option_9']")))
    delivery_method_button.click()
    time.sleep(0.4)

    continue_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "form.clearfix > button.continue.btn.btn-primary.float-xs-right")))
    continue_button.click()
    time.sleep(0.4)


def choose_payment_method_and_finalize():
    payment_method_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='payment-option-2']")))
    payment_method_option.click()
    time.sleep(0.4)

    checkbox_terms = wait.until(EC.presence_of_element_located((By.ID, "conditions_to_approve[terms-and-conditions]")))
    checkbox_terms.click()
    time.sleep(0.4)

    continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary.center-block')))
    continue_button.click()
    time.sleep(0.4)


def check_order_status():
    my_account_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.user-info > a.account')))
    my_account_button.click()
    time.sleep(0.4)

    history_button = wait.until(EC.element_to_be_clickable((By.ID, 'history-link')))
    history_button.click()
    time.sleep(0.4)

    order_status = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody > tr > td > span.label.label-pill.bright')))

    try:
        assert order_status.text.strip() == "Oczekiwanie na płatność przy odbiorze"
    except AssertionError:
        print(f"Test failed: Expected 'Oczekiwanie na płatność przy odbiorze' but got '{order_status.text.strip()}'")


def get_invoice():
    invoice_download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'tbody > tr > td.text-sm-center.hidden-md-down > a > i.material-icons')))
    invoice_download_button.click()
    time.sleep(5)

    files = [f for f in os.listdir(download_dir) if f.startswith("FV") and f.endswith(".pdf")]
    try:
        assert len(files) != 0
    except AssertionError:
        print("Invoice download failed")
        return

    # remove file after test
    file_path = os.path.join(download_dir, files[0])
    #os.remove(file_path)


def run_tests():
    relative_path = "./products_to_add_to_cart.json"
    absolute_path = os.path.abspath(relative_path)
    add_products(absolute_path)
    add_random_products("Joy")
    remove_from_cart(3)
    register_user()
    order()
    check_order_status()
    get_invoice()


if __name__ == "__main__":
    start_time = time.time()
    run_tests()
    print("--- %s seconds ---" % (time.time() - start_time))
    driver.quit()

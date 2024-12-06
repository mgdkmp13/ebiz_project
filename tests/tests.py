from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import time  # Importujemy moduł time do dodania opóźnień
import json
import time
import os

MAIN_PAGE_URL = "https://localhost:8443"  # Poprawny adres URL
CART_URL = "https://localhost:8443/koszyk?action=show"

# Konfiguracja opcji przeglądarki
options = Options()
options.add_argument('--ignore-certificate-errors')  # Ignoruj błędy certyfikatu
options.add_argument('--no-sandbox')  # Opcjonalnie, jeśli masz problemy z uruchomieniem
options.add_argument('--disable-gpu')

# Upewnij się, że chromedriver znajduje się w PATH lub podaj pełną ścieżkę
driver = webdriver.Chrome(options=options)
driver.get(MAIN_PAGE_URL)
wait = WebDriverWait(driver, 10)

def parse_product_list(data):
    # Konwertowanie JSON na listę słowników
    products = json.loads(data)
    
    # Tworzymy słownik, w którym kluczem jest nazwa produktu, a wartością jego ilość
    product_dict = {product['name']: product['quantity'] for product in products}
    
    return product_dict


def testTests():
    try:
        # Poczekaj na załadowanie elementów z klasą "thumbnail product-thumbnail"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.thumbnail.product-thumbnail"))
        )

        # Znajdź pierwszy element i kliknij
        product_link = driver.find_element(By.CSS_SELECTOR, "a.thumbnail.product-thumbnail")
        product_link.click()

        print("Przeniesiono na stronę produktu.")
        time.sleep(2)  # Opóźnienie 2 sekundy

        # Poczekaj, aż załaduje się przycisk "Add to Cart"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart")))

        # Kliknij przycisk dodania do koszyka
        add_to_cart_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart")
        add_to_cart_button.click()

        print("Dodano produkt do koszyka.")
        time.sleep(2)  # Opóźnienie 2 sekundy

        # Poczekaj na pojawienie się powiadomienia o dodaniu do koszyka i kliknij przycisk zamknięcia
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close"))
        )
        close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
        close_button.click()

        print("Zamknięto powiadomienie o dodaniu do koszyka.")
        time.sleep(2)  # Opóźnienie 2 sekundy

        # Kliknij przycisk przejścia do koszyka
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='//localhost:8443/koszyk?action=show']"))
        )
        cart_button = driver.find_element(By.CSS_SELECTOR, "a[href='//localhost:8443/koszyk?action=show']")
        cart_button.click()

        print("Przeniesiono do koszyka.")
        time.sleep(2)  # Opóźnienie 2 sekundy

        # Poczekaj na załadowanie listy produktów w koszyku
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.cart-items li.cart-item"))
        )

        # Sprawdź, ile jest produktów w koszyku
        cart_items = driver.find_elements(By.CSS_SELECTOR, "ul.cart-items li.cart-item")
        print(f"Liczba produktów w koszyku: {len(cart_items)}")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

        


def search_product(name):
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.ui-autocomplete-input"))
        )

        # Znajdź pole wyszukiwania i wpisz nazwę produktu
        search_input = driver.find_element(By.CSS_SELECTOR, "input.ui-autocomplete-input")
        search_input.send_keys(name)
        
        # Poczekaj, aż pojawią się wyniki i kliknij w pierwsze wystąpienie
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-corner-all"))
        )
        first_result = driver.find_element(By.CSS_SELECTOR, "a.ui-corner-all")
        first_result.click()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")


def random_search_choose_add_check_cart(name):
    try:
        # Oczekiwanie na obecność pola wyszukiwania
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.ui-autocomplete-input"))
        )

        # Znajdź pole wyszukiwania i wpisz nazwę produktu
        search_input = driver.find_element(By.CSS_SELECTOR, "input.ui-autocomplete-input")
        search_input.clear()  # Upewnij się, że pole jest puste
        search_input.send_keys(name)

        # Poczekaj na załadowanie wyników wyszukiwania
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ui-corner-all span"))
        )

        # Pobierz wszystkie wyniki wyszukiwania
        search_results = driver.find_elements(By.CSS_SELECTOR, "a.ui-corner-all")

        if not search_results:
            print(f"Brak wyników wyszukiwania dla: {name}")
            return

        # Wybierz losowy wynik z listy
        random_result = random.choice(search_results)
        product_name = random_result.find_element(By.CSS_SELECTOR, "span").text.strip()
        print(f"Wybrano losowy produkt: {product_name}")

        # Przejdź na stronę wybranego produktu
        random_result.click()

        # Poczekaj na załadowanie strony produktu
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart"))
        )

        # Dodaj produkt do koszyka
        add_to_cart_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart")
        add_to_cart_button.click()
        print(f"Dodano {product_name} do koszyka.")

        # Zamknij powiadomienie o dodaniu produktu do koszyka
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close"))
        )
        close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
        close_button.click()
        print(f"Zamknięto powiadomienie o dodaniu {product_name} do koszyka.")

        # Przejdź do koszyka
        driver.get(CART_URL)
        print("Przeniesiono do koszyka.")

        # Poczekaj na załadowanie produktów w koszyku
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.cart-items li.cart-item"))
        )

        # Pobierz produkty z koszyka
        cart_items = driver.find_elements(By.CSS_SELECTOR, "ul.cart-items li.cart-item")
        found = False

        for item in cart_items:
            item_name = item.find_element(By.CSS_SELECTOR, "a.label").text.strip()
            if item_name == product_name:
                print(f"Produkt {product_name} znajduje się w koszyku.")
                found = True
                break

        if not found:
            print(f"Produkt {product_name} NIE został znaleziony w koszyku.")

    except Exception as e:
        print(f"Wystąpił błąd podczas wyszukiwania losowego produktu: {e}")



def add_products_from_json_to_cart(json_file_path):
    driver.get(MAIN_PAGE_URL)
    try:
        # Odczytaj dane z pliku JSON
        with open(json_file_path, 'r') as file:
            data = file.read()
            products = parse_product_list(data)

        # Iteruj po produktach i dodawaj je do koszyka
        for product_name, quantity in products.items():
            print(f"Szukanie produktu: {product_name}")
            search_product(product_name)  # Wyszukaj produkt

            # Ustaw ilość produktu przed dodaniem do koszyka
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-touchspin:nth-child(1)"))
            )
            quantity_input = driver.find_element(By.CSS_SELECTOR, "button.btn-touchspin:nth-child(1)")
            for _ in range(quantity - 1):
                quantity_input.click()
            print(f"Ustawiono ilość {quantity} dla produktu {product_name}.")


            # Dodaj produkt do koszyka
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart"))
            )
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart")
            add_to_cart_button.click()
            print(f"Dodano {product_name} do koszyka.")

            # Poczekaj na powiadomienie o dodaniu do koszyka i zamknij je
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close"))
            )
            close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
            close_button.click()
            print(f"Zamknięto powiadomienie o dodaniu {product_name} do koszyka.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def verify_cart_contents(json_file_path):
    try:
        # Odczytaj dane z pliku JSON
        with open(json_file_path, 'r') as file:
            data = file.read()
            expected_products = parse_product_list(data)

        driver.get(CART_URL)

        # Znajdź wszystkie produkty w koszyku
        cart_items = driver.find_elements(By.CSS_SELECTOR, "ul.cart-items li.cart-item")

        # Iteruj po produktach z koszyka i sprawdzaj ich zgodność
        for item in cart_items:
            # Pobierz nazwę produktu
            product_name_element = item.find_element(By.CSS_SELECTOR, "a.label:nth-child(1)")
            product_name = product_name_element.text.strip()

            # Pobierz ilość produktu
            quantity_element = item.find_element(By.CSS_SELECTOR, "input.js-cart-line-product-quantity")
            actual_quantity = int(quantity_element.get_attribute("value"))

            # Sprawdź, czy produkt znajduje się w oczekiwanej liście
            if product_name in expected_products:
                expected_quantity = expected_products[product_name]
                if actual_quantity == expected_quantity:
                    print(f"Produkt {product_name} ma poprawną ilość: {actual_quantity}.")
                else:
                    print(f"BŁĄD: Produkt {product_name} ma niezgodną ilość. Oczekiwano {expected_quantity}, a znaleziono {actual_quantity}.")
            else:
                print(f"BŁĄD: Produkt {product_name} nie powinien znajdować się w koszyku.")

        # Sprawdź, czy w koszyku nie ma dodatkowych produktów
        expected_names = set(expected_products.keys())
        actual_names = {item.find_element(By.CSS_SELECTOR, "a.label:nth-child(1)").text.strip() for item in cart_items}

        extra_items = actual_names - expected_names
        if extra_items:
            print(f"BŁĄD: Znaleziono dodatkowe produkty w koszyku: {', '.join(extra_items)}.")
        else:
            print("Koszyk zawiera dokładnie oczekiwane produkty.")

    except Exception as e:
        print(f"Wystąpił błąd podczas weryfikacji koszyka: {e}")

def remove_from_cart(amount):
    try:
        # Przejdź do koszyka
        driver.get(CART_URL)
        print("Przeniesiono do koszyka.")

        # Poczekaj na załadowanie produktów w koszyku
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.cart-items li.cart-item"))
        )

        # Pobierz listę produktów w koszyku
        cart_items = driver.find_elements(By.CSS_SELECTOR, "ul.cart-items li.cart-item")

        # Sprawdź, czy liczba produktów w koszyku jest wystarczająca
        if len(cart_items) < amount:
            print(f"W koszyku jest tylko {len(cart_items)} przedmiotów. Nie można usunąć {amount}.")
            return

        # Usuń pierwsze 'amount' produktów
        for i in range(amount):
            product_name = cart_items[i].find_element(By.CSS_SELECTOR, "a.label").text.strip()
            print(f"Usuwanie produktu: {product_name}")

            # Znajdź i kliknij przycisk usuwania
            remove_button = cart_items[i].find_element(By.CSS_SELECTOR, "a.remove-from-cart")
            remove_button.click()

            # Poczekaj na odświeżenie koszyka po usunięciu produktu
            wait.until(
                EC.staleness_of(cart_items[i])
            )
            print(f"Produkt {product_name} został usunięty.")

            # Zaktualizuj listę produktów w koszyku
            cart_items = driver.find_elements(By.CSS_SELECTOR, "ul.cart-items li.cart-item")

        print(f"Usunięto {amount} produktów z koszyka.")

    except Exception as e:
        print(f"Wystąpił błąd podczas usuwania produktów z koszyka: {e}")




def add_products_and_check_cart(json_file_path):
    add_products_from_json_to_cart(json_file_path)
    verify_cart_contents(json_file_path)



def run_tests():
    relative_path = "./products_to_add_to_cart.json"
    absolute_path = os.path.abspath(relative_path)
    add_products_and_check_cart(absolute_path)
    random_search_choose_add_check_cart("Joy")
    remove_from_cart(3)


if __name__ == "__main__":
    start_time = time.time()
    run_tests()
    print("--- %s seconds ---" % (time.time() - start_time))
    driver.quit()
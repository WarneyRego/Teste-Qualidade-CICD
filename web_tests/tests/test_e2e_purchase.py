from web_tests.pages.login_page import LoginPage
from web_tests.pages.inventory_page import InventoryPage
from web_tests.pages.cart_page import CartPage
from web_tests.pages.checkout_page import CheckoutPage

USERNAME = "standard_user"
PASSWORD = "secret_sauce"

ITEMS_TO_BUY = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
]


def test_complete_purchase_flow(driver):
    # Login
    print(f"[1] Abrindo https://www.saucedemo.com")
    login_page = LoginPage(driver)
    login_page.open()

    print(f"[2] Realizando login com usuário '{USERNAME}'")
    login_page.login(USERNAME, PASSWORD)

    inventory_page = InventoryPage(driver)
    title = inventory_page.get_page_title()
    print(f"[3] Página carregada: '{title}'")
    assert title == "Products"

    # Adicionar produtos
    for item in ITEMS_TO_BUY:
        inventory_page.add_item_to_cart(item)
        print(f"[4] Produto adicionado ao carrinho: '{item}'")

    count = inventory_page.get_cart_item_count()
    print(f"[5] Itens no carrinho: {count}")
    assert count == len(ITEMS_TO_BUY)

    # Ir ao carrinho
    print(f"[6] Navegando para o carrinho")
    inventory_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_items = cart_page.get_item_names()
    print(f"[7] Itens encontrados no carrinho: {cart_items}")
    assert cart_page.get_item_count() == len(ITEMS_TO_BUY)
    for item in ITEMS_TO_BUY:
        assert item in cart_items

    # Checkout
    print(f"[8] Iniciando checkout")
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    print(f"[9] Preenchendo dados do cliente: John Doe, CEP 12345")
    checkout_page.fill_customer_info("John", "Doe", "12345")

    total_label = checkout_page.get_item_total_label()
    print(f"[10] Resumo do pedido: '{total_label}'")
    assert "Item total:" in total_label

    print(f"[11] Finalizando compra")
    checkout_page.finish_order()

    header = checkout_page.get_confirmation_header()
    text   = checkout_page.get_confirmation_text()
    print(f"[12] Confirmação: '{header}'")
    print(f"[13] Mensagem: '{text}'")

    assert header == "Thank you for your order!"
    assert "dispatched" in text.lower()

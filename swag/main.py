import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


# Функция ожидания элементов
def wait_of_element_located(xpath, driver_init):
    element = WebDriverWait(driver_init, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return element


# Инициализция драйвера
@pytest.fixture
def driver_init():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        options=options, executable_path=r"/Users/marathon/Desktop/study/testing/swag/chromedriver"
    )
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.close()


# Аутентификация юзера
def auth_user(user_name, password, driver_init):
    # Поиск и ожидание элементов и присваивание к переменным.
    input_username = wait_of_element_located(xpath='//*[@id="user-name"]', driver_init=driver_init)
    input_password = wait_of_element_located(xpath='//*[@id="password"]', driver_init=driver_init)
    login_button = wait_of_element_located(xpath='//*[@id="login-button"]', driver_init=driver_init)

    # Действия с формами
    input_username.send_keys(user_name)
    input_password.send_keys(password)
    login_button.send_keys(Keys.RETURN)


def add_item_to_cart(xpath_item, driver_init):
    # Поиск и ожидание прогрузки ссылки элемента товара магазина и клик по ссылке
    item_name = wait_of_element_located(xpath=xpath_item, driver_init=driver_init)
    item_name.click()

    # Поиск и ожидание кнопки добавления товара и клик по этой кнопке
    item_add_button = wait_of_element_located(
        xpath='//*[@id="add-to-cart-sauce-labs-fleece-jacket"]', driver_init=driver_init
    )
    item_add_button.click()

    # Ждем пока товар добавится в корзину, появится span(кол-во позиций в корзине)
    # Возвращаем True или False в зависимости добавился товар или нет
    shop_cart_with_item = wait_of_element_located(
        xpath='//*[@id="shopping_cart_container"]/a/span', driver_init=driver_init
    )
    return shop_cart_with_item


def test_add_jacket_to_the_shopcart(driver_init):
    # Аутентификация пользователя
    auth_user("standard_user", "secret_sauce", driver_init=driver_init)

    # Добавление товара в корзину и если товар добавлен переход в корзину
    add_item_to_cart(xpath_item='//*[@id="item_5_title_link"]/div', driver_init=driver_init).click()
    # Поиск корзины и клик
    wait_of_element_located(xpath='//*[@id="shopping_cart_container"]/a', driver_init=driver_init).click()

    # Поиск ссылки элемента позиции магазина
    item_name = wait_of_element_located(xpath='//*[@id="item_5_title_link"]/div', driver_init=driver_init)

    # Поиск описания товара
    item_description = wait_of_element_located(
        xpath='//*[@id="cart_contents_container"]/div/div[1]/div[3]/div[2]/div[1]', driver_init=driver_init
    )

    # Проверка что товар с таким описанием добавлен в корзину
    assert item_name.text == "Sauce Labs Fleece Jacket"
    assert (
        item_description.text == "It's not every day that you come across a midweight quarter-zip fleece jacket"
        " capable of handling everything from a relaxing day outdoors to a busy day at "
        "the office."
    )


def test_remove_jacket_from_the_shopcart(driver_init):
    # Аутентификация пользователя
    auth_user("standard_user", "secret_sauce", driver_init=driver_init)

    # Добавление товара в корзину и если товар добавлен переход в корзину
    add_item_to_cart(xpath_item='//*[@id="item_5_title_link"]/div', driver_init=driver_init).click()

    # Поиск корзины и клик
    wait_of_element_located(xpath='//*[@id="shopping_cart_container"]/a', driver_init=driver_init).click()

    # Проверка что длина корзина равна 1
    assert (
        len(driver_init.find_elements(
            by=By.XPATH, value='//*[@id="cart_contents_container"]/div/div[1]'
        )) == 1
    )
    # Поиск удаления товара и клик
    wait_of_element_located(
        xpath='//*[@id="remove-sauce-labs-fleece-jacket"]', driver_init=driver_init
    ).click()

    # Поиск корзины и клик
    wait_of_element_located(
        xpath='//*[@id="shopping_cart_container"]/a', driver_init=driver_init
    ).click()

    # Поиск ссылки удалённого из корзины элемента
    try:
        driver_init.find_element(
                by=By.XPATH, value='//*[@id="item_5_title_link"]/div'
            )
    except Exception as e:
        assert isinstance(e, NoSuchElementException)


if __name__ == "__main__":
    test_add_jacket_to_the_shopcart(driver_init=driver_init)
    test_remove_jacket_from_the_shopcart(driver_init=driver_init)
    

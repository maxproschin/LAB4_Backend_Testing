from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Налаштування драйвера
options = webdriver.ChromeOptions()
# options.add_argument("--headless") # Розкоментуй, якщо не хочеш, щоб вікно реально відкривалося
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("Запуск браузера...")
    # 1. Відкриваємо сторінку логіну
    driver.get("http://localhost:3000/login")
    time.sleep(2)

    # 2. Авторизація (вводимо дані в інпути)
    # Переконайся, що на сторінці Login є input type="email" та "password"
    email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

    email_input.send_keys("test@test.com")
    pass_input.send_keys("123456")

    # Шукаємо кнопку Sign In і тиснемо
    login_button = driver.find_element(By.TAG_NAME, "button")
    login_button.click()

    print("Логін виконано, чекаємо завантаження головної...")
    time.sleep(3)

    # 3. Скрапінг даних з головної сторінки
    # Шукаємо всі заголовки постів (теги h2, які ми робили в минулій лабі)
    titles = driver.find_elements(By.TAG_NAME, "h2")

    print("\n--- ЗІБРАНІ ДАНІ З САЙТУ ---")
    if not titles:
        print("Заголовків не знайдено. Можливо, пости ще не завантажились?")
    else:
        for i, title in enumerate(titles, 1):
            print(f"{i}. Пост: {title.text}")
    print("---------------------------\n")

finally:
    time.sleep(2)
    driver.quit()
    print("Браузер закрито.")
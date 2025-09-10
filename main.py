import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def search_bike(driver, query="bike"):
    driver.get('https://www.zoom.com.br/')
    search = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'SearchInput_Input__W2vzU'))
    )
    search.clear()
    search.send_keys(query)
    search.send_keys(Keys.ENTER)


def change_sort(driver, option_text):
    sort_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select[data-testid="select-order-by"]'))
    )
    select = Select(sort_select)
    select.select_by_visible_text(option_text)
    sleep(2)


def scrape_pages(driver, pages=2):
    items = []
    for page in range(pages):
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="product-card"]'))
        )
        produtos = driver.find_elements(By.CSS_SELECTOR, '[data-testid="product-card"]')
        for produto in produtos:
            try:
                titulo = produto.find_element(By.CSS_SELECTOR, '[data-testid="product-card::name"]').text
                link = produto.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                items.append({'titulo': titulo, 'link': link})
            except:
                pass

        try:
            next_li = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="page-next"]')
            next_a = next_li.find_element(By.TAG_NAME, 'a')
            href = next_a.get_attribute("href")
            driver.get(href)
            sleep(2)
        except:
            break
    return items

def extract_specs(driver, url):
    driver.get(url)
    sleep(2)
    specs = {}
    try:
        spec_rows = driver.find_elements(By.CSS_SELECTOR, '[data-testid="attribute"]')
        for row in spec_rows:
            try:
                key = row.find_element(By.CSS_SELECTOR, 'dt').text
                val = row.find_element(By.CSS_SELECTOR, 'dd').text
                specs[key] = val
            except:
                continue
    except:
        pass
    return specs

driver = webdriver.Edge()

search_bike(driver, "bike")
result_default = scrape_pages(driver, 2)

search_bike(driver, "bike")
change_sort(driver, "Melhor avaliado")
result_best = scrape_pages(driver, 2)

search_bike(driver, "bike")
change_sort(driver, "Menor preço")
result_price = scrape_pages(driver, 2)

# --- Ranking ---
df = pd.DataFrame(result_default + result_best + result_price)
ranking = df.groupby(["titulo","link"]).size().reset_index(name="aparicoes")
ranking = ranking.sort_values("aparicoes", ascending=False)
print(ranking.head(10))

# Top 5
top5 = ranking.head(5)

all_specs = []
for _, row in top5.iterrows():
    specs = extract_specs(driver, row["link"])
    specs["titulo"] = row["titulo"]
    specs["link"] = row["link"]
    specs["aparicoes"] = row["aparicoes"]
    all_specs.append(specs)

pd.DataFrame(all_specs).to_csv("bikes_top5.csv", index=False, encoding="utf-8-sig")
print("Arquivo salvo: bikes_top5.csv")

driver.quit()

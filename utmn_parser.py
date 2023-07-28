from selenium.webdriver.common.by import By

from webdriver import *


FAST_MODE = 1
TABLE_MODE = 2
TR_MODE = 3

MODE = TR_MODE
driver = login_driver("https://ratings.utmn.ru/")
path = "utmn/"


def load_section(sect):
    fname = (path + sect.text + ".csv").replace(":", "_")
    print(fname)
    f = open(fname, "w", encoding="utf-8")
    sect.click()
    sleep(1)
    fields = driver.find_elements(By.CLASS_NAME, "q-field")
    fields[2].click()  # категори приема
    sleep(0.2)
    for el in driver.find_elements(By.CLASS_NAME, "q-item"):
        if el.text == "На общих основаниях":
            el.click()
    sleep(0.5)
    fields[5].click()  # основание поступления
    sleep(0.2)
    # driver.find_element(By.XPATH, r'//*[@id="raitings"]/div/section[2]/div[1]/div[2]/div[6]/label').click()
    for el in driver.find_elements(By.CLASS_NAME, "q-item"):
        if el.text == "Бюджетная основа":
            el.click()

    sleep(1)
    head = driver.find_element(By.XPATH, r'//*[@id="raitings"]/div/section[2]/div[2]/table/thead/tr')
    table = driver.find_element(By.XPATH, '//*[@id="raitings"]/div/section[2]/div[2]/table')
    print()
    headers = ";".join([th.text for th in head.find_elements(By.TAG_NAME, "th")]) + ";\n"
    f.write(headers)
    cnt_columns = len(headers)
    if MODE == FAST_MODE:
        text = table.text.replace("\nещё\n", "").replace("На общих основаниях", "На_общих_основаниях").replace("Бюджетная основа", "Бюджетная_основа").replace(" ", ";")
        # print(text.count("\n"))
        text = text[text.find("\n")+1:]
        print(text)
        f.write(text)
    elif MODE == TR_MODE:
        cells = driver.find_elements(By.TAG_NAME, "td")
        rows = [";".join(cells[i:i+cnt_columns])+";" for i in range(0, len(cells), cnt_columns)]
        print(rows)
        f.writelines(rows)
    elif MODE == TABLE_MODE:
        res_rows = []
        rows = driver.find_elements(By.CLASS_NAME, "normal")
        i = 0
        for tr in rows:
            res_rows.append(";".join([th.text for th in tr.find_elements(By.TAG_NAME, "td")]) + ";")
            if i == len(rows) // 4 or i == len(rows) // 4 * 2 or i == len(rows) // 4 * 3:
                print(i / len(rows), i, len(rows))
            i += 1
        f.writelines(res_rows)

    f.close()


num_sect = 1
while True:
    el1 = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/main/div/div/section[2]/div[1]/div[2]/div[2]/label")
    print(el1)
    el1.click()
    sleep(0.3)
    el2 = driver.find_element(By.CLASS_NAME, "q-virtual-scroll__content")

    sections = el2.find_elements(By.CLASS_NAME, "q-item")
    # print(len(sections))
    load_section(sections[num_sect])
    if num_sect == len(sections) - 1:
        break
    num_sect += 1
    break
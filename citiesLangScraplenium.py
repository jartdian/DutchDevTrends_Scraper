from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import random

languages = [
    "javascript",
    "python",
    "ruby",
    "java",
    "C%2B%2B",
    "c%23",
    "golang",
    "swift",
    "php",
    "sql",
    "typescript",
    "kotlin",
]
cities = [
    "Amsterdam",
    "Rotterdam",
    "Den Haag",
    "Utrecht",
    "Eindhoven",
    "Groningen",
    "Zwolle",
    "Nijmegen",
    "Tilburg",
    "'s-Hertogenbosch",
    "Breda",
    "Almere",
    "Apeldoorn",
    "Arnhem",
    "Haarlem",
    "Enschede",
    "Amersfoort",
    "Leeuwarden",
    "Sittard",
]

citiesLangData = {
    "Rotterdam": {"coordinates": [51.9225, 4.47917], "data": {}},
    "Amsterdam": {"coordinates": [52.3676, 4.9041], "data": {}},
    "Den Haag": {"coordinates": [52.0705, 4.3007], "data": {}},
    "Utrecht": {"coordinates": [52.0907, 5.1214], "data": {}},
    "Eindhoven": {"coordinates": [51.4416, 5.4697], "data": {}},
    "Groningen": {"coordinates": [53.2194, 6.5665], "data": {}},
    "Zwolle": {"coordinates": [52.5150, 6.0835], "data": {}},
    "Nijmegen": {"coordinates": [51.8426, 5.8546], "data": {}},
    "Tilburg": {"coordinates": [51.5719, 5.0672], "data": {}},
    "'s-Hertogenbosch": {"coordinates": [51.6888, 5.2884], "data": {}},
    "Breda": {"coordinates": [51.5831, 4.7484], "data": {}},
    "Almere": {"coordinates": [52.3508, 5.2647], "data": {}},
    "Apeldoorn": {"coordinates": [52.2112, 5.9699], "data": {}},
    "Arnhem": {"coordinates": [51.9851, 5.8987], "data": {}},
    "Haarlem": {"coordinates": [52.3874, 4.9024], "data": {}},
    "Enschede": {"coordinates": [52.2215, 6.8937], "data": {}},
    "Amersfoort": {"coordinates": [52.1561, 5.3878], "data": {}},
    "Leeuwarden": {"coordinates": [53.2194, 5.8054], "data": {}},
    "Sittard": {"coordinates": [51.0018, 5.8662], "data": {}},
}

url_base = "https://nl.indeed.com/jobs?q={}&l={}&radius=25"

driver = webdriver.Chrome()

successful_iterations = 0

start_iteration = 0

try:
    for iteration, language in enumerate(languages, start=start_iteration):
        for city in cities:
            url = url_base.format(language, city)
            driver.get(url)
            sleep_time = random.uniform(4, 7)
            time.sleep(sleep_time)

            try:
                element_to_capture = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-JobCountAndSortPane-jobCount"))
                )
                element_text = element_to_capture.text
                job_count = int("".join(filter(str.isdigit, element_text)))

                citiesLangData[city]["data"][language] = job_count
                successful_iterations += 1

                with open('output.txt', 'a') as file:
                    file.write(f'Iteration {iteration}: {element_text}\n')

            except Exception as e:
                # Log the exception and continue with the next iteration
                print(f'Error in iteration {iteration}, language {language}, city {city}: {str(e)}')

finally:
    driver.quit()

citiesLangData_json = json.dumps(citiesLangData, indent=2)
file_path = "citiesLangData.js"
with open(file_path, "w") as file:
    file.write(f"const citiesLangData = {citiesLangData_json};")

print(f"City coordinates data has been saved to {file_path}")
print(f'Successful iterations: {successful_iterations}')

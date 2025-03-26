import requests
from bs4 import BeautifulSoup
import json

url = input('Введите ссылку на таблицу >>> ')
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="waffle")

if table:
    rows = table.find_all("tr")
    directions = {}

    if len(rows) >= 2:
        semester_text = rows[2].get_text(separator=' ', strip=True)
        parts = semester_text.split(' уч. года ')
        if len(parts) > 1:
            central_part = parts[0].split('на ')[-1].strip()
            semester = central_part

    for row in rows[1:]:
        cells = row.find_all(["th", "td"])
        row_data = [cell.get_text(separator=' ', strip=True) for cell in cells]

        if len(row_data) >= 7:
            direction = row_data[2]
            project_name = row_data[3]

            teachers_cell = cells[4].get_text(separator=', ', strip=True) if cells[4].get_text(strip=True) else ""
            contacts_cell = cells[5].get_text(separator=', ', strip=True) if cells[5].get_text(strip=True) else ""

            teachers = teachers_cell.split(', ') if ', ' in teachers_cell else teachers_cell
            contacts = contacts_cell.split(', ') if ', ' in contacts_cell else contacts_cell

            project_info = {
                "teachers": teachers,  
                "contacts": contacts, 
                "schedule": {}
            }

            schedule_days = {
                "Monday": 6,      
                "Wednesday": 7,   
                "Consultations": 8   
            }

            for day, index in schedule_days.items():
                if index < len(row_data) and row_data[index]:
                    schedule_info = row_data[index]
                    project_info["schedule"][day] = [schedule_info] if schedule_info else []

            if direction not in directions:
                directions[direction] = {}

            directions[direction][project_name] = project_info

    result = {
        "semester": semester,
        "directions": directions
    }

    with open("schedule.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в schedule.json")

else:
    print("Таблица не найдена!")

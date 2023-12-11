from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

## 1. Выполните пункты 1-3 задания.
## Ваш код
## Составляю список полных имен из 3х элементов
full_name_list = []
for row in contacts_list[1:]:
    name = row[0].split() + row[1].split() + row[2].split()
    while len(name) < 3:
        name.append('')
    full_name_list.append(name)

# С помощью регулярного выражения составляю список телефонов в правильном формате
pattern = r"^(\+7|8)\s?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})\s?\(?(доб. \d+)?\)?"
sub = r"+7(\2)\3-\4-\5 \6"
phones = [row[5] for row in contacts_list[1:]]
phones_new = [re.sub(pattern, sub, phone).strip() for phone in phones]

# Объединяю дублирующиеся записи
contacts_list_dict = {}
for idx, (name, phone) in enumerate(zip(full_name_list, phones_new)):
    key = ' '.join(name[:2])
    row = name + contacts_list[idx+1][3:5] + [phone] + [contacts_list[idx+1][6]]
    if key not in contacts_list_dict.keys():
        contacts_list_dict[key] = row
    else:
        row_new = []
        for col1, col2 in zip(contacts_list_dict[key], row):
            if col1:
                row_new.append(col1)
            else:
                row_new.append(col2)
        contacts_list_dict[key] = row_new

# Результат
contacts_list_new = [contacts_list[0]] + list(contacts_list_dict.values())
pprint(contacts_list_new)

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')

    ## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contacts_list_new)
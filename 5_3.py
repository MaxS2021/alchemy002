"""
Везение кончилось
Ограничение времени	10 секунд
Ограничение памяти	64Mb
Ввод	стандартный ввод
Вывод	стандартный вывод
Одиннадцатого декабря, без четверти одиннадцать вечера, поезд остановился в Нью-Йорке,
и путешественники поспешили в порт, где должен был стоять на якоре пароход до Ливерпуля.
И тут везение закончилось: пароход «Китай» отправился в плавание сорок пять минут назад!
Вся сумасшедшая гонка оказалась напрасной.
Напишите программу, выбирающую пароходы.
Через аргументы командной строки передаются адрес (address) и порт (port) сервера, а
также имя файла csv (file), в котором записаны данные о ближайших пароходах. Заголовки
файла (разделители запятые):
id, порт следования, название парохода время отплытия
id, port, steamer, departure
Напишите приложение на flask для того, чтобы при переходе по адресу
http://address:port/luck возвращает словарь в формате json,
в котором по ключу – часу отплытия записан список кораблей, отплывающих в этот час,
в порядке увеличения времени отплытия, в случае одинакового по алфавиту.

Пример
Ввод	Вывод
# Пример запуска:
python 5_3.py --address 127.0.0.1 --port 5000 --file steamers.csv
# Содержание файла steamers.csv:
id,port,steamer,departure
1,Seaham,Fairy,8:15
2,Blyth,Flosie,13:25
3,Wisbech,Garland,8:20
4,Felixstowe,Fortuna,13:06
5,Mistley,Harvester,9:05
6,Cowes,Hope,6:00
7,Fowey,Ajax,8:15
{
    "8": [
        "Ajax",
        "Fairy",
        "Garland"
    ],
    "13": [
        "Fortuna",
        "Flosie"
    ],
    "9": [
        "Harvester"
    ],
    "6": [
        "Hope"
    ]
}
Примечания
CSV файл из примера можно скачать здесь
"""

from flask import Flask
from flask import jsonify
import sys

print(sys.argv)
args = {}
arg = sys.argv
for i in range(1, len(sys.argv)):
    if arg[i][0:2] == "--":
        args[arg[i][2:]] = arg[i + 1]
# print(args)

app = Flask(__name__)


@app.route('/luck')
def luck():
    with open(args['file'], "r", encoding='utf-8') as f:
        csv = f.readlines()
    # print(csv)
    data = csv[1:]
    jsn = {}
    for d in data:
        d1 = d.strip().split(",")
        h = d1[3][:-3]
        jsn.setdefault(h, []).append((d1[2], d1[3][-2:]))

    for k, v in jsn.items():
        v1 = sorted(v, key=lambda x: (x[1], x[0]))
        jsn[k] = []
        for v2 in v1:
            jsn[k].append(v2[0])
    print(*jsn.items(), sep="\n")

    return jsonify(jsn)


if __name__ == '__main__':
    app.run(port=args['port'], host=args['address'])

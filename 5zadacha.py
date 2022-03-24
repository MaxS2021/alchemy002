"""
Но едва они ступили на землю Англии, как сыщик Фикс положил руку на плечо мистера
Фогга и торжественно объявил:
– Именем закона – вы арестованы.
Напишите программу для выбора арестованных.
Через аргументы командной строки передаются хост (host) и порт (port) сервера,
а также имя файла csv filename) и параметр choice – одно из двух значений – date или blame.
В файле записаны данные об арестованных, разделители двоеточие, заголовки файла:
id, фамилия, имя, дата, обвинение, срок ареста
id, surname,first_name, date, charge, arrest_term
Напишите приложение на flask, которое при переходе по адресу http://host:port/arrest
возвращает словарь в формате json с ключами: если параметр choice имеет значение date,
то ключи даты, если blame, то статьи обвинения, значения – списки фамилий и имен
в алфавитном порядке.

Пример
Ввод	Вывод
# Пример запуска:
python3 solution.py --host 127.0.0.1 --port 5000 --filename accuse.csv --choice blame
# Содержимое файла accuse.csv:
id;surname;first_name;date;charge;arrest_term
1;Fogg;Phileas;29/09;robbery;60
2;Smith;Jacob;29/09;theft;20
3;Gabor;Sam;1/10;assault;60
4;Smith;Jeb;29/09;theft;20
5;Adams;John;1/10;theft;30
6;Byron;George;30/09;assault;60

"""

from flask import Flask
from flask import jsonify, request
import requests
import json
import sys
import csv


print(sys.argv)
args = {}
arg = sys.argv
for i in range(1, len(sys.argv)):
    if arg[i][0:2] == "--":
        args[arg[i][2:]] = arg[i + 1]
print(args)

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "5 zadach!"


@app.route('/arrest')
def arrest():
    with open(args['filename'], "r", encoding='utf-8') as csvf:
        data = csvf.readlines()
        #reader = list(csv.reader(csvf, delimiter=';', quotechar='"'))
    print(data)
    data = data[1:]
    #prit(reader)
    jsn = {}
    for dt in data:
        dt1 = dt.split(";")
        print(dt1)
        if args["choice"] == 'date':
            jsn.setdefault(dt1[3],[]).append(dt1[1]+" "+dt1[2])
        elif args["choice"] == 'blame':
            jsn.setdefault(dt1[4], []).append(dt1[1] + " " + dt1[2])
    for k, v in jsn.items():
        jsn[k]=sorted(v)
    return jsonify(jsn)


if __name__ == '__main__':
    app.run(port=args['port'], host=args['host'])

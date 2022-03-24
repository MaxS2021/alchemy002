"""
На улицах Бомбея было необычайно многолюдно. Разинув рот, молодой француз таращил глаза
на персов в остроконечных шапках, на торговцев-банианов в круглых тюрбанах, на парсов в
чёрных митрах, армян в длиннополой, до пят одежде. Никогда ещё он не видел ничего
подобного и так увлёкся, что едва не забыл про время.
Напишите программу для определения, кто что носит.
Через аргументы командной строки передаются адрес (server) и порт (port) сервера и имя
файла json (filename) с данными. В файле находится список словарей с ключами: ethnos (этнос),
clothing (одежда).
Напишите приложение на flask, которое при переходе по адресу http://server:port/bombay/
возвращает словарь в формате json с ключами – этносами и значениями – списками видов
одежды без повторений в алфавитном порядке.

Пример
Ввод	Вывод
# Пример запуска:
python 5_2.py --server 127.0.0.1 --port 5000 --filename wear.json
# Содержимое файла wear.json:
[
 {
   "ethnos": "Bengali",
   "clothing": "dhoti"
 },
 {
   "ethnos": "Tamil",
   "clothing": "salwar"
 },
 {
   "ethnos": "Bengali",
   "clothing": "shirvani"
 },
 {
   "ethnos": "Bengali",
   "clothing": "sari"
 },
 {
   "ethnos": "Bengali",
   "clothing": "sari"
 },
 {
   "ethnos": "Punjabi",
   "clothing": "sari"
 }
]
{
    "Bengali": [
        "dhoti",
        "sari",
        "shirvani"
    ],
    "Tamil": [
        "salwar"
    ],
    "Punjabi": [
        "sari"
    ]
}
Примечания
JSON файл из примера можно скачать здесь
"""


from flask import Flask
from flask import jsonify
import json
import sys


print(sys.argv)
args = {}
arg = sys.argv
for i in range(1, len(sys.argv)):
    if arg[i][0:2] == "--":
        args[arg[i][2:]] = arg[i + 1]
#print(args)

app = Flask(__name__)


@app.route('/bombay')
def bombay():
    with open(args['filename'], "r", encoding='utf-8') as jsf:
        data_js = json.load(jsf)
    #print(data_js)
    jsn = {}
    for di in data_js:
        key = di['ethnos']
        value = di['clothing']
        jsn.setdefault(key, []).append(value)
    for k, v in jsn.items():
        jsn[k] = sorted(list(set(v)))
    #sorted_jsn = dict(sorted(jsn.items()))
    # for k, v in jsn.items():
    #     jsn[k] = sorted(v)
    return jsonify(jsn)


if __name__ == '__main__':
    app.run(port=args['port'], host=args['server'])
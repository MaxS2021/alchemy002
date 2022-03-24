"""
В клубе джентльмены обсуждали ограбление банка и то, что преступника, конечно, не найдут,
ведь Земля велика.
– Была когда-то велика, – заметил Филеас Фогг, внезапно вступив в разговор.
– Что вы имели в виду, мистер Фогг? Почему была когда-то? Разве мир стал меньше?
– Вне всяких сомнений, – ответил Филеас Фогг. – Земля действительно уменьшилась.
Теперь можно объехать вокруг неё в десять раз быстрее, чем столетие назад.
Напишите программу для сравнения скоростей перемещения.
Через аргументы командной строки передаются хост (host) и порт (port) сервера, а также
имя файла (ﬁle) с информацией о перемещениях между городами, заголовки файла
(разделители двоеточие):
id, пункт отправления, пункт прибытия, расстояние, вид транспорта, время в пути
id, departure, arrival, distance, transport, time
Напишите приложение на ﬂask, которое выполняет следующую функцию:
при обращении по адресу http://host:port/less/ приложение возвращает словарь в
формате json с ключами – видами транспорта и значениями – списками из двух значений:
минимальной и максимальной скоростью для этого вида транспорта, округленных до целого
числа вниз.

Пример
Ввод	Вывод
# Пример запуска:
python solution.py --host 127.0.0.1 --port 5000 --file peace.csv
# Содержимое файла peace.csv:
id:departure:arrival:distance:transport:time
1:London:Paris:460:train:9
2:Paris:Brussel:305:airplane:5
3:Antwerpen:Liege:122:car:4
4:Gent:Brest:826:airplane:12
5:Brest:Bilbo:981:train:23
6:Madrid:Rabat:1022:airplane:38
7:Porto:Madrid:468:airplane:8
{
    "train": [
        42,
        51
    ],
    "airplane": [
        26,
        68
    ],
    "car": [
        30,
        30
    ]
}
Примечания
CSV файл из примера можно скачать здесь
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
    return "5 !"


@app.route('/less')
def less():
    with open(args['file'], "r", encoding='utf-8') as csvf:
        road = list(map(lambda x:x.strip(), csvf.readlines()))
        # reader = list(csv.reader(csvf, delimiter=';', quotechar='"'))
    print(road)
    data = road[1:]
    # prit(reader)
    jsn = {}
    for dt in data:
        dt1 = dt.split(":")
        print(dt1)
        dst = int(int(dt1[3])/int(dt1[5]))
        if dt1[4] not in jsn:
            jsn[dt1[4]]=[999999,0]
        jsn[dt1[4]][0]= min(jsn[dt1[4]][0], dst)
        jsn[dt1[4]][1] = max(jsn[dt1[4]][1], dst)
        # if args["choice"] == 'date':
        #     jsn.setdefault(dt1[3], []).append(dt1[1] + " " + dt1[2])
        # elif args["choice"] == 'blame':
        #     jsn.setdefault(dt1[4], []).append(dt1[1] + " " + dt1[2])
    # for k, v in jsn.items():
    #     jsn[k] = sorted(v)
    return jsonify(jsn)


if __name__ == '__main__':
    app.run(port=args['port'], host=args['host'])
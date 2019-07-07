from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

#Chapter 1
superheroes = [{'name':'Batman', 'origin':'DC'}, {'name':'Superman', 'origin':'DC'}]

@app.route('/chapter1', methods=['GET', 'POST'])
def chapter1All():
    if request.method == 'POST':
        superhero = {'name' : request.form['name'], 'origin' : request.form['origin']}
        superheroes.append(superhero)
        return jsonify(superheroes)
    else:
        return request.args.get('name')

@app.route('/chapter1/<string:name>', methods=['GET', 'PUT', 'DELETE'])
def chapter1One(name):
    if request.method == 'PUT':
        supers = [superhero for superhero in superheroes if superhero['name']==name]
        supers[0]['name'] = request.form['name']
        supers[0]['origin'] = request.form['origin']
        return jsonify(superheroes)
    elif request.method == 'DELETE':
        supers = [superhero for superhero in superheroes if superhero['name']==name]
        superheroes.remove(supers[0])
        return jsonify(superheroes)
    else:
        supers = [superhero for superhero in superheroes if superhero['name']==name]
        return 'Hello, {0} from {1} Universe!'.format(supers[0]['name'], supers[0]['origin'])

#Chapter 2
@app.route('/chapter2', methods=['POST'])
def chapter2():
    npm = request.form['npm']
    listNpm = list(map(int, npm))

    added = 0
    for x in listNpm:
        added += x

    multiplied = 0
    for x in listNpm:
        multiplied *= x
    
    even = []
    for n in listNpm:
        if(n % 2 == 0):
            if(n != 0):
                even.append(str(n))
    joinedEven = ', '.join(even)

    odd = []
    for n in listNpm:
        if(n % 2 != 0):
            odd.append(str(n))
    joinedOdd = ', '.join(odd)

    return 'NPM anda {}\nTotal penjumlahan {}\nTotal perkalian {}\nBilangan genap {}\nBilangan ganjil {}'.format(npm, added, multiplied, joinedEven, joinedOdd)

#Chapter 3
from libs.Calculator import Calculator
from libs import checknumber as cn

@app.route('/chapter3', methods=['POST'])
def chapter3():
    number1 = int(request.form['number1'])
    number2 = int(request.form['number2'])

    cal = Calculator(number1, number2)

    cal.added()
    cal.substracted()
    cal.multiplied()
    cal.divided()

    return '{} {} dan {}\n{} {} dan {}\nHasil penjumlahan {}\nHasil pengurangan {}\nHasil perkalian {}\nHasil pembagian {}'.format(number1, cn.evenedorodded(number1), cn.isPrime(number1), number2, cn.evenedorodded(number2), cn.isPrime(number2), cal.add, cal.substract, cal.multiply, cal.divide)

#Chapter 4
import csv
import pandas

@app.route('/chapter4', methods=['GET', 'POST'])
def chapter4All():
    if request.method == 'POST':
        npm = request.form['npm']
        nama = request.form['nama']
        kelas = request.form['kelas']

        writeModeListCsv = csv.writer(open('listmahasiswa.csv', mode='a', newline=''))
        writeModeListCsv.writerow([npm, nama, kelas])

        return 'Berhasil menambahkan data'
    else:
        readerModeListCsv = csv.reader(open('listmahasiswa.csv', mode='r'))
        next(readerModeListCsv, None)
        readerModeDictCsv = csv.DictReader(open('listmahasiswa.csv', mode='r'))  
        readerModePandas = pandas.read_csv('listmahasiswa.csv')

        return render_template('chapter4all.html', resultModeListCsv = readerModeListCsv, resultModeDictCsv = readerModeDictCsv, resultModePandas = readerModePandas)

@app.route('/chapter4/<int:param>', methods=['GET', 'PUT'])
def chapter4One(param):
    if request.method == 'PUT':
        readerModeListCsv = csv.reader(open('listmahasiswa.csv', mode='r'))
        lines = list(readerModeListCsv)
        lines[param] = [request.form['npm'], request.form['nama'], request.form['kelas']]

        writeModeListCsv = csv.writer(open('listmahasiswa.csv', mode='w', newline=''))
        writeModeListCsv.writerows(lines)

        return 'Berhasil mengubah data'
    else:
        readerModeListCsv = csv.reader(open('listmahasiswa.csv', mode='r'))
        next(readerModeListCsv, None)
        lines = list(readerModeListCsv)
        return jsonify(lines[param])
        # return render_template('chapter4One.html', resultModeListCsv = lines[param])

#Chapter 5
import serial
import time

@app.route('/chapter5', methods=['POST','GET'])
def chapter5():
    arduino = serial.Serial('COM3', 9600)
    time.sleep(2)

    if request.method == 'POST':
        status = request.form['status']
        if status == 'on':
            arduino.write(b'H')
            return 'The LED is on'
        elif status == 'off':
            arduino.write(b'L')
            return 'The LED is off'
    else:
        data = []
        count = 0
        while count < 5:
            arduino.write(b'G')
            result = arduino.readline().decode("utf-8").strip('\n').strip('\r')
            data.append(result)
            count +=1
            time.sleep(0.5)

        return jsonify(data)            

#Chapter 6
from matplotlib import pyplot as plt

years = [2014,2015,2016,2017,2018]
fansDC = [76,87,105,122,148]
fansMarvel = [78,97,114,134,146]

@app.route('/chapter6', methods=['GET', 'POST', 'DELETE'])
def chapter6All():
    if request.method == 'POST':
        year = int(request.form['year'])
        fanDC = int(request.form['fanDC'])
        fanMarvel = int(request.form['fanMarvel'])

        years.append(year)
        fansDC.append(fanDC)
        fansMarvel.append(fanMarvel)

        return jsonify(years, fansDC, fansMarvel)
    elif request.method == 'DELETE':      
        year = int(request.form['year'])

        fansDC.remove(fansDC[years.index(year)])
        fansMarvel.remove(fansMarvel[years.index(year)])
        years.remove(years[years.index(year)])

        return jsonify(years, fansDC, fansMarvel)
    else:
        plt.plot(years, fansDC,'b',label='Team DC', linewidth=1)
        plt.plot(years, fansMarvel,'r',label='Team Marvel',linewidth=1)
        plt.xticks(range(years[0],years[-1]+1))
        plt.title('Fans Superheroes')
        plt.ylabel('Jumlah Fans')
        plt.xlabel('Tahun')
        plt.legend()
            
        plt.savefig('static/plot.png', dpi=300, bbox_inches='tight')
        return render_template('chapter6.html', url = 'static/plot.png')

@app.route('/chapter6/<string:origin>', methods=['GET', 'PUT'])
def chapter6One(origin):
    if request.method == 'PUT':
        year = int(request.form['year'])
        
        if origin == 'DC':
            fanDC = int(request.form['fan'])
            fansDC[years.index(year)] = fanDC

            return jsonify(years, fansDC, fansMarvel)
        elif origin == 'Marvel':
            fanMarvel = int(request.form['fan'])
            fansMarvel[years.index(year)] = fanMarvel
            
            return jsonify(years, fansDC, fansMarvel)
        else:
            return 'Tidak mengubah apapun'
    else:
        if origin == 'DC':
            plt.plot(years,fansDC,'b',label='Team DC', linewidth=1)
        elif origin == 'Marvel':
            plt.plot(years,fansMarvel,'r',label='Team Marvel',linewidth=1)
        
        plt.xticks(range(years[0],years[-1]+1))
        plt.title('Fans Superheroes')
        plt.ylabel('Jumlah Fans')
        plt.xlabel('Tahun')
        plt.legend()
              
        plt.savefig('static/plot.png', dpi=300, bbox_inches='tight')
        return render_template('chapter6.html', url = '../static/plot.png')

# if __name__ == '__main__':
#     app.run(debug=True)
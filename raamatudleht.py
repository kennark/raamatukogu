from leht import *
import raamatud as r

@app.route('/raamatud', methods=['GET'])
@flask_login.login_required
def books():

    asukohad = r.asukohad()
    sarjad = r.sarjad()

    nimetus = request.args.get('nimetus')
    autor = request.args.get('autor')
    aasta = request.args.get('aasta')
    asukoht = request.args.get('asukoht')
    sari = request.args.get('sari')
    number = request.args.get('number')
    if nimetus != None or autor != None or aasta != None or asukoht != None or sari != None or number != None:
        data = r.täpne_otsing(nimetus, autor, aasta, asukoht, sari, number)
        return render_template('books.html', data=data, asukohad=asukohad, sarjad=sarjad)

    return render_template('books.html', asukohad=asukohad, sarjad=sarjad)

@app.route('/raamatud/all')
@flask_login.login_required
def allbooks():
    data = r.kõik_raamatud()
    return render_template('allbooks.html', data=data)

@app.route('/raamatud/read', methods=['POST'])
@flask_login.login_required
def read():
    id = request.form['id']
    r.märgi_loetuks(id)
    return redirect(url_for('books'))

@app.route('/raamatud/update', methods=['POST'])
@flask_login.login_required
def updatebook():
    id = request.form['id']
    asukoht = request.form['asukoht']
    enda_id = request.form['enda_id']
    r.muuda_andmed(id, asukoht, enda_id)
    return redirect(url_for('books'))

@app.route('/raamatud/delete', methods=['POST'])
@flask_login.login_required
def deletebook():
    id = request.form['id']
    r.eemalda_raamat(id)
    return redirect(url_for('books'))

@app.route('/raamatud/create', methods=['POST'])
@flask_login.login_required
def createbook():
    nimetus = request.form['nimetus']
    autor = request.form['autor']
    aasta = request.form['aasta']
    lk_arv = request.form['lk_arv']
    asukoht = request.form['asukoht']
    sari = request.form['sari']
    number = request.form['number']
    r.lisa_raamat(nimetus, autor, aasta, lk_arv, asukoht, sari, number)

    osad = nimetus.split(" ")
    a = ""
    for osa in osad:
        a += osa + "+"
    return redirect('/raamatud?nimetus=' + a[0:-1])

@app.route('/raamatud/addseries', methods=['POST'])
@flask_login.login_required
def addseries():
    sari = request.form['sari']
    r.lisa_sari(sari)
    return redirect(url_for('books'))

@app.route('/raamatud/addlocation', methods=['POST'])
@flask_login.login_required
def addlocation():
    asukoht = request.form['asukoht']
    r.lisa_asukoht(asukoht)
    return redirect(url_for('books'))


if __name__ == '__main__':
    app.run(debug=True)

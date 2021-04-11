
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
from flask import Flask, render_template, request, redirect, jsonify, session


app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'assalamualaikum'  # secret key


cred = credentials.Certificate("kunci.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/')
def index():
    if 'login' not in session:
        return redirect('/login')
    daftar_mhs = []
    docs = db.collection('mahasiswa1').stream()
    for doc in docs:
        "print(f'(doc.id) -> {doc.to_dict()}')"
        mhs = doc.to_dict()
        mhs["id"] = doc.id
        daftar_mhs.append(mhs)
    return render_template('index.html', mahasiswa=daftar_mhs)


@app.route('/proseslogin', methods=["POST"])
def proseslogin():
    username_form = request.form.get("username")
    password_form = request.form.get("password")
    # docs = db.collection('admin').stream()
    # for doc in docs:
    #     #"print(f'(doc.id) -> {doc.to_dict()}')"
    #     admin = doc.to_dict()
    #     if admin['username'] == username_form and admin['password'] == password_form:
    #         print('berhasil login')
    #         break
    #     else:
    #         print('gagal')    b
    docs = db.collection('admin').where(
        "username", "==", username_form).stream()
    for doc in docs:
        admin = doc.to_dict()
        print(admin)
        if admin['password'] == password_form:
            session['login'] = True
            return redirect('/')
    return render_template('login.html')


@app.route('/login')
def login():
    if 'login' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/api/mahasiswa')
def api_mahasiswa():
    daftar_mhs = []
    docs = db.collection('mahasiswa1').stream()
    for doc in docs:
        "print(f'(doc.id) -> {doc.to_dict()}')"
        mhs = doc.to_dict()
        mhs["id"] = doc.id
        daftar_mhs.append(mhs)
    return jsonify(daftar_mhs)


@app.route('/detail/<uid>')
def detail(uid):
    #mahasiswa = daftar_mhs[int(uid)-1]
    mahasiswa = db.collection('mahasiswa1').document(uid).get().to_dict()
    return render_template("detail.html", mahasiswa=mahasiswa)


@app.route('/add', methods=["POST"])
def add_data():
    nama = request.form.get("nama")
    nilai = request.form.get("nilai")

    mahasiswa = {
        'alamat': 'rumah',
        'email': 'mahasiswa@gmail.com',
        'nama': nama,
        'nilai': int(nilai),
        'foto': 'https://robohash.org/repudiandaenonqui.png?size=100x100&set=set1,',
        'no_hp': '123456',

    }
    db.collection('mahasiswa1').document().set(mahasiswa)

    daftar_mhs = []
    docs = db.collection('mahasiswa1').stream()
    for doc in docs:
        "print(f'(doc.id) -> {doc.to_dict()}')"
        mhs = doc.to_dict()
        mhs["id"] = doc.id
        daftar_mhs.append(mhs)
    return render_template('index.html', mahasiswa=daftar_mhs)


@app.route('/update/<uid>')
def update(uid):
    mhs = db.collection('mahasiswa1').document(uid).get()
    mahasiswa = mhs.to_dict()
    mahasiswa['id'] = mhs.id
    return render_template('update.html', mhs=mahasiswa)


@app.route('/delete/<uid>')
def delete(uid):
    # ambil nilai formulir
    db.collection('mahasiswa1').document(uid).delete()
    daftar_mhs = []
    docs = db.collection('mahasiswa1').stream()
    for doc in docs:
        "print(f'(doc.id) -> {doc.to_dict()}')"
        mhs = doc.to_dict()
        mhs["id"] = doc.id
        daftar_mhs.append(mhs)
    return render_template('index.html', mahasiswa=daftar_mhs)


@app.route('/updatedata/<uid>', methods=["POST"])
def updatedata(uid):
    # ambil nilai formulir
    nama = request.form.get("nama")
    nilai = request.form.get("nilai")

    db.collection('mahasiswa1').document(uid).update({
        'nama': nama,
        'nilai': int(nilai)
    })

    daftar_mhs = []
    docs = db.collection('mahasiswa1').stream()
    for doc in docs:
        "print(f'(doc.id) -> {doc.to_dict()}')"
        mhs = doc.to_dict()
        mhs["id"] = doc.id
        daftar_mhs.append(mhs)
    return render_template('index.html', mahasiswa=daftar_mhs)


if __name__ == "__main__":
    app.run(debug=True)

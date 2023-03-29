from flask import Flask, request, redirect, render_template
from AES_cryption import data_encrypt, data_decrypt
from peewee import *
from datetime import date, datetime

db = MySQLDatabase('student', host='localhost', port=3306, user='root', password='')
app = Flask(__name__)
remaining_account = None

def default(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError(f'Object of type {type(obj)} is not JSON serializable')

class Student(Model):
    masv = TextField()
    password = BlobField()
    hoten = TextField()
    ngaysinh = DateField()
    lop = TextField()
    khoa = TextField()
    sothe = BlobField()
    cmnd = BlobField()

    class Meta:
        database = db

@app.route('/')
def index():
    global remaining_account
    if remaining_account is None:
        return redirect('/login')
    elif remaining_account == 'admin':
        return redirect('/admin')
    else:
        list_students = Student.select()
        return render_template('/index.html', list=list_students)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global remaining_account
    if remaining_account is None:
        if request.method == 'GET':
            return render_template('/login.html', text='')
        elif request.method == 'POST':
            tk = request.form['tk']
            password = request.form['password']
            if tk == 'admin' and password == 'admin':
                remaining_account = 'admin'
                return redirect('/admin')
            else:
                data = Student.select().where((Student.masv == tk))
                if data.exists():
                    list_students = [item.__dict__['__data__'] for item in data]
                    passwd = list_students[0]['password']
                    if data_encrypt(tk, password) == passwd:
                        remaining_account = tk
                        return redirect('/')
                    else:
                        render_template('/login.html', text='Tài khoản hoặc mật khẩu không đúng!')
                else:
                    return render_template('./login.html', text='Tài khoản hoặc mật khẩu không đúng!')
    elif remaining_account == 'admin':
        return redirect('/admin')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    global remaining_account
    remaining_account = None
    return redirect('/')

@app.route('/admin')
def admin():
    global remaining_account
    if remaining_account == 'admin':
        list_students = Student.select()
        return render_template('/admin.html', list=list_students)
    else:
        return redirect('/')


@app.route('/info/<masv>')  
def get_info(masv):
    global remaining_account
    if remaining_account is None:
        return redirect('/')
    else:
        data = Student.select().where(Student.masv == masv)
        list_students = [item.__dict__['__data__'] for item in data]
        chosen_student = list_students[0]
        if remaining_account == 'admin':
            masv = chosen_student['masv']
            passwd = data_decrypt(masv, chosen_student['password'])
            sothe = data_decrypt(masv, chosen_student['sothe'])
            cmnd = data_decrypt(masv, chosen_student['cmnd'])
        else:
            passwd = data_decrypt(remaining_account, chosen_student['password'])
            sothe = data_decrypt(remaining_account, chosen_student['sothe'])
            cmnd = data_decrypt(remaining_account, chosen_student['cmnd'])
        chosen_student['password'] = passwd
        chosen_student['sothe'] = sothe
        chosen_student['cmnd'] = cmnd
        return render_template('/ttsv.html', sv = chosen_student)

@app.route('/them_sv', methods=['GET', 'POST'])
def them_sv():
    global remaining_account
    if remaining_account == 'admin':
        if request.method == 'GET':
            return render_template('/them_sv.html', text='')
        elif request.method == 'POST':
            masv = request.form['tk']
            password = request.form['password']
            hoten = request.form['hoten']
            ngaysinh = request.form['ngaysinh']
            ngaysinh_obj = datetime.strptime(ngaysinh, '%Y-%m-%d')
            ngaysinh_obj = ngaysinh_obj.date()
            lop = request.form['lop']
            khoa = request.form['khoa']
            sothe = request.form['sothe']
            cmnd = request.form['cmnd']
            password = data_encrypt(masv, password)
            sothe = data_encrypt(masv, sothe)
            cmnd = data_encrypt(masv, cmnd)
            student = Student(masv=masv, password=password, hoten=hoten, ngaysinh=ngaysinh_obj, lop=lop, khoa=khoa, sothe=sothe, cmnd=cmnd)
            student.save()
            if Student.select().where(Student.masv == masv).exists():
                return render_template('/them_sv.html', text='Thêm thành công!')
            else:
                return render_template('/them_sv.html', text='Thêm thất bại!')
    else:
        return 'Bạn không có quyền thêm!'

@app.route('/delete/<masv>', methods=['GET', 'POST'])
def delete(masv):
    global remaining_account
    if remaining_account == 'admin':
        query = Student.delete().where(Student.masv == masv)
        query.execute()
        return redirect('/')
    else:
        return 'Bạn không có quyền xóa!'

@app.route('/suatt/<masv>', methods=['GET', 'POST'])
def sua_ttsv(masv):
    global remaining_account
    if remaining_account == 'admin':
        if request.method == 'GET':
            data = Student.select().where(Student.masv == masv)
            list_students = [item.__dict__['__data__'] for item in data]
            chosen_student = list_students[0]
            if remaining_account == 'admin':
                masv = chosen_student['masv']
                passwd = data_decrypt(masv, chosen_student['password'])
                sothe = data_decrypt(masv, chosen_student['sothe'])
                cmnd = data_decrypt(masv, chosen_student['cmnd'])
            else:
                passwd = data_decrypt(remaining_account, chosen_student['password'])
                sothe = data_decrypt(remaining_account, chosen_student['sothe'])
                cmnd = data_decrypt(remaining_account, chosen_student['cmnd'])
            chosen_student['password'] = passwd
            chosen_student['sothe'] = sothe
            chosen_student['cmnd'] = cmnd
            return render_template('/sua_ttsv.html', sv=chosen_student)
        elif request.method == 'POST':
            masv = request.form['tk']
            password = request.form['password']
            hoten = request.form['hoten']
            ngaysinh = request.form['ngaysinh']
            ngaysinh_obj = datetime.strptime(ngaysinh, '%Y-%m-%d')
            ngaysinh_obj = ngaysinh_obj.date()
            lop = request.form['lop']
            khoa = request.form['khoa']
            sothe = request.form['sothe']
            cmnd = request.form['cmnd']
            password = data_encrypt(masv, password)
            sothe = data_encrypt(masv, sothe)
            cmnd = data_encrypt(masv, cmnd)
            student = Student.get(Student.masv == masv)
            student.password = password
            student.hoten = hoten
            student.ngaysinh = ngaysinh_obj
            student.lop = lop
            student.khoa = khoa
            student.sothe = sothe
            student.cmnd = cmnd
            student.save()
            return redirect('/')
    else:
        return 'Bạn không có quyền sửa!'

@app.route('/xem_ttsv/<masv>', methods=['GET', 'POST'])
def vd(masv):
    global remaining_account
    if remaining_account == 'admin':
        if request.method == 'GET':
            data = Student.select().where(Student.masv == masv)
            list_students = [item.__dict__['__data__'] for item in data]
            chosen_student = list_students[0]
            chosen_student['password'] = chosen_student['password'].decode('ISO-8859-1')
            chosen_student['sothe'] = chosen_student['sothe'].decode('ISO-8859-1')
            chosen_student['cmnd'] = chosen_student['cmnd'].decode('ISO-8859-1')
            return render_template('/xem_ttsv.html', sv = chosen_student)
        elif request.method == 'POST':
            key = request.form['key']
            data = Student.select().where(Student.masv == masv)
            list_students = [item.__dict__['__data__'] for item in data]
            chosen_student = list_students[0]
            chosen_student['password'] = data_decrypt(key, chosen_student['password'])
            chosen_student['sothe'] = data_decrypt(key, chosen_student['sothe'])
            chosen_student['cmnd'] = data_decrypt(key, chosen_student['cmnd'])
            return render_template('/xem_ttsv.html', sv=chosen_student)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run()
    app.debug(True)


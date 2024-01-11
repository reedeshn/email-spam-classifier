from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Establish a connection to MySQL Server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mainreed"
)
mycursor = mydb.cursor()
print("Connection Established")

# Define routes for CRUD operations

@app.route('/')
def home():
    return render_template('one.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        sql = "INSERT INTO users (name, email, address, phone) VALUES (%s, %s, %s, %s)"
        val = (name, email, address, phone)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('read'))
    return render_template('two.html')

@app.route('/read')
def read():
    mycursor.execute("SELECT * FROM users")
    result = mycursor.fetchall()
    return render_template('three.html', result=result)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        sql = "UPDATE users SET name=%s, email=%s,address=%s,phone=%s WHERE id=%s"
        val = (name, email, address, phone, id)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('read'))
    mycursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    result = mycursor.fetchone()
    return render_template('four.html', result=result)

@app.route('/delete/<int:id>')
def delete(id):
    sql = "DELETE FROM users WHERE id=%s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('read'))

if __name__ == '__main__':
    app.run(debug=True)

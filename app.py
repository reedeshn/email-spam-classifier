from flask import Flask, render_template, request,redirect, url_for
import pickle
import mysql.connector
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)

ps = PorterStemmer()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mainreed"
)
@app.route('/')
def home():
    return render_template('index.html')

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

def predict_spam(input_sms):
    # Load pre-trained models
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))

    # Preprocess and predict
    transformed_sms = transform_text(input_sms)
    vector_input = tfidf.transform([transformed_sms])
    result = model.predict(vector_input)[0]

    return result

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_sms = request.form['input_sms']
        result = predict_spam(input_sms)
        return render_template('result.html', result=result)


@app.route('/one')
def one():
    return render_template('one.html')

mycursor = mydb.cursor()
print("Connection Established")



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

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

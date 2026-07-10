from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image
import os

app = Flask(__name__)
API_KEY = "AQ.Ab8RN6JZjkuDGGvobb5jnA0k1iyS2AySzCoKcqRnj9vAuN7Abg"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') #

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#თუ გაგზავნილი ფოტო 1 = ფოტო 2 მაშინ იგივე პირობა
# თუ იგივე არის თვითო იგი დაავადება მაშინ ქნას იგივე პირობა.
#გასაკეთებელი _+++++++++++++++++++++++++++++++++++++)choloka

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        plant = request.form.get('plant')
        count = request.form.get('count')
        file = request.files.get('file')

        if file and plant:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            img = Image.open(filepath)
            prompt = f"შენ ხარ აგრონომი. ეს არის {plant}-ის ფოტო. გააკეთე დაავადების დიაგნოსტიკა, მკურნალობის გზები, ხარჯთაღრიცხვა {count} ძირისთვის და რეკომენდაციები საქართველოში."
            response = model.generate_content([prompt, img])
            result = response.text

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
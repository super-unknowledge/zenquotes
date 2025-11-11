# zenquotes
A vibecoded Django web app that randomly displays a quote from a sqlite db.

✅ Steps to Run the Django App Locally

📦 1. Install Dependencies
pip install -r requirements.txt
⚠️ If you're missing pip, install it or use Python 3.10+ which comes bundled.

🔧 2. Apply Migrations (Set up the DB)
python manage.py makemigrations
python manage.py migrate

🧠 3. Load the Sample Quotes
The script created a management command and sample JSON:

python manage.py loadquotes

▶️  4. Run the Development Server
python manage.py runserver

🌐 5. Open in Your Browser
Visit:
http://127.0.0.1:8000/ — this is your Zen Quote homepage.

http://127.0.0.1:8000/quote/ — this is the JSON API that returns a random quote.


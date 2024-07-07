# Feedback Form for HeadHunters HQ Submission Technical Assessment

## How to run

1. Run `python -m venv venv`

2. In windows run: `venv\Scripts\activate`,
   In Linux/MacOS run: `source venv/Scripts/activate`

3. Run `pip install -r requirements.txt`

4. Run `cp .env.example .env`

5. Change .env to include your local postgreSQL instance

6. Run `alembic upgrade head`

7. Run `fastapi run app/main.py`

8. open [http://localhost:8000](http://localhost:8000) in the browser

## How to run tests

1. Run `pytest`
2. See the results

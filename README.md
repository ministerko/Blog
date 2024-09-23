# Blog

A scalable FastAPI project with support for multiple route files and modular architecture.

## Setup Instructions

1. Clone the repository to your local machine.
2. Create a virtual environment and activate it:
    `python3 -m venv venv`
    `source venv/bin/activate`
3. Install dependencies:
    `pip install -r requirements.txt`
4. Start the development server:
    `uvicorn app.main:app --reload`

## Project Structure

```
Blog/
├── app/
│   ├── routers/
│   │   ├── items.py
│   │   ├── users.py
│   ├── models/
│   ├── schemas/
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
├── tests/
├── .gitignore
├── README.md
├── requirements.txt
└── venv/
```

## Testing

Run tests using:
`pytest`

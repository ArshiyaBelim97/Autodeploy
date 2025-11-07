# Autodeploy
=======
# AI-Powered Autodeployment System (Serverless Demo)

## Backend (CLI)
1. Install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install typer boto3 awsgi

2. Run deploy:
   python cli.py deploy --git-url https://github.com/Arvo-AI/hello_world

## Frontend (React)
cd frontend
npm install
npm start

Enter GitHub URL + deployment description to see mock deployment.

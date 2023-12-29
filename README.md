# GCP Datastore GUI

## server 
- Python 3.11+ 
- Basic Flask server that connect to GCP Datastore emulator DB
- the datastore emulator should run on port `8001` and the project-id is `local-dev`
### install:
1. `cd server`
2. (recommended to create a venv) 
3. `pip install Flask google-cloud-datastore flask-cors`
4. `python app.py`

## Client
- React 18 (Vite)
- simple reactJS app that shows the db entities

### install:
1. `cd client` 
2. `yarn` or `npm install`
4. `yarn dev` or `npm run dev`
5. open http://localhost:8003

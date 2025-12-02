# Deploying Summarify (ready-to-deploy)

Below are simple ways to get your app live (no coding required). I cannot deploy for you from here, but I've prepared everything so you can deploy in minutes.

## Option 1 — Streamlit Community Cloud (free, easiest)
1. Create a free account at https://streamlit.io/cloud (Sign in with GitHub).
2. Create a new app, connect a GitHub repo containing these files (upload the project to a GitHub repo).
3. Set the main file path to `app.py`. Streamlit will install `requirements.txt` automatically.
4. Click deploy — your app will be live on a streamlit.app domain.

Notes: Streamlit Cloud allows small apps and is simplest. No Docker required.

## Option 2 — Render.com (free tier available)
1. Push the project to GitHub.
2. On Render, create a new Web Service.
3. Choose 'Docker' or 'Python' and point to the repo. If using 'Docker', Render will use the included `Dockerfile`. If using 'Python', set the Start Command to:
   `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Deploy — Render will build and provide a public URL.

## Option 3 — Heroku (deprecated for some but still works via Docker)
1. Use the included `Dockerfile` or `Procfile`.
2. Deploy via GitHub integration or Heroku CLI:
   `heroku container:push web && heroku container:release web`

## Local (run on your machine)
1. Create virtual env, install requirements:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
2. Open http://localhost:8501

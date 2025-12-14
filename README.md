# AI Lead Generation SaaS Platform

A Python Flask-based MVP for an AI-powered Lead Generation, Messaging, and Ad Campaign management platform.

## Features
- **Lead Generation:** Source leads by Industry and Location (uses Mock data provider by default).
- **Messaging:** Send simulated Emails/SMS to leads.
- **Campaign Management:** Launch and track ad campaigns across platforms.
- **Analytics:** View real-time performance metrics.

---

## 🚀 Local Development Setup

Follow these steps to run the application on your own machine.

### Prerequisites
- Python 3.8 or higher
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
You should see output indicating the server is running (usually `Running on http://127.0.0.1:5000`).
Open that URL in your web browser.

---

## ☁️ Deploying to Google Cloud Platform (App Engine)

This application is configured for easy deployment to Google App Engine (Standard Environment).

### Prerequisites
- [Google Cloud SDK (gcloud CLI)](https://cloud.google.com/sdk/docs/install) installed.
- A Google Cloud Project created.

### 1. Initialize gcloud
Login and select your project:
```bash
gcloud init
```

### 2. Deploy
Run the following command from the project root:
```bash
gcloud app deploy
```

### 3. View Your App
Once deployment finishes, run:
```bash
gcloud app browse
```
Or navigate to `https://YOUR_PROJECT_ID.uc.r.appspot.com`.

---

## ⚙️ Configuration

You can configure the application using Environment Variables.

| Variable | Default | Description |
|----------|---------|-------------|
| `LEAD_PROVIDER` | `MOCK` | Options: `MOCK`, `APOLLO`, `PDL`. |
| `LEAD_API_KEY` | `""` | Generic API Key (fallback). |
| `APOLLO_API_KEY` | `""` | Specific key for Apollo.io. |
| `PDL_API_KEY` | `""` | Specific key for People Data Labs. |
| `SECRET_KEY` | `secret...` | Flask Secret Key (Change this for production!). |

# 🚀 Deployment Guide: Drug-Free TN AI System

This guide provides step-by-step instructions to deploy the **Drug-Free TN AI System** using free cloud services: **Clever Cloud** (Database), **Hugging Face Spaces** (AI API Backend), and **GitHub Pages** (Frontend Dashboard).

---

## 🗺️ Deployment Overview

```
 ┌──────────────────────┐      (1) API Requests      ┌──────────────────────┐
 │    GitHub Pages      ├───────────────────────────>│ Hugging Face Spaces  │
 │ (Frontend Dashboard) │                            │ (FastAPI AI Backend) │
 └──────────────────────┘                            └──────────┬───────────┘
                                                                │
                                            (2) SQL Queries     │ (Clever Cloud Host)
                                                                ▼
                                                     ┌──────────────────────┐
                                                     │    Clever Cloud      │
                                                     │   (MySQL Database)   │
                                                     └──────────────────────┘
```

---

## 1. Database Setup (Clever Cloud) 🗄️

**Clever Cloud** provides a free 10MB MySQL instance, which is permanently online and requires no credit cards.

1. **Sign Up:** Create a free account at [clever-cloud.com](https://www.clever-cloud.com/).
2. **Create Database:**
   - In the console, click **Create...** and select **an add-on**.
   - Select **MySQL** from the list.
   - Choose the **Dev / Free** plan (10MB size limit) and click **Next**.
3. **Save Database Credentials:**
   - Once provisioned, click on the database name to view credentials.
   - Note down the:
     - **Host** (`bapary...mysql.services.clever-cloud.com`)
     - **Database Name** (`bapary...`)
     - **User** (`uc6...`)
     - **Password** (`c8y...`)
     - **Port** (`3306`)
4. **Initialize Table:**
   - Under the add-on menu, click on **phpMyAdmin** to open the SQL console.
   - Execute the following query to initialize the table:
     ```sql
     CREATE TABLE complaints (
         id INT AUTO_INCREMENT PRIMARY KEY,
         complaint_text TEXT,
         is_junk BOOLEAN,
         drug_type VARCHAR(100),
         crime_type VARCHAR(100),
         address TEXT,
         city VARCHAR(100),
         location_detail VARCHAR(255),
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

---

## 2. API Backend Deployment (Hugging Face Spaces) 🧠

**Hugging Face Spaces** hosts your FastAPI backend on their ZeroGPU free tier, allowing model inference to run with GPU acceleration.

1. **Create Space:**
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space).
   - Enter your **Space Name** (e.g., `drug-free-tn-complaint-classifier`).
   - Select **Gradio** as the Space SDK (this is the free SDK option).
   - **Important:** Click **ZeroGPU** under Space Hardware (Free tier).
   - Click **Create Space**.
2. **Add Environment Secrets:**
   - Go to the **Settings** tab of your Space.
   - Scroll down to the **Variables and secrets** section.
   - Add the following secrets using the credentials from your **Clever Cloud** database:
     - `DB_HOST` ➔ *your Clever Cloud host*
     - `DB_USER` ➔ *your Clever Cloud user*
     - `DB_PASSWORD` ➔ *your Clever Cloud password*
     - `DB_NAME` ➔ *your Clever Cloud database name*
     - `DB_PORT` ➔ `3306`
3. **Deploy Code from Terminal:**
   - Add the Hugging Face space as a Git remote:
     ```bash
     git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/YOUR_SPACE_NAME
     ```
   - Push your code to Hugging Face (when prompted for a password, generate and use a **Write Access Token** from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)):
     ```bash
     git push hf main --force
     ```
   - Hugging Face will automatically download your model files (`BART`, `MiniLM`, `BERT-NER`) and launch the Uvicorn FastAPI server on port `7860`.
   - Your API endpoints will be live at:
     `https://YOUR_HF_USERNAME-YOUR_SPACE_NAME.hf.space`

---

## 3. Frontend Deployment (GitHub Pages) 🖥️

**GitHub Pages** hosts the static HTML dashboard which calls your Hugging Face API dynamically.

1. **Deploy Code to GitHub:**
   - Create a GitHub repository (e.g., `drug-free-tn-message-classification`).
   - Push the codebase to the GitHub repository:
     ```bash
     git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
     git branch -M main
     git push -u origin main
     ```
2. **Enable GitHub Pages:**
   - Go to the **Settings** tab of your GitHub repository.
   - Click **Pages** in the left sidebar.
   - Under **Build and deployment**, select **Deploy from a branch**.
   - Choose the **`main`** branch and the root folder **`/`**.
   - Click **Save**.
   - Your site will go live in 1–2 minutes at:
     `https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPO_NAME/`

---

## 🔗 Running and Testing

To view the dashboard and submit new complaints, access your GitHub Pages URL while appending your Hugging Face Space URL as a query parameter (the dashboard will automatically save this URL to the browser's `localStorage` for future visits):

```text
https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPO_NAME/?api=https://YOUR_HF_USERNAME-YOUR_SPACE_NAME.hf.space
```

### Verification Endpoints:
- **Swagger Docs:** `https://YOUR_HF_USERNAME-YOUR_SPACE_NAME.hf.space/docs`
- **Dashboard Data:** `https://YOUR_HF_USERNAME-YOUR_SPACE_NAME.hf.space/api/dashboard/data`
- **Submission Portal:** `https://YOUR_HF_USERNAME-YOUR_SPACE_NAME.hf.space/api/dashboard/submit`

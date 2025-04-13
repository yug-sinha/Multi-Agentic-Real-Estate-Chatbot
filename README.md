# Multi-Agentic Real Estate Copilot

This repository contains a multi-agent real estate chatbot application that uses FastAPI (Python) for the backend and Next.js (TypeScript) for the frontend. The application can analyze property images for damage, answer tenancy-related questions, and provide context-driven responses.

## Table of Contents

1. [Features](#features)  
2. [Directory Structure](#directory-structure)  
3. [Setup & Installation](#setup--installation)  
4. [Backend Usage](#backend-usage)  
   - [Environment Variables](#environment-variables)  
   - [Local Run (without Docker)](#local-run-without-docker)  
   - [Docker Build & Run Locally](#docker-build--run-locally)  
5. [Frontend Usage](#frontend-usage)  
   - [Environment Variables](#environment-variables-1)  
   - [Local Run](#local-run)  
   - [Deploy on Vercel](#deploy-on-vercel)  
6. [Deployment on Render (Backend)](#deployment-on-render-backend)  
7. [License](#license)

---

## Features

- **Property Agent**: Upload an image and get diagnosis & recommendations on property issues (e.g., mold, cracks).  
- **Tenancy Agent**: Handles tenancy-related queries, referencing legal FAQs.  
- **Multi-Agent** logic: If an image is provided, the backend uses the Property Agent; otherwise defaults to the Tenancy Agent.  
- **RAG**: (Retrieval-Augmented Generation) example retrieving additional context.  

---

## Directory Structure

```
Multi-Agentic-Real-Estate-Chatbot
├─ backend
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ main.py
│   ├─ config.py
│   ├─ agents
│   │   ├─ property_agent.py
│   │   └─ tenancy_agent.py
│   ├─ utils
│   │   └─ rag.py
│   └─ ...
└─ frontend
    ├─ app
    │   ├─ api
    │   │   ├─ chat
    │   │   │   └─ route.ts
    │   │   └─ reset
    │   │       └─ route.ts
    │   ├─ page.tsx
    │   └─ layout.tsx
    ├─ components
    │   ├─ ChatBubble.tsx
    │   ├─ ChatInput.tsx
    │   └─ TypingLoader.tsx
    ├─ lib
    │   └─ api.ts
    ├─ styles
    │   └─ globals.css
    ├─ eslint.config.mjs
    └─ ...
```

- **backend/**: FastAPI code, including your Dockerfile and dependencies.  
- **frontend/**: Next.js 13+ with the App Router, TypeScript, and Tailwind CSS.  

---

## Setup & Installation

1. **Clone** the repository:
   ```bash
   git clone https://github.com/your-username/Multi-Agentic-Real-Estate-Chatbot.git
   ```
2. **Navigate** to either the `backend/` folder or `frontend/` folder for further setup steps.

---

## Backend Usage

### Environment Variables

Create a `.env` file in `backend/` (for local dev) with:
```
GEMINI_API_KEY=<YOUR_PALM_API_KEY>
```

- **`GEMINI_API_KEY`** is your Google PaLM / GenAI key.  
- Make sure you **do not** commit `.env` to public source control.  

In **production**, pass this key via environment variables rather than storing in `.env`.

### Local Run (Without Docker)

1. **Create a virtual environment** (optional but recommended):
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run** the FastAPI server:
   ```bash
   python main.py
   ```
4. Open your browser at `http://localhost:8000/docs` to see the API docs.

### Docker Build & Run Locally

1. **Build** the Docker image:
   ```bash
   cd backend
   docker build -t my-backend-image .
   ```
2. **Run** the container (specifying your environment variable):
   ```bash
   docker run -p 8000:8000 \
     -e GEMINI_API_KEY="AI.xxx" \
     --name my-backend-container \
     my-backend-image
   ```
   Or use `--env-file .env` if you have a `.env`:
   ```bash
   docker run -p 8000:8000 \
     --env-file .env \
     my-backend-image
   ```
The API is now accessible on `http://localhost:8000`.

---

## Frontend Usage

### Environment Variables

Create a file called `.env.local` in `frontend/` (which Next.js automatically loads in development):
```
BACKEND_URL=http://localhost:8000
```
- **`BACKEND_URL`** is the address where your FastAPI backend is running.

In production (e.g., on Vercel), set this variable in your project settings to your publicly accessible backend URL.

### Local Run

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```
2. **Start Development Server**:
   ```bash
   npm run dev
   ```
3. Open [http://localhost:3000](http://localhost:3000) to see the Next.js frontend. The chat calls your local backend at `http://localhost:8000`.

### Deploy on Vercel

1. **Push** your repo to GitHub (or similar).
2. Go to [Vercel](https://vercel.com/), create a **New Project**, and import your repository.
3. In the **Project Settings** → **Environment Variables**, add:
   ```
   BACKEND_URL=https://YOUR_BACKEND_URL
   ```
4. On build, Vercel will read `BACKEND_URL` and your Next.js serverless functions will route API calls to that URL.  
5. Once the build finishes, you can access your site at `https://<your-vercel-project>.vercel.app`.

---

## Deployment on Render (Backend)

1. Create a **new service** in Render:
   - **Type**: Web Service.
   - **Repo**: your GitHub repo.
2. In the **Service Settings**:
   - **Environment**: Provide `GEMINI_API_KEY` in the environment variables.
   - **Dockerfile path**: `backend/Dockerfile`.
   - **Build context**: `backend`.
3. Render will build the Docker image from `backend/Dockerfile` and run your FastAPI container.  
4. Copy the URL that Render assigns your service (e.g., `https://your-backend.onrender.com`) and use that as your `BACKEND_URL` in the frontend.

---

## License

This project is provided under an open-source license of your choice (e.g., MIT, Apache-2.0). Make sure to include a `LICENSE` file if you intend for it to be open source.

---

## Contact

If you have questions or issues:

- **GitHub Issues**: [Open an issue](https://github.com/your-username/Multi-Agentic-Real-Estate-Chatbot/issues).  
- **Contributions**: Feel free to open pull requests.

---

**Enjoy your Multi-Agentic Real Estate Copilot!**
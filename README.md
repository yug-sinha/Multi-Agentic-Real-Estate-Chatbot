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
8. [Additional README/Documentation](#additional-readme--documentation)

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
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
```

- **`GEMINI_API_KEY`** is your Google Gemini key.  
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

## Additional README / Documentation

Below is a concise **README/Documentation** covering core points of the Multi-Agentic Real Estate Chatbot, along with instructions for resending this document.

---

### Multi-Agentic Real Estate Chatbot

#### 1. Introduction

This chatbot offers property issue detection and tenancy-related advice, leveraging AI-driven logic. It comprises:
- **Backend**: FastAPI and Python  
- **Frontend**: Next.js (TypeScript) for the user interface  
- **AI Services**: Google Gemini API for image-driven analysis  
- **Deployment Options**: Dockerized backend, deployable on Render or similar cloud platforms; frontend deployable on Vercel

---

#### 2. Tools/Technologies Used

1. **FastAPI (Python)**: Provides REST endpoints to handle user requests.  
2. **Next.js (TypeScript)**: Frontend for user interaction and chat interface.  
3. **Docker**: Containerizes the FastAPI backend for consistent deployment.  
4. **Google Gemini API**: Processes images (upload + analysis) and advanced text generation (property/tenancy insights).  
5. **Tailwind CSS**: For styling the Next.js app quickly and consistently.

---

#### 3. Logic Behind Agent Switching

- **Property Agent**: Activated whenever a user uploads an image (or continues a discussion about property damage). It analyzes images for property issues like mold, cracks, or water damage.  
- **Tenancy Agent**: Activated when no file is provided. This agent handles legal/tenancy questions, referencing RAG (Retrieval-Augmented Generation) for location-specific or previously fetched knowledge.

Essentially:
1. If an **image** is included, route to **Property Agent**.  
2. If **no image** is included, route to **Tenancy Agent** (unless the conversation is a follow-up to a property discussion).

---

#### 4. How Image-Based Issue Detection Works

1. **User Uploads an Image**: The frontend sends the image to the FastAPI backend.  
2. **FastAPI** calls **Google’s Gemini API** to upload and process the file, then requests an AI-driven analysis.  
3. **Property Agent** forms a prompt describing the property context and queries the AI model for potential issues, e.g., mold spots, cracks, broken fixtures.  
4. **Short, Actionable Answer**: The response is limited to around 100 words, providing quick, targeted advice.

---

#### 5. Use Case Examples

1. **Landlord/Tenant Disputes**: User queries about deposit refunds or lease terms, Tenancy Agent returns legal guidelines or steps to resolve.  
2. **Home Damage**: User uploads pictures of water damage or wall cracks; Property Agent returns probable cause and recommended repairs.  
3. **Maintenance Questions**: E.g., “The sink is leaking. What should I do next?” The bot can guide them on next steps, referencing prior context.  
4. **Mold Identification**: The user snaps a photo of mold on a wall, gets quick advice on cleaning or professional help.

---

#### 6. Deadline

- **Deadline:** All tasks must be completed **48 hours** after receiving this document.

---

#### 7. Resending This Document

When you resend or submit this document, please **include** the following information:

1. **THE TOOL USED**: Which AI / cloud / container service you utilized.  
2. **The Place Where It Is Deployed**: Provide the URL or deployment environment (e.g., Vercel domain, Render link).  
3. **Steps to View the Bot (if there is code)**: Short instructions on how someone can clone and run it, or how they can try it online.  
4. **A Small Video of How the Bot Works** (Google Drive link, accessible to all): Demonstrate key features, e.g., uploading an image or asking a tenancy question.

---

**Thank you!** You now have a high-level overview of the Multi-Agentic Real Estate Chatbot, the logic behind agent switching, image-based detection flow, and use-case examples.

---

## Contact

If you have questions or issues:

- **GitHub Issues**: [Open an issue](https://github.com/your-username/Multi-Agentic-Real-Estate-Chatbot/issues).  
- **Contributions**: Feel free to open pull requests.

**Enjoy your Multi-Agentic Real Estate Copilot!**
```

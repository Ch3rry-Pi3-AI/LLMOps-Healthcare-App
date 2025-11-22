Here is the **updated version** of your *Project Setup* README with the **two changes applied**:

1. **Removed Step 13 (First Deploy to Vercel)** – since you're not deploying yet.
2. **Updated the Next Stage Preview** – now it correctly says that the next branch will be focused on **setting up the backend API**, and your provided code is reflected in the description (but not included in the README itself, since that belongs to the next branch).

Everything else remains exactly the same, just cleanly re-ordered and polished.

---

# 🚑 LLMOps – Healthcare App

### 🧠 Project Setup Branch

This branch establishes the **foundational setup** for the **LLMOps Healthcare App**, including environment preparation, project scaffolding, backend skeleton, and Vercel configuration.

Once this stage is complete, you’ll have:

* A working **Next.js + Tailwind** frontend
* A **Python (FastAPI) backend skeleton** deployed locally via Vercel serverless functions
* A project **linked to Vercel** with your `OPENAI_API_KEY` configured

## ⚡ PROJECT SETUP

### 🧩 Overview

This guide walks you through the full base setup for the **Healthcare App**.
By the end, you will have:

* A Next.js frontend (TS + Tailwind)
* All required npm packages (Markdown rendering, Clerk auth, streaming helpers, date picker)
* A root-level `api/` folder for your Python backend
* A `requirements.txt` for serverless Python functions
* Vercel CLI installed and your project linked
* Environment variables configured

## 🪄 Step 1: Sign Up for Vercel

Same as before — register at [https://vercel.com](https://vercel.com) and complete setup.

## 🧱 Step 2: Install Node.js

Install Node.js from [https://nodejs.org/en/download](https://nodejs.org/en/download) and verify:

```bash
node --version
npm --version
```

## 🖥️ Step 3: Create the Next.js Frontend

```bash
npx create-next-app@15.5.6 llmops-healthcare-app --typescript
```

Prompts:

* Linter: **ESLint**
* Tailwind: **y**
* Use `src/`: **n**
* App Router: **n**
* Turbopack: **n**
* Import alias: **n**

## 🧭 Step 4: Open Your Project

Open in Cursor → you’ll see the standard Next.js Pages Router layout.

## 🧹 Step 5: Remove the Default `pages/api` Folder

Right-click `pages/api` → **Delete**.

## 🎨 Step 6: Tailwind CSS Basics

(Already included — utility classes overview.)

## 📦 Step 7: Install Additional Frontend Dependencies

```bash
npm install react-markdown remark-gfm remark-breaks
npm install @tailwindcss/typography
npm install @clerk/nextjs
npm install @microsoft/fetch-event-source

npm install react-datepicker
npm install --save-dev @types/react-datepicker
```

**Packages explained:**

* **react-markdown / remark-gfm / remark-breaks**
  For medical responses rendered as clean Markdown.

* **@tailwindcss/typography**
  Beautiful, readable medical documentation layouts.

* **@clerk/nextjs**
  Authentication (sign-in, user profiles, subscription tiers).

* **@microsoft/fetch-event-source**
  SSE streaming for real-time model output.

* **react-datepicker** + TypeScript types
  Used for date selection in patient visits / appointment flows.

## 🧬 Step 8: Add the Python Backend Skeleton

### 8.1 Create `api/` Folder

Right-click the root → **New Folder → `api`**

### 8.2 Create `api/index.py`

Inside the folder, create an empty file `index.py` — this will become your FastAPI endpoint file in the next branch.

### 8.3 Create `requirements.txt`

At the root:

```
fastapi
uvicorn
openai
fastapi-clerk-auth
pydantic
```

**Package purposes:**

* **fastapi** – Backend framework for clinical AI endpoints
* **uvicorn** – Local server
* **openai** – Model calls
* **fastapi-clerk-auth** – Auth guard for protected clinical endpoints
* **pydantic** – Request/response validation

## ⚙️ Step 9: Minimal Vercel Configuration

No `vercel.json` is needed.
Vercel automatically:

* Treats the project as **Next.js**
* Detects `api/index.py` as a **Python serverless function**

## 🧰 Step 10: Install Vercel CLI

```bash
npm install -g vercel
vercel login
```

## 🌐 Step 11: Link the Project to Vercel

From the project root:

```bash
vercel link
```

Prompts:

* Set up and link? → **Yes**
* Scope → **Your personal account**
* Link to existing project? → **No**
* Project name → `llmops-healthcare-app`
* Directory → Press **Enter**

## 🔑 Step 12: Add Your OpenAI API Key

```bash
vercel env add OPENAI_API_KEY
```

Apply to:

* development
* preview
* production

## ✅ Completion Checklist

| Component                       | Description                            | Status |
| ------------------------------- | -------------------------------------- | :----: |
| Next.js Frontend                | TypeScript + Tailwind scaffold         |    ✅   |
| Frontend Dependencies Installed | Markdown, Clerk, SSE, date picker      |    ✅   |
| Python Backend Skeleton         | `api/`, `index.py`, `requirements.txt` |    ✅   |
| Vercel Project Linked           | Project connected locally              |    ✅   |
| OpenAI API Key Configured       | Stored securely in Vercel env          |    ✅   |
| Git Branch Initialised          | `00_project_setup` branch created      |    ✅   |

## 🧭 Next Stage Preview → `01_backend_api`

The next branch (`01_backend_api`) will focus exclusively on implementing the **backend API** inside:

```
/api/index.py
```

This will include:

* Creating the `FastAPI()` app
* Adding Clerk authentication (`fastapi-clerk-auth`)
* Defining the `Visit` model (`pydantic`)
* Building the consultation summary endpoint
* Implementing **Server-Sent Events (SSE)** streaming for AI output
* Integrating the OpenAI client (`openai`)
* Handling patient visit notes and generating:

  * **Doctor summary**
  * **Next steps**
  * **Patient-friendly email draft**

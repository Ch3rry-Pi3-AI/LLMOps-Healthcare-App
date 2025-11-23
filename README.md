# 🏥 **LLMOps Healthcare App — Main Project Overview**

The **LLMOps Healthcare App** is an end-to-end SaaS that provides clinicians with **AI-powered consultation summaries**, **next-step recommendations**, and **patient-friendly email drafts** from raw consultation notes.

This system integrates:

* ⚛️ **Next.js (Pages Router)** frontend
* 🧠 **OpenAI GPT-5-Nano** for real-time token streaming
* 🔐 **Clerk authentication + subscription billing**
* 🐍 **FastAPI serverless backend** deployed on Vercel
* 📡 **SSE (Server-Sent Events)** for live streaming
* 🎨 **Tailwind CSS** for the UI

Clinicians can sign up, subscribe, and immediately generate structured documentation to speed up their clinical workflows.

## 🎥 **Application Walkthrough**

### 🔑 1. User Sign-Up Flow

<p align="center">
  <img src="img/app/sign_up.gif" width="100%" alt="User Sign Up Demo">
</p>

### 💳 2. Subscription Selection & Checkout

<p align="center">
  <img src="img/app/subscription.gif" width="100%" alt="Subscription Demo">
</p>

### 📝 3. Real-Time Consultation Summary Generation

<p align="center">
  <img src="img/app/notes_generation.gif" width="100%" alt="Notes Generation Demo">
</p>

## 🧩 **Grouped Stages**

|  Stage | Category                      | Description                                                             |
| :----: | ----------------------------- | ----------------------------------------------------------------------- |
| **00** | Project Setup                 | Next.js scaffold, Vercel linking, backend folder creation, global deps  |
| **01** | Backend API                   | Implemented `api/index.py`, FastAPI SSE streaming, OpenAI integration   |
| **02** | App Configuration             | Added global providers & metadata in `_app.tsx` and `_document.tsx`     |
| **03** | Consultation Form             | Created `product.tsx` with form UI, Clerk JWT useAuth, fetchEventSource |
| **04** | Landing Page                  | Designed full marketing page with auth-aware CTAs (`index.tsx`)         |
| **05** | Authentication & Subscription | Clerk sign-in, JWT, premium gating, Billing, PricingTable fallback      |

## 🗂️ **Project Structure**

```
llmops-healthcare-app/
├── api/
│   └── index.py                  # FastAPI backend (SSE streaming)
├── img/
├── pages/
│   ├── _app.tsx                  # Global providers (Clerk + styles)
│   ├── _document.tsx             # App-wide metadata HTML wrapper
│   ├── index.tsx                 # Landing page (marketing + auth-aware CTAs)
│   └── product.tsx               # Premium consultation assistant
├── styles/
│   └── globals.css
├── public/
├── requirements.txt              # Python deps (FastAPI, Clerk Auth, OpenAI)
├── package.json
├── tsconfig.json
└── next.config.js
```

## 💡 **Key Components**

### 🔐 Clerk Authentication & Billing

* Sign-up/sign-in modal
* JWT available via `useAuth().getToken()`
* Premium gating via:

  ```jsx
  <Protect plan="premium_subscription">
  ```
* Billing, checkout, and subscription state handled automatically

### 📡 SSE Streaming Backend

* FastAPI serverless route at `/api`
* GPT-5-Nano streamed using `client.chat.completions.create(stream=True)`
* EventSource-compatible SSE generator

### 🎨 Frontend (Next.js)

* Pages Router for simplicity
* Tailwind for styling
* ReactMarkdown to render GPT output

## 💻 **Local Development**

Install:

```bash
npm install
```

Run frontend:

```bash
npm run dev
```

Run serverless backend locally:

```bash
vercel dev
```

## ☁️ **Deploying to Production**

To deploy for the first time:

```bash
vercel .
```

This builds the full Next.js app + backend and publishes directly to **production**.

### Updating Production Afterwards

```bash
vercel --prod
```

## 🎉 **Project Complete**

The application is now fully deployed and production-ready, with:

* Authentication
* Subscription gating
* Real-time AI streaming
* Full clinical UI
* Secure backend

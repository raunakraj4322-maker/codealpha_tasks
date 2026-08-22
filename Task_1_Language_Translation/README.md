# CodeAlpha - AI Language Translation Tool

![CodeAlpha Internship Project](https://img.shields.io/badge/CodeAlpha-AI%20Internship-blue?style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Express.js](https://img.shields.io/badge/Express.js-404D59?style=for-the-badge&logo=express&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

A full-stack, production-grade **AI Language Translation Tool** built for the **CodeAlpha Artificial Intelligence Internship**. The tool provides instant neural machine translation across 25+ global and Indian regional languages, equipped with real-time text-to-speech synthesis, auto-detection, copy-to-clipboard, translation history, and multi-provider translation API support.

---

## 🌟 Task Requirements & Features

### Core Task Requirements Checklist
- [x] **User Interface**: Intuitive modern UI to enter source text with character counting (0 / 5000).
- [x] **Language Selection**: Source language dropdown (with Auto-Detect support) and Target language dropdown.
- [x] **Language Swap**: Working swap button (`English → Hindi` to `Hindi → English`) with state persistence.
- [x] **Real Translation API**: Multi-provider integration (Google Cloud Translate v2, Microsoft Azure Translator, LibreTranslate, and zero-config MyMemory fallback). No fake or hardcoded mock responses.
- [x] **Copy to Clipboard**: One-click copying with visual toast feedback ("Copied!").
- [x] **Text-to-Speech (TTS)**: Web Speech API integration for both source text and target translations.
- [x] **Clean & Responsive UI**: Responsive design for Mobile, Tablet, and Desktop with Dark/Light mode toggle.
- [x] **Security**: Backend proxy ensuring API keys and credentials are never exposed to client browsers.

---

## 🏗️ Architecture Overview

```
                      ┌────────────────────────────────────────┐
                      │            Browser Client              │
                      │  React + TypeScript + Tailwind CSS     │
                      └──────────────────┬─────────────────────┘
                                         │
                                         │ HTTP POST /api/translate
                                         ▼
                      ┌────────────────────────────────────────┐
                      │          Backend Node/Express API      │
                      │  Rate Limiting • CORS • Helmet • Input  │
                      └──────────────────┬─────────────────────┘
                                         │
                     ┌───────────────────┼───────────────────┐
                     ▼                   ▼                   ▼
           ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
           │   Google Cloud   │ │ Microsoft Azure  │ │ MyMemory API     │
           │   Translate v2   │ │    Translator    │ │ (Zero-Config)    │
           └──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript & Vite
- **Styling**: Tailwind CSS, PostCSS, Autoprefixer
- **Icons**: Lucide React
- **Browser APIs**: Web Speech API (SpeechSynthesis), Clipboard API, LocalStorage

### Backend
- **Runtime**: Node.js with TypeScript & `ts-node-dev`
- **Framework**: Express.js
- **Security**: Helmet, CORS, Express Rate Limit
- **HTTP Client**: Axios

---

## 📁 Directory Structure

```
CodeAlpha_LanguageTranslationTool/
├── frontend/                     # React + Vite Frontend Application
│   ├── src/
│   │   ├── components/           # UI Components (Header, LanguageSelector, TranslationCard, etc.)
│   │   ├── services/             # API client services
│   │   ├── data/                 # Language catalog & BCP-47 speech mappings
│   │   ├── hooks/                # Web Speech API & LocalStorage history hooks
│   │   ├── types/                # TypeScript interfaces
│   │   ├── App.tsx               # Main application component
│   │   ├── main.tsx              # React entry point
│   │   └── index.css             # Tailwind base styles
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── package.json
│
├── backend/                      # Express.js Backend Service
│   ├── src/
│   │   ├── config/               # Centralized configuration & env parser
│   │   ├── middleware/           # Rate limiting, validation, error handler
│   │   ├── services/             # Multi-provider translation service strategy
│   │   ├── routes/               # API endpoints (/api/translate, /api/languages, /api/health)
│   │   └── server.ts             # Express server entry point
│   ├── tsconfig.json
│   └── package.json
│
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git protection rules
├── package.json                  # Root concurrent launcher package
└── README.md                     # Documentation
```

---

## ⚙️ Prerequisites

- **Node.js**: `v18.0.0` or higher
- **npm**: `v9.0.0` or higher

---

## 🚀 Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool
```

### 2. Install All Dependencies
Run the root setup command to install dependencies for both frontend and backend:
```bash
npm run setup
```

### 3. Environment Variable Configuration

Create a `.env` file in the root directory (or copy `.env.example`):
```bash
cp .env.example .env
```

Edit `.env` to configure your preferred settings:
```env
PORT=5000
NODE_ENV=development
CLIENT_URL=http://localhost:5173

# Options: 'mymemory' (default zero-config), 'google', 'azure', 'libretranslate'
TRANSLATION_PROVIDER=mymemory

# Optional: Google Cloud Translation API Key
GOOGLE_TRANSLATE_API_KEY=

# Optional: Microsoft Azure Translator Key
AZURE_TRANSLATOR_KEY=
AZURE_TRANSLATOR_REGION=global
```

> 💡 **Zero-Config Default**: If `TRANSLATION_PROVIDER` is set to `mymemory` (or no API key is provided), the application automatically uses the free public MyMemory Translation API, allowing you to test real machine translations immediately without creating paid accounts!

---

## 🔑 How to Obtain API Keys

### Option A: Google Cloud Translation API
1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the **Cloud Translation API**.
3. Go to **APIs & Services > Credentials** and create an **API Key**.
4. Set in `.env`:
   ```env
   TRANSLATION_PROVIDER=google
   GOOGLE_TRANSLATE_API_KEY=your_actual_google_api_key_here
   ```

### Option B: Microsoft Azure Translator
1. Visit the [Azure Portal](https://portal.azure.com/).
2. Create a **Translator** resource.
3. Copy **Key 1** and the **Region** under **Keys and Endpoint**.
4. Set in `.env`:
   ```env
   TRANSLATION_PROVIDER=azure
   AZURE_TRANSLATOR_KEY=your_actual_azure_key_here
   AZURE_TRANSLATOR_REGION=global
   ```

---

## 🏃 Running the Application

### Start Both Frontend and Backend Concurrently (Recommended)
```bash
npm run dev
```
- **Frontend App**: `http://localhost:5173`
- **Backend API**: `http://localhost:5000`

### Start Services Individually

**Backend**:
```bash
npm run dev:backend
```

**Frontend**:
```bash
npm run dev:frontend
```

---

## 📡 API Endpoint Documentation

### `POST /api/translate`
Translates source text into the requested target language.

**Request Body**:
```json
{
  "text": "Hello world, welcome to CodeAlpha!",
  "sourceLanguage": "en",
  "targetLanguage": "hi"
}
```

**Response (200 OK)**:
```json
{
  "translatedText": "नमस्ते दुनिया, कोडअल्फा में आपका स्वागत है!",
  "sourceLanguage": "en",
  "targetLanguage": "hi",
  "provider": "MyMemory Translate",
  "timestamp": "2026-08-22T13:15:00.000Z"
}
```

### `GET /api/languages`
Returns list of supported languages.

### `GET /api/health`
Health check endpoint reporting API status and active provider engine.

---

## 🛡️ Security Considerations

1. **No Frontend API Key Exposure**: All requests to external translation providers pass through our Node.js backend. Private keys are never sent to or visible in client browser code.
2. **Git Protection**: `.gitignore` strictly ignores `.env`, `.env.*`, `node_modules/`, and build artifacts.
3. **Rate Limiting**: Express rate limiter protects endpoints from automated abuse (max 100 requests per 15 minutes per IP).
4. **Input Validation**: Backend validates text non-emptiness, maximum character length (5000 chars), and supported BCP-47 language codes.
5. **Sanitized Error Responses**: Internal stack traces or credential information are stripped before returning error payloads to clients.

---

## 📄 License

Distributed under the **MIT License**. Created by CodeAlpha Intern.

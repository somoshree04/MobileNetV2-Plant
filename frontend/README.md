

# 💻 Green Guard — Frontend

React + TypeScript single-page application for the Green Guard Plant Disease Scanner. Handles leaf image uploads and renders real-time model diagnostics from the FastAPI backend.

---

## Folder Structure

```
frontend/
├── src/
│   ├── assets/           # Static images and vectors
│   ├── App.tsx           # App state, file upload logic, API fetch
│   ├── App.css           # Component styles
│   ├── index.css         # Tailwind CSS directives
│   ├── main.tsx          # React DOM mount
│   └── types.ts          # TypeScript interfaces matching backend Pydantic models
├── public/               # Favicons and static assets
├── index.html            # SPA entry point
├── tailwind.config.js    # Color palette and layout extensions
├── vite.config.ts        # Dev server config and port forwarding
├── postcss.config.js     # CSS post-processing pipeline
├── eslint.config.js      # Linting rules
└── package.json          # Dependencies and build scripts
```

---

## Local Development

```bash
npm install     # Install dependencies
npm run dev     # Start Vite dev server with HMR
```

App runs at **`http://127.0.0.1:5173`**

---

## API Connection

`src/App.tsx` sends image uploads to:

```
POST http://127.0.0.1:8000/api/v1/predict
```

If requests hang or fail, confirm:
1. The backend FastAPI server is running in its own terminal (`uvicorn main:app --reload`)
2. The backend port matches (`8000`) on both ends
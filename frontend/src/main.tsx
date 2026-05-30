
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css' // Imports Tailwind utility classes

// In JavaScript, document.getElementById can theoretically return null if 'root' doesn't exist.
// TypeScript flags this as dangerous. We use 'as HTMLElement' to explicitly assert 
// to the compiler that this DOM element structurally exists.
ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
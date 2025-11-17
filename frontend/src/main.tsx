import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { enableMocking } from './mocks'

// Note: StrictMode temporarily disabled for production build
// import { StrictMode } from 'react'

// Enable mock server if VITE_USE_MOCKS=true
enableMocking().then(() => {
  createRoot(document.getElementById('root')!).render(
    <App />
  )
})

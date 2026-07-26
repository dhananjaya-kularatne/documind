import { useState, useEffect } from "react"

// Key used to store the session ID in the browser's localStorage.
const STORAGE_KEY = "documind_session_id"

// Custom hook that manages a persistent session ID for this browser. On first load, checks localStorage for an existing session ID.
// If none exists yet, sessionId starts as null — it gets set later, once the backend actually creates a session (e.g. after the first upload).
export function useSessionId() {
  const [sessionId, setSessionIdState] = useState(null)

  // Runs once when the hook is first used — loads any existing session ID.
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      setSessionIdState(stored)
    }
  }, [])

  // Call this after the backend returns a session_id (e.g. from an upload response).
  // Saves it to localStorage AND updates component state, so future page loads and future components using this hook both see the same session ID.
  function setSessionId(id) {
    localStorage.setItem(STORAGE_KEY, id)
    setSessionIdState(id)
  }

  // Clears the stored session — useful for a "start new session" button later.ok
  function clearSessionId() {
    localStorage.removeItem(STORAGE_KEY)
    setSessionIdState(null)
  }

  return { sessionId, setSessionId, clearSessionId }
}
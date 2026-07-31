import { useState, useEffect } from "react"
import UploadPage from "./pages/UploadPage"
import ChatPage from "./pages/ChatPage"
import { getSessionDocuments } from "./api/documents"
import { useSessionId } from "./hooks/useSessionId"

// Top-level app component — toggles between the upload screen and chat screen. uploadedDocs lives here so both screens see the same, accurate document list —
// fetched from the backend on load, not just accumulated from local uploads.
function App() {
  const [currentScreen, setCurrentScreen] = useState("upload")
  const [uploadedDocs, setUploadedDocs] = useState([])
  const { sessionId } = useSessionId()

  // Whenever we have a sessionId (e.g. on page load, from a previous visit), fetch the real document list for it from the backend.
  useEffect(() => {
    if (sessionId) {
      getSessionDocuments(sessionId)
        .then(setUploadedDocs)
        .catch(() => setUploadedDocs([]))
    }
  }, [sessionId])

  return (
    <div>
      {currentScreen === "upload" ? (
        <UploadPage
          onContinue={() => setCurrentScreen("chat")}
          uploadedDocs={uploadedDocs}
          setUploadedDocs={setUploadedDocs}
        />
      ) : (
        <ChatPage
          onBack={() => setCurrentScreen("upload")}
          uploadedDocs={uploadedDocs}
          setUploadedDocs={setUploadedDocs}
        />
      )}
    </div>
  )
}

export default App
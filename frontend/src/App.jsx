import { useState } from "react"
import UploadPage from "./pages/UploadPage"
import ChatPage from "./pages/ChatPage"

// Top-level app component — toggles between the upload screen and chat screen.
// uploadedDocs lives here so ChatPage can also display the list of documents in the current session, in its sidebar.
function App() {
  const [currentScreen, setCurrentScreen] = useState("upload")
  const [uploadedDocs, setUploadedDocs] = useState([])

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
        />
      )}
    </div>
  )
}

export default App
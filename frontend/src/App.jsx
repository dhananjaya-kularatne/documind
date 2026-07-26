import { useState } from "react"
import UploadPage from "./pages/UploadPage"
import ChatPage from "./pages/ChatPage"

// Top-level app component — toggles between the upload screen and chat screen.
// Using simple state here rather than a router, since this is only two screens.
function App() {
  // Start on the upload screen; user can switch to chat once they've uploaded something.
  const [currentScreen, setCurrentScreen] = useState("upload")

  return (
    <div>
      {currentScreen === "upload" ? (
        <UploadPage onContinue={() => setCurrentScreen("chat")} />
      ) : (
        <ChatPage onBack={() => setCurrentScreen("upload")} />
      )}
    </div>
  )
}

export default App
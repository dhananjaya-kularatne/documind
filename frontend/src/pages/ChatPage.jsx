import { useState } from "react"
import Citation from "../components/Citation"
import { deleteDocument } from "../api/documents"
import { useSessionId } from "../hooks/useSessionId"

// The chat screen — lets the user ask questions about documents already uploaded in their current session, and shows grounded answers with citations back to the source document + page.
function ChatPage({ onBack, uploadedDocs, setUploadedDocs }) {
  const { sessionId } = useSessionId()
  const [question, setQuestion] = useState("")
  const [messages, setMessages] = useState([])
  const [isAsking, setIsAsking] = useState(false)
  

  async function handleAsk() {
    if (!question.trim() || !sessionId) return

    const currentQuestion = question
    setQuestion("")
    setIsAsking(true)

    // Add the user's question to the conversation immediately, so it appears right away rather than waiting on the API response.
    setMessages((prev) => [...prev, { role: "user", content: currentQuestion }])

    try {
      const result = await askQuestion(sessionId, currentQuestion)

      // Add the assistant's answer, along with its source citations.
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result.answer, sources: result.sources },
      ])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Something went wrong answering that. Please try again.", sources: [] },
      ])
    } finally {
      setIsAsking(false)
    }
  }

  // Allow pressing Enter to submit, same as clicking the send button.
  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault()
      handleAsk()
    }
  }


  // Removes a document from the session — mirrors the same logic used on the upload screen.
  async function handleDeleteDocument(documentId) {
    try {
      await deleteDocument(documentId, sessionId)
      setUploadedDocs((prev) => prev.filter((doc) => doc.document_id !== documentId))
    } catch (err) {
      console.error("Failed to delete document", err)
    }
  }

  return (
  <div className="min-h-screen bg-[#FAF9F6] flex">
    {/* Sidebar listing documents in this session */}
    <div className="w-56 border-r border-[#DDD9D2] p-4 hidden md:block">
      <h2 className="text-xs font-mono text-[#6B6862] mb-3">This session</h2>
      {uploadedDocs.map((doc) => (
        <div key={doc.document_id} className="group flex items-center justify-between py-1.5 text-xs">
          <span className="text-[#1C1B1A] truncate mr-1">{doc.filename}</span>
          <div className="flex items-center gap-1 shrink-0">
            <span className="font-mono text-[10px] text-[#1C1B1A] bg-[#FFD84D] px-1 py-0.5 rounded">
              {doc.page_count}p
            </span>
            <button
              onClick={() => handleDeleteDocument(doc.document_id)}
              className="opacity-0 group-hover:opacity-100 text-[#6B6862] cursor-pointer hover:text-red-600 transition-opacity"
              aria-label="Remove document"
            >
              ✕
            </button>
          </div>
        </div>
      ))}
    </div>

    <div className="flex-1 flex flex-col">
      <header className="border-b border-[#DDD9D2] px-4 py-3 flex items-center justify-between">
        <h1 className="font-serif text-lg font-medium text-[#1C1B1A]">DocuMind</h1>
        <button onClick={onBack} className="text-xs text-[#6B6862] cursor-pointer hover:text-[#2A5B8C]">
          ← Upload more
        </button>
      </header>

      {/* Message list */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3 max-w-2xl mx-auto w-full">
        {messages.map((msg, i) =>
          msg.role === "user" ? (
            <div key={i} className="self-end max-w-[78%] bg-[#2A5B8C] text-[#FAF9F6] px-3 py-2 rounded text-sm">
              {msg.content}
            </div>
          ) : (
            <div key={i} className="self-start max-w-[85%] bg-white border border-[#DDD9D2] px-3 py-2 rounded">
              <p className="text-sm text-[#1C1B1A] mb-2">{msg.content}</p>
              <div>
                {msg.sources.map((source, j) => (
                  <Citation key={j} filename={source.filename} page={source.page} />
                ))}
              </div>
            </div>
          )
        )}
      </div>

      {/* Input bar */}
      <div className="border-t border-[#DDD9D2] p-3 flex gap-2 max-w-2xl mx-auto w-full">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about this document"
          disabled={isAsking}
          className="flex-1 h-8 border border-[#DDD9D2] rounded px-2.5 text-sm bg-white"
        />
        <button
          onClick={handleAsk}
          disabled={isAsking || !question.trim()}
          className="w-8 h-8 bg-[#2A5B8C] rounded text-[#FAF9F6] cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
          aria-label="Send"
        >
          ↑
        </button>
      </div>
    </div>
  </div>
)
}

export default ChatPage
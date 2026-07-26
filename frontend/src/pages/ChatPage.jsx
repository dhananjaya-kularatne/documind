import { useState } from "react"
import { askQuestion } from "../api/documents"
import { useSessionId } from "../hooks/useSessionId"
import Citation from "../components/Citation"

// The chat screen — lets the user ask questions about documents already uploaded in their current session, and shows grounded answers with citations back to the source document + page.
function ChatPage({onBack}) {
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

  return (
    <div className="min-h-screen bg-[#FAF9F6] flex flex-col">
      <header className="border-b border-[#DDD9D2] px-4 py-3 flex items-center justify-between">
        <h1 className="font-serif text-lg font-medium text-[#1C1B1A]">DocuMind</h1>
        <button onClick={onBack} className="text-xs text-[#6B6862] hover:text-[#2A5B8C]">
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
          className="w-8 h-8 bg-[#2A5B8C] rounded text-[#FAF9F6] disabled:opacity-40"
          aria-label="Send"
        >
          ↑
        </button>
      </div>
    </div>
  )
}

export default ChatPage
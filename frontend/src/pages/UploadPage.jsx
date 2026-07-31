import { useState, useRef } from "react"
import { useSessionId } from "../hooks/useSessionId"
import { uploadDocuments, deleteDocument } from "../api/documents"

// The main upload screen — lets a user select one or more PDFs, uploads them to the backend, and stores the returned session ID.
function UploadPage({onContinue, uploadedDocs, setUploadedDocs}) {
  const { sessionId, setSessionId, clearSessionId } = useSessionId()
  const [selectedFiles, setSelectedFiles] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState(null)

  // Ref to the hidden file input, so we can trigger it programmatically when the user clicks anywhere on the dropzone.
  const fileInputRef = useRef(null)

  // Called when the user picks files via the file picker.
  function handleFileSelect(event) {
    const files = Array.from(event.target.files)
    setSelectedFiles(files)
  }

  // Clears the current session entirely — both the stored ID and the locally-tracked document list — so the next upload starts completely fresh.
  function handleStartNewSession() {
    clearSessionId()
    setUploadedDocs([])
  }

// Removes a single document from the session — both from the backend (Chroma + MongoDB) and from the locally-displayed list.
async function handleDeleteDocument(documentId) {
  try {
    await deleteDocument(documentId, sessionId)
    setUploadedDocs((prev) => prev.filter((doc) => doc.document_id !== documentId))
  } catch (err) {
    setError("Failed to remove document.")
  }
}

  // Sends the selected files to the backend.
  async function handleUpload() {
    if (selectedFiles.length === 0) return

    setIsUploading(true)
    setError(null)

    try {
      // Pass the existing sessionId if we have one (adds to the same session), or null if this is the user's first upload (backend creates a new session).
      const results = await uploadDocuments(selectedFiles, sessionId)

      // Every result in the array shares the same session_id — just grab it from the first.
      setSessionId(results[0].session_id)

      // Add the newly uploaded docs to whatever was already uploaded this session.
      setUploadedDocs((prev) => [...prev, ...results])
      setSelectedFiles([])
    } catch (err) {
      setError("Upload failed. Please try again.")
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#FAF9F6] flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-md text-center">
        <h1 className="font-serif text-2xl font-medium text-[#1C1B1A] mb-1">
          DocuMind
        </h1>
        <p className="text-sm text-[#6B6862] mb-8">
          Upload a PDF and ask it questions.
        </p>

        {/* Hidden native file input — triggered by clicking the dropzone below */}
        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf"
          multiple
          onChange={handleFileSelect}
          className="hidden"
        />u

        {/* Clickable dropzone area */}
        <div
          onClick={() => fileInputRef.current.click()}
          className="border border-dashed border-[#DDD9D2] rounded p-12 cursor-pointer hover:border-[#2A5B8C] transition-colors"
        >
          <p className="text-sm font-medium text-[#1C1B1A]">
            {selectedFiles.length > 0
              ? `${selectedFiles.length} file(s) selected`
              : "Drop a PDF here"}
          </p>
          <p className="text-xs text-[#6B6862] mt-1">or click to browse</p>
        </div>

        {error && (
          <p className="text-xs text-red-600 mt-3">{error}</p>
        )}

        <button
          onClick={handleUpload}
          disabled={selectedFiles.length === 0 || isUploading}
          className="mt-5 w-full h-9 bg-[#2A5B8C] text-[#FAF9F6] rounded text-sm font-medium cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {isUploading ? "Uploading..." : "Upload document"}
        </button>

        {uploadedDocs.length > 0 && (
      <div className="mt-7 text-left border-t border-[#DDD9D2] pt-4">
        <div className="flex items-center justify-between mb-2">
          <p className="text-xs font-mono text-[#6B6862]">This session</p>
          <button
            onClick={handleStartNewSession}
            className="text-xs text-[#6B6862] cursor-pointer hover:text-red-600"
          >
            Start new session
          </button>
        </div>
        {uploadedDocs.map((doc) => (
        <div
          key={doc.document_id}
          className="group flex items-center justify-between py-1.5 text-sm"
        >
          <span className="text-[#1C1B1A] truncate mr-2">{doc.filename}</span>
          <div className="flex items-center gap-1.5 shrink-0">
            <span className="font-mono text-xs text-[#1C1B1A] bg-[#FFD84D] px-1.5 py-0.5 rounded">
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
    )}
      </div>
      {uploadedDocs.length > 0 && (
      <div className="mt-4 text-center">
        <button
          onClick={onContinue}
          className="text-sm text-[#2A5B8C] font-medium cursor-pointer hover:underline"
        >
          Continue to chat →
        </button>
      </div>
    )}
    </div>
  )
}

export default UploadPage
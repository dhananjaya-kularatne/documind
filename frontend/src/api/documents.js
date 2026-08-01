
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

// Uploads one or more PDF files into a session.
// If sessionId is null/undefined, the backend generates a new one and returns it.
export async function uploadDocuments(files, sessionId) {
  const formData = new FormData()

  // Append each file under the same "files" field name — this matches FastAPI's List[UploadFile] on the backend.
  for (const file of files) {
    formData.append("files", file)
  }

  // Only include session_id if we already have one (returning user).
  if (sessionId) {
    formData.append("session_id", sessionId)
  }

  const response = await fetch(`${API_BASE_URL}/documents`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    // Read the backend's specific error message (e.g. the upload-limit messages)
    // instead of showing a generic failure.
    const errorData = await response.json().catch(() => null)
    throw new Error(errorData?.detail || "Failed to upload documents")
  }

  // Returns an array of DocumentResponse objects, one per uploaded file.
  return response.json()
}

// Asks a question against a session's documents.
// documentIds is optional — pass an array to search only specific documents, or omit/null to search everything uploaded in the session.
export async function askQuestion(sessionId, question, documentIds = null) {
  const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      document_ids: documentIds,
    }),
  })

  if (!response.ok) {
    throw new Error("Failed to get an answer")
  }

  return response.json()
}

// Fetches the true, authoritative list of documents in a session — directly from the backend/database, not from locally-tracked frontend state (which only reflects what was uploaded this page load).
export async function getSessionDocuments(sessionId) {
  const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/documents`)

  if (!response.ok) {
    throw new Error("Failed to fetch session documents")
  }

  return response.json()
}

// Removes a single document from a session — deletes its chunks from Chroma and its metadata record from MongoDB.
export async function deleteDocument(documentId, sessionId) {
  const response = await fetch(
    `${API_BASE_URL}/documents/${documentId}?session_id=${sessionId}`,
    { method: "DELETE" }
  )

  if (!response.ok) {
    throw new Error("Failed to delete document")
  }

  return response.json()
}
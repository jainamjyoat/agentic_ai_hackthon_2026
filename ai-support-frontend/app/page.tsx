"use client"

import { useState } from "react"

type Message = {
  role: "user" | "ai"
  text: string
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  // 🔥 Upload state
  const [file, setFile] = useState<File | null>(null)
  const [uploadStatus, setUploadStatus] = useState("")

  // 💬 Chat function
  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage: Message = { role: "user", text: input }

    setMessages(prev => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
          session_id: "user1"
        }),
      })

      const data = await res.json()

      const aiMessage: Message = {
        role: "ai",
        text:
          typeof data === "string"
            ? data
            : data.response || data.error || JSON.stringify(data)
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: "ai", text: "❌ Error connecting to server" }
      ])
    }

    setLoading(false)
  }

  // 📂 Upload function
  const handleUpload = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)
    setUploadStatus("Uploading...")

    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })

      const data = await res.json()
      setUploadStatus(data.message || "✅ Uploaded successfully")
    } catch {
      setUploadStatus("❌ Upload failed")
    }
  }

  return (
    <div className="min-h-screen bg-[#0f172a] text-white flex flex-col items-center p-6">
      <h1 className="text-2xl mb-6 font-bold">AI Support Agent</h1>

      {/* 🔥 FILE UPLOAD SECTION */}
      <div className="w-full max-w-2xl mb-4 bg-[#1e293b] p-4 rounded-lg shadow-md">
        <p className="mb-2 text-sm text-gray-400">Upload your JSON file:</p>

        <div className="flex gap-2">
          <input
            type="file"
            accept=".json"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="text-sm file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />

          <button
            onClick={handleUpload}
            disabled={!file} // Disables button if no file is selected
            className="bg-green-600 hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed px-4 py-2 rounded transition-colors font-medium"
          >
            Upload
          </button>
        </div>

        {uploadStatus && (
          <p className={`text-sm mt-2 ${uploadStatus.includes("❌") ? "text-red-400" : "text-green-400"}`}>
            {uploadStatus}
          </p>
        )}
      </div>

      {/* 💬 CHAT WINDOW */}
      <div className="w-full max-w-2xl h-[500px] overflow-y-auto space-y-4 p-4 bg-[#1e293b] rounded-lg shadow-md">
        {messages.length === 0 && (
          <p className="text-gray-500 text-center mt-20">Start a conversation...</p>
        )}
        
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`px-4 py-2 rounded-lg max-w-[70%] ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-700 text-gray-100"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
             <div className="px-4 py-2 rounded-lg bg-gray-700 text-gray-400 italic">
               🤖 Typing...
             </div>
          </div>
        )}
      </div>

      {/* ✍️ INPUT */}
      <div className="flex w-full max-w-2xl mt-4 gap-2">
        <input
          className="flex-1 p-3 rounded bg-white text-black focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()} // Allows sending with Enter key
          placeholder="Ask something..."
          disabled={loading}
        />

        <button
          onClick={sendMessage}
          disabled={!input.trim() || loading} // Disables if empty or currently loading
          className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-2 rounded font-medium transition-colors"
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  )
}
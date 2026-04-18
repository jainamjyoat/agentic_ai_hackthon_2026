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

  const sendMessage = async () => {
    if (!input) return

    const userMessage: Message = { role: "user", text: input }

    setMessages(prev => [...prev, userMessage])
    setInput("")
    setLoading(true)

    const res = await fetch("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        message: input,
        session_id: "user1"
      }),
    })

    const data = await res.json()

    const aiMessage: Message = {
      role: "ai",
      text: typeof data === "string"
      ? data
      : data.response || data.error || JSON.stringify(data)
    }

    setMessages(prev => [...prev, aiMessage])
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-[#0f172a] text-white flex flex-col items-center p-6">
      <h1 className="text-2xl mb-6 font-bold">AI Support Agent</h1>

      <div className="w-full max-w-2xl h-[500px] overflow-y-auto space-y-4 p-4 bg-[#1e293b] rounded-lg">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`px-4 py-2 rounded-lg max-w-[70%] ${
                msg.role === "user"
                  ? "bg-blue-500"
                  : "bg-gray-700"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <p className="text-gray-400 italic">🤖 Typing...</p>
        )}
      </div>

      <div className="flex w-full max-w-2xl mt-4 gap-2">
        <input
          className="flex-1 p-3 rounded bg-white text-black"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 px-4 rounded"
        >
          Send
        </button>
      </div>
    </div>
  )
}
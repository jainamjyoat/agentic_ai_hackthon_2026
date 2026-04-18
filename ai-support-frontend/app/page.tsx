"use client"

import { useState } from "react"

export default function Home() {
  const [message, setMessage] = useState("")
  const [chat, setChat] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!message) return

    setLoading(true)

    const res = await fetch("/api/chat", {
      method: "POST",
      body: JSON.stringify({ message }),
    })

    const data = await res.json()

    setChat(prev => [
      ...prev,
      "🧑 " + message,
      "🤖 " + (data.response || JSON.stringify(data))
    ])

    setMessage("")
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-black text-white p-10">
      <h1 className="text-2xl mb-4">AI Support Agent</h1>

      <div className="border p-4 h-[400px] overflow-y-auto mb-4">
        {chat.map((c, i) => (
          <p key={i} className="mb-2">{c}</p>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 p-2 text-black"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask something..."
        />

        <button
          onClick={sendMessage}
          className="bg-blue-500 px-4 py-2"
        >
          Send
        </button>
      </div>

      {loading && <p className="mt-2">Thinking...</p>}
    </div>
  )
}
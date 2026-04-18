import { NextResponse } from "next/server"

export async function POST(req: Request) {
  try {
    // 🔹 Parse incoming request
    const body = await req.json()

    if (!body.message) {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      )
    }

    console.log("➡️ Sending to backend:", body)

    // 🔹 Call Render backend
    const res = await fetch(process.env.BACKEND_URL!, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: body.message,
        session_id: body.session_id || "user1",
      }),
    })

    // 🔹 Read response safely
    const text = await res.text()
    console.log("⬅️ Backend raw response:", text)

    let data
    try {
      data = JSON.parse(text)
    } catch {
      // If backend returns non-JSON
      return NextResponse.json(
        { error: "Invalid JSON from backend", raw: text },
        { status: 500 }
      )
    }

    // 🔹 Handle backend errors
    if (!res.ok) {
      return NextResponse.json(
        { error: "Backend error", details: data },
        { status: res.status }
      )
    }

    // 🔹 Success response
    return NextResponse.json(data)

  } catch (error) {
    console.error("❌ Route error:", error)

    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
import { NextResponse } from "next/server"

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const url = process.env.BACKEND_URL + '/chat'

    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: body.message,
        session_id: body.session_id || "user1",
      }),
    })

    const data = await res.json()

    return NextResponse.json(data)

  } catch (error) {
    return NextResponse.json(
      { error: "Backend connection failed" },
      { status: 500 }
    )
  }
}
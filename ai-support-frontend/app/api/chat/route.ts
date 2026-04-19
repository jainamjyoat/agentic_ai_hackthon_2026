import { NextResponse } from "next/server"

export async function POST(req: Request) {
  try {
    const body = await req.json()

    const res = await fetch(process.env.BACKEND_URL!, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })

    const data = await res.json()

    return Response.json(data)
  } catch (error) {
    return Response.json({ error: "Backend error" }, { status: 500 })
  }
}
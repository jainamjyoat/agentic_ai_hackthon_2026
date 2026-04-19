export async function POST(req: Request) {
  try {
    const formData = await req.formData()
    const file = formData.get("file") as File

    if (!file) {
      return Response.json({ error: "No file uploaded" }, { status: 400 })
    }

    const backendRes = await fetch(process.env.BACKEND_URL!.replace("/chat", "/upload-json"), {
      method: "POST",
      body: formData,
    })

    const data = await backendRes.json()

    return Response.json(data)
  } catch (error) {
    return Response.json({ error: "Upload failed" }, { status: 500 })
  }
}
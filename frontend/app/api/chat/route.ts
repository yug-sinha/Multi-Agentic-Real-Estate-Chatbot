import { NextRequest, NextResponse } from 'next/server'
import axios from 'axios'

export async function POST(req: NextRequest) {
  const formData = await req.formData()
  try {
    const backendResponse = await axios.post(
      `${process.env.BACKEND_URL}/chat`, // set in .env.local
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    return NextResponse.json(backendResponse.data)
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

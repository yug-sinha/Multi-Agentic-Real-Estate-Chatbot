import { NextRequest, NextResponse } from 'next/server'
import axios from 'axios'

export async function POST(req: NextRequest) {
  try {
    const backendResponse = await axios.post(`${process.env.BACKEND_URL}/reset`)
    return NextResponse.json({ message: 'Conversation history cleared.' })
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

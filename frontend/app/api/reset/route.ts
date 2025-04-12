import { NextRequest, NextResponse } from 'next/server'
import axios from 'axios'

export async function POST(req: NextRequest) {
  const res = await axios.post('http://localhost:8000/reset')
  return NextResponse.json({ message: 'Conversation history cleared.' })
}

'use client'

import { useState } from 'react'

interface ChatInputProps {
  onSend: (query: string, file?: File) => void
}

export default function ChatInput({ onSend }: ChatInputProps) {
  const [query, setQuery] = useState('')
  const [file, setFile] = useState<File | null>(null)

  const handleSend = () => {
    if (!query.trim() && !file) return
    onSend(query, file || undefined)
    setQuery('')
    setFile(null)
  }

  return (
    <div className="flex gap-2 p-3 border-t border-gray-700 bg-[#0d0d0d]">
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="text-sm text-gray-400"
      />
      <input
        type="text"
        placeholder="Type your message..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1 p-2 rounded bg-gray-800 text-gray-100 placeholder-gray-500 border border-gray-700 focus:outline-none"
      />
      <button
        onClick={handleSend}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Send
      </button>
    </div>
  )
}

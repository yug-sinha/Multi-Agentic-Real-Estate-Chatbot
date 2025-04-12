'use client'

import { useState } from 'react'
import { Paperclip, Send, X } from 'lucide-react'

interface ChatInputProps {
  onSend: (query: string, file?: File) => void
  onReset: () => void
}

export default function ChatInput({ onSend, onReset }: ChatInputProps) {
  const [query, setQuery] = useState('')
  const [file, setFile] = useState<File | null>(null)

  const handleSubmit = () => {
    if (!query.trim() && !file) return
    onSend(query, file || undefined)
    setQuery('')
    setFile(null)
  }

  return (
    <div className="flex flex-col border-t border-gray-700 p-2 gap-2">
      {file && (
        <div className="flex items-center justify-between bg-gray-800 text-gray-300 text-xs px-2 py-1 rounded">
          <span className="truncate max-w-[200px]">{file.name}</span>
          <button onClick={() => setFile(null)}>
            <X className="w-4 h-4 text-red-400 hover:text-red-500" />
          </button>
        </div>
      )}

      <div className="flex items-center gap-2">
        <button
          onClick={onReset}
          className="text-xs text-gray-400 border border-gray-700 px-2 py-1 rounded hover:bg-gray-800 transition"
        >
          New Chat
        </button>

        <label className="cursor-pointer">
          <Paperclip className="text-gray-400 w-5 h-5" />
          <input
            type="file"
            onChange={(e) => {
              if (e.target.files?.[0]) setFile(e.target.files[0])
            }}
            className="hidden"
          />
        </label>

        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 p-2 rounded bg-gray-800 text-gray-100 text-sm outline-none"
        />

        <button
          onClick={handleSubmit}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}

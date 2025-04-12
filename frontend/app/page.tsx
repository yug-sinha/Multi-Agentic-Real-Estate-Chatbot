'use client'

import { useState, useEffect, useRef } from 'react'
import { api } from '@/lib/api'
import ChatBubble from '@/components/ChatBubble'
import ChatInput from '@/components/ChatInput'
import TypingLoader from '@/components/TypingLoader'

interface ChatMessage {
  type: 'user' | 'agent'
  message: string
  agentName?: string
  imageUrl?: string
}

export default function HomePage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isTyping, setIsTyping] = useState(false)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  const handleSend = async (query: string, file?: File) => {
    if (!query.trim() && !file) return

    let imageUrl = ''
    if (file) {
      imageUrl = URL.createObjectURL(file)
    }

    setMessages(prev => [
      ...prev,
      { type: 'user', message: query, imageUrl }
    ])

    setIsTyping(true)

    const formData = new FormData()
    formData.append('query', query)
    if (file) formData.append('file', file)

    try {
      const res = await api.post('/chat', formData)
      const { response, agent } = res.data

      setMessages(prev => [
        ...prev,
        { type: 'agent', message: response, agentName: agent }
      ])
    } catch {
      setMessages(prev => [
        ...prev,
        { type: 'agent', message: 'Something went wrong.', agentName: 'System' }
      ])
    } finally {
      setIsTyping(false)
    }
  }

  useEffect(() => {
    chatContainerRef.current?.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: 'smooth',
    })
  }, [messages, isTyping])

  return (
    <main className="flex flex-col h-screen w-[95%] sm:w-[80%] mx-auto border-x border-gray-700 bg-[#0d0d0d]">
      <header className="p-4 border-b border-gray-700 text-center text-xl font-semibold text-gray-200 hover:text-blue-400 transition">
        Multi-Agent Real Estate Copilot
      </header>

      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-4"
      >
        {messages.map((msg, idx) => (
          <ChatBubble key={idx} {...msg} />
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-900 max-w-[85%] p-3 rounded-xl">
              <TypingLoader />
            </div>
          </div>
        )}
      </div>

      <ChatInput onSend={handleSend} />
    </main>
  )
}

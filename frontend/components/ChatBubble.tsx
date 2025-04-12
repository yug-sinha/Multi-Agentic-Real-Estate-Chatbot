import clsx from 'clsx'
import Image from 'next/image'
import ReactMarkdown from 'react-markdown'

interface ChatBubbleProps {
  message: string
  type: 'user' | 'agent'
  agentName?: string
  imageUrl?: string
}

export default function ChatBubble({
  message,
  type,
  agentName,
  imageUrl
}: ChatBubbleProps) {
  return (
    <div className={clsx('flex', type === 'user' ? 'justify-end' : 'justify-start')}>
      <div className={clsx(
        'max-w-[85%] p-3 rounded-xl space-y-2 overflow-x-auto',
        type === 'user' ? 'bg-gray-700 text-gray-100' : 'bg-gray-200 text-gray-900'
      )}>
        {type === 'agent' && agentName && (
          <p className="text-xs text-gray-400">{agentName}</p>
        )}
        {imageUrl && (
          <Image
            src={imageUrl}
            alt="Uploaded"
            width={200}
            height={200}
            className="rounded"
          />
        )}
        {type === 'agent' ? (
            <ReactMarkdown
            components={{
                strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
                ul: ({ node, ...props }) => <ul className="list-disc pl-5" {...props} />,
                ol: ({ node, ...props }) => <ol className="list-decimal pl-5" {...props} />,
                li: ({ node, ...props }) => <li className="mb-1" {...props} />,
                p: ({ node, ...props }) => <p className="mb-2" {...props} />,
                h2: ({ node, ...props }) => <h2 className="text-lg font-bold mt-4 mb-2" {...props} />,
                h3: ({ node, ...props }) => <h3 className="text-base font-bold mt-3 mb-1" {...props} />,
            }}
            >
            {message}
            </ReactMarkdown>
        ) : (
          <p className="whitespace-pre-wrap">{message}</p>
        )}
      </div>
    </div>
  )
}

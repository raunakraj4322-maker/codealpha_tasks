import { ChatMessage as ChatMessageType } from '../types';
import { Bot, User, CheckCircle2, AlertCircle } from 'lucide-react';

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-2`}>
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary-500' : 'bg-gray-700'
        }`}>
          {isUser ? (
            <User className="w-5 h-5 text-white" />
          ) : (
            <Bot className="w-5 h-5 text-white" />
          )}
        </div>
        
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`px-4 py-3 rounded-2xl ${
            isUser 
              ? 'bg-primary-500 text-white rounded-br-md' 
              : 'bg-gray-100 text-gray-800 rounded-bl-md'
          }`}>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {message.content}
            </p>
          </div>
          
          {message.sender === 'bot' && message.confidence !== undefined && (
            <div className="mt-1 flex items-center gap-1 text-xs text-gray-500">
              {message.confidence > 0.5 ? (
                <CheckCircle2 className="w-3 h-3 text-green-500" />
              ) : (
                <AlertCircle className="w-3 h-3 text-yellow-500" />
              )}
              <span>
                {message.confidence > 0 
                  ? `Confidence: ${(message.confidence * 100).toFixed(0)}%` 
                  : 'No match found'}
              </span>
            </div>
          )}
          
          {message.matchedQuestion && (
            <div className="mt-1 text-xs text-gray-500 italic">
              Matched: "{message.matchedQuestion}"
            </div>
          )}
          
          <span className="text-xs text-gray-400 mt-1">
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
      </div>
    </div>
  );
}

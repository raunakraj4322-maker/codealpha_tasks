import React from 'react';
import {
  Volume2,
  VolumeX,
  Copy,
  Check,
  X,
  ClipboardPaste,
  Sparkles,
  AlertCircle,
  Loader2,
} from 'lucide-react';

interface TranslationCardProps {
  sourceText: string;
  translatedText: string;
  onSourceChange: (text: string) => void;
  onClear: () => void;
  onCopy: () => void;
  onSpeakSource: () => void;
  onSpeakTarget: () => void;
  onPaste: () => void;
  isLoading: boolean;
  isCopied: boolean;
  isSpeakingSource: boolean;
  isSpeakingTarget: boolean;
  isSpeechSupported: boolean;
  provider?: string;
  error?: string | null;
  detectedSource?: string;
}

export const TranslationCard: React.FC<TranslationCardProps> = ({
  sourceText,
  translatedText,
  onSourceChange,
  onClear,
  onCopy,
  onSpeakSource,
  onSpeakTarget,
  onPaste,
  isLoading,
  isCopied,
  isSpeakingSource,
  isSpeakingTarget,
  isSpeechSupported,
  provider,
  error,
  detectedSource,
}) => {
  const maxChars = 5000;
  const charCount = sourceText.length;
  const wordCount = sourceText.trim() ? sourceText.trim().split(/\s+/).length : 0;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
      
      {/* SOURCE TEXT INPUT CARD */}
      <div className="flex flex-col bg-white dark:bg-slate-800 rounded-2xl shadow-md border border-slate-200 dark:border-slate-700/80 overflow-hidden transition-all focus-within:ring-2 focus-within:ring-blue-500/20 focus-within:border-blue-500">
        <div className="p-4 flex-1 flex flex-col min-h-[260px]">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold tracking-wider text-slate-400 dark:text-slate-400 uppercase flex items-center gap-1.5">
              Source Text
              {detectedSource && detectedSource !== 'auto' && (
                <span className="text-[10px] lowercase bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded text-blue-600 dark:text-blue-400 font-medium">
                  (Detected: {detectedSource})
                </span>
              )}
            </span>
            {sourceText && (
              <button
                onClick={onClear}
                className="p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
                title="Clear input text"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          <textarea
            value={sourceText}
            onChange={(e) => onSourceChange(e.target.value.slice(0, maxChars))}
            placeholder="Type or paste text to translate here..."
            className="w-full flex-1 bg-transparent resize-none focus:outline-none text-slate-800 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 text-base leading-relaxed"
            rows={7}
          />
        </div>

        {/* Source Card Footer Controls */}
        <div className="px-4 py-3 bg-slate-50/70 dark:bg-slate-900/40 border-t border-slate-100 dark:border-slate-700/60 flex items-center justify-between">
          <div className="flex items-center gap-1.5">
            {/* Speak Source Button */}
            <button
              onClick={onSpeakSource}
              disabled={!sourceText.trim() || !isSpeechSupported}
              className={`p-2 rounded-xl transition-colors ${
                isSpeakingSource
                  ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/60 dark:text-blue-300'
                  : 'hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400'
              } disabled:opacity-40 disabled:cursor-not-allowed`}
              title={isSpeechSupported ? 'Listen to source text' : 'Text-to-speech not supported'}
            >
              {isSpeakingSource ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </button>

            {/* Paste Button */}
            <button
              onClick={onPaste}
              className="p-2 rounded-xl hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 transition-colors"
              title="Paste from clipboard"
            >
              <ClipboardPaste className="w-4 h-4" />
            </button>
          </div>

          {/* Character & Word Counter */}
          <div className="text-xs font-medium text-slate-400 dark:text-slate-500 flex items-center gap-2">
            <span>{wordCount} words</span>
            <span>•</span>
            <span className={charCount >= maxChars ? 'text-rose-500 font-bold' : ''}>
              {charCount} / {maxChars}
            </span>
          </div>
        </div>
      </div>

      {/* TRANSLATED RESULT CARD */}
      <div className="flex flex-col bg-slate-50/90 dark:bg-slate-900/60 rounded-2xl shadow-md border border-slate-200 dark:border-slate-700/80 overflow-hidden relative transition-all">
        <div className="p-4 flex-1 flex flex-col min-h-[260px]">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold tracking-wider text-slate-400 dark:text-slate-400 uppercase flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-blue-500" />
              Translation Result
            </span>
            {provider && (
              <span className="text-[11px] font-medium text-slate-400 dark:text-slate-500">
                {provider}
              </span>
            )}
          </div>

          {/* Content Area */}
          <div className="flex-1 relative">
            {isLoading ? (
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 text-blue-600 dark:text-blue-400 py-12">
                <Loader2 className="w-8 h-8 animate-spin" />
                <span className="text-xs font-semibold tracking-wide animate-pulse">
                  Translating with AI...
                </span>
              </div>
            ) : error ? (
              <div className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 text-sm flex items-start gap-2.5">
                <AlertCircle className="w-5 h-5 shrink-0 text-rose-500 mt-0.5" />
                <div>
                  <h4 className="font-semibold mb-1">Translation Failed</h4>
                  <p className="text-xs">{error}</p>
                </div>
              </div>
            ) : translatedText ? (
              <p className="text-slate-800 dark:text-slate-100 text-base leading-relaxed whitespace-pre-wrap font-medium">
                {translatedText}
              </p>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-400 dark:text-slate-600 text-sm italic">
                Your translated text will appear here...
              </div>
            )}
          </div>
        </div>

        {/* Target Card Footer Controls */}
        <div className="px-4 py-3 bg-white/60 dark:bg-slate-800/60 border-t border-slate-100 dark:border-slate-700/60 flex items-center justify-between">
          <div className="flex items-center gap-1.5">
            {/* Speak Target Button */}
            <button
              onClick={onSpeakTarget}
              disabled={!translatedText.trim() || isLoading || !isSpeechSupported}
              className={`p-2 rounded-xl transition-colors ${
                isSpeakingTarget
                  ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/60 dark:text-blue-300'
                  : 'hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400'
              } disabled:opacity-40 disabled:cursor-not-allowed`}
              title={isSpeechSupported ? 'Listen to translation (🔊 Speak)' : 'Text-to-speech not supported'}
            >
              {isSpeakingTarget ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </button>
          </div>

          {/* Copy Button */}
          <button
            onClick={onCopy}
            disabled={!translatedText.trim() || isLoading}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all duration-200 ${
              isCopied
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'bg-blue-50 dark:bg-blue-900/40 hover:bg-blue-100 dark:hover:bg-blue-900/70 text-blue-600 dark:text-blue-300 border border-blue-200 dark:border-blue-800'
            } disabled:opacity-40 disabled:cursor-not-allowed`}
            title="Copy translation to clipboard"
          >
            {isCopied ? (
              <>
                <Check className="w-3.5 h-3.5" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy Text</span>
              </>
            )}
          </button>
        </div>

      </div>

    </div>
  );
};

import React, { useState, useEffect, useCallback } from 'react';
import { Header } from './components/Header';
import { LanguageSelector } from './components/LanguageSelector';
import { TranslationCard } from './components/TranslationCard';
import { ActionControls } from './components/ActionControls';
import { HistoryDrawer } from './components/HistoryDrawer';
import { Toast } from './components/Toast';
import { requestTranslation, checkServerHealth } from './services/api';
import { useSpeechSynthesis } from './hooks/useSpeechSynthesis';
import { useHistory } from './hooks/useHistory';
import { ToastMessage, ServerHealth, HistoryItem } from './types';
import { getLanguageByCode } from './data/languages';
import { Sparkles, Globe2, ShieldCheck, Cpu } from 'lucide-react';

export const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  const [sourceLang, setSourceLang] = useState<string>('en');
  const [targetLang, setTargetLang] = useState<string>('hi');
  const [sourceText, setSourceText] = useState<string>('');
  const [translatedText, setTranslatedText] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isCopied, setIsCopied] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [provider, setProvider] = useState<string>('');
  const [detectedSource, setDetectedSource] = useState<string>('');
  const [autoTranslate, setAutoTranslate] = useState<boolean>(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState<boolean>(false);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const [serverHealth, setServerHealth] = useState<ServerHealth | null>(null);

  const { speak, isPlaying, speakingText, isSupported: isSpeechSupported } = useSpeechSynthesis();
  const { history, addHistoryItem, removeHistoryItem, clearHistory } = useHistory();

  // Dark mode effect
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Initial server health check
  useEffect(() => {
    checkServerHealth().then(setServerHealth);
  }, []);

  const addToast = (type: ToastMessage['type'], message: string) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  const handleTranslate = useCallback(async () => {
    if (!sourceText.trim()) {
      setError('Please enter text to translate.');
      addToast('error', 'Please enter text to translate.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setIsCopied(false);

    try {
      const response = await requestTranslation({
        text: sourceText,
        sourceLanguage: sourceLang,
        targetLanguage: targetLang,
      });

      setTranslatedText(response.translatedText);
      setProvider(response.provider);
      setDetectedSource(response.sourceLanguage);

      addHistoryItem({
        sourceText,
        translatedText: response.translatedText,
        sourceLanguage: response.sourceLanguage || sourceLang,
        targetLanguage: targetLang,
      });
    } catch (err: any) {
      const msg = err?.message || 'Translation service is unavailable.';
      setError(msg);
      addToast('error', msg);
    } finally {
      setIsLoading(false);
    }
  }, [sourceText, sourceLang, targetLang, addHistoryItem]);

  // Auto-translate debounce trigger
  useEffect(() => {
    if (!autoTranslate || !sourceText.trim()) return;

    const timer = setTimeout(() => {
      handleTranslate();
    }, 800);

    return () => clearTimeout(timer);
  }, [sourceText, sourceLang, targetLang, autoTranslate, handleTranslate]);

  // Keyboard shortcut listener (Ctrl + Enter)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        handleTranslate();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleTranslate]);

  // Swap languages
  const handleSwap = () => {
    if (sourceLang === 'auto') return;
    const tempLang = sourceLang;
    setSourceLang(targetLang);
    setTargetLang(tempLang);

    // Swap texts if translated text exists
    if (translatedText) {
      setSourceText(translatedText);
      setTranslatedText(sourceText);
    }

    addToast('info', 'Languages swapped!');
  };

  // Copy-to-clipboard handler
  const handleCopy = async () => {
    if (!translatedText) return;
    try {
      await navigator.clipboard.writeText(translatedText);
      setIsCopied(true);
      addToast('success', 'Translation copied to clipboard!');
      setTimeout(() => setIsCopied(false), 2500);
    } catch (e) {
      addToast('error', 'Failed to copy to clipboard.');
    }
  };

  // Copy arbitrary text
  const handleCopyText = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      addToast('success', 'Copied to clipboard!');
    } catch (e) {
      addToast('error', 'Failed to copy.');
    }
  };

  // Text-to-Speech handlers
  const handleSpeakSource = () => {
    if (!sourceText.trim()) return;
    const langObj = getLanguageByCode(sourceLang);
    const success = speak(sourceText, langObj.bcp47 || 'en-US');
    if (!success) {
      addToast('error', 'Text-to-speech is not supported in this browser.');
    }
  };

  const handleSpeakTarget = () => {
    if (!translatedText.trim()) return;
    const langObj = getLanguageByCode(targetLang);
    const success = speak(translatedText, langObj.bcp47 || 'en-US');
    if (!success) {
      addToast('error', 'Text-to-speech is not supported in this browser.');
    }
  };

  // Paste handler
  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        setSourceText(text.slice(0, 5000));
        addToast('info', 'Pasted text from clipboard');
      }
    } catch {
      addToast('error', 'Unable to access clipboard. Please paste manually using Ctrl+V.');
    }
  };

  // History select handler
  const handleSelectHistory = (item: HistoryItem) => {
    setSourceLang(item.sourceLanguage);
    setTargetLang(item.targetLanguage);
    setSourceText(item.sourceText);
    setTranslatedText(item.translatedText);
    setError(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-900 transition-colors duration-200">
      
      {/* App Header */}
      <Header
        darkMode={darkMode}
        onToggleDarkMode={() => setDarkMode(!darkMode)}
        onOpenHistory={() => setIsHistoryOpen(true)}
        serverHealth={serverHealth}
      />

      {/* Main Content Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Banner Title Section */}
        <div className="text-center max-w-2xl mx-auto mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 text-blue-700 dark:text-blue-300 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI-Powered Multi-Language Translation Tool</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Break Language Barriers Instantly
          </h2>
          <p className="mt-2 text-sm sm:text-base text-slate-600 dark:text-slate-400">
            Real-time neural machine translation across 25+ global and Indian regional languages.
          </p>
        </div>

        {/* Language Selection */}
        <LanguageSelector
          sourceLang={sourceLang}
          targetLang={targetLang}
          onSourceChange={setSourceLang}
          onTargetChange={setTargetLang}
          onSwap={handleSwap}
        />

        {/* Translation Dual Card */}
        <TranslationCard
          sourceText={sourceText}
          translatedText={translatedText}
          onSourceChange={(val) => {
            setSourceText(val);
            if (error) setError(null);
          }}
          onClear={() => {
            setSourceText('');
            setTranslatedText('');
            setError(null);
          }}
          onCopy={handleCopy}
          onSpeakSource={handleSpeakSource}
          onSpeakTarget={handleSpeakTarget}
          onPaste={handlePaste}
          isLoading={isLoading}
          isCopied={isCopied}
          isSpeakingSource={isPlaying && speakingText === sourceText}
          isSpeakingTarget={isPlaying && speakingText === translatedText}
          isSpeechSupported={isSpeechSupported}
          provider={provider}
          error={error}
          detectedSource={detectedSource}
        />

        {/* Action Controls & Translate Button */}
        <ActionControls
          onTranslate={handleTranslate}
          isLoading={isLoading}
          disabled={!sourceText.trim()}
          autoTranslate={autoTranslate}
          onToggleAutoTranslate={() => setAutoTranslate(!autoTranslate)}
        />

        {/* Feature Highlights Footer Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6 border-t border-slate-200 dark:border-slate-800">
          <div className="p-4 rounded-xl bg-white dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/60 flex items-start gap-3">
            <Globe2 className="w-5 h-5 text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wide">
                25+ Languages
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Supports English, Hindi, Bengali, Tamil, Telugu, Spanish, French, Japanese & more.
              </p>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-white dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/60 flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wide">
                Bank-Grade Security
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                API credentials are strictly protected on backend server. Zero client key leaks.
              </p>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-white dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/60 flex items-start gap-3">
            <Cpu className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wide">
                Multi-Provider Engine
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Google Cloud Translate, Microsoft Azure, and MyMemory fallback strategy.
              </p>
            </div>
          </div>
        </div>

      </main>

      {/* Footer */}
      <footer className="py-6 border-t border-slate-200 dark:border-slate-800 text-center text-xs text-slate-500 dark:text-slate-400">
        <p>CodeAlpha Artificial Intelligence Internship Project • Language Translation Tool</p>
      </footer>

      {/* History Drawer Modal */}
      <HistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        history={history}
        onSelectHistory={handleSelectHistory}
        onDeleteItem={removeHistoryItem}
        onClearAll={clearHistory}
        onCopyText={handleCopyText}
      />

      {/* Toast Notification Container */}
      <Toast toasts={toasts} onDismiss={(id) => setToasts((t) => t.filter((item) => item.id !== id))} />

    </div>
  );
};

export default App;

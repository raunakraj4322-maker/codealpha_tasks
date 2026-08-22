import React from 'react';
import { Send, Loader2, Zap } from 'lucide-react';

interface ActionControlsProps {
  onTranslate: () => void;
  isLoading: boolean;
  disabled: boolean;
  autoTranslate: boolean;
  onToggleAutoTranslate: () => void;
}

export const ActionControls: React.FC<ActionControlsProps> = ({
  onTranslate,
  isLoading,
  disabled,
  autoTranslate,
  onToggleAutoTranslate,
}) => {
  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-8">
      
      {/* Auto-Translate Toggle */}
      <label className="flex items-center gap-2.5 cursor-pointer text-xs font-medium text-slate-600 dark:text-slate-300 select-none">
        <div className="relative inline-block w-9 h-5 align-middle select-none transition duration-200 ease-in">
          <input
            type="checkbox"
            checked={autoTranslate}
            onChange={onToggleAutoTranslate}
            className="toggle-checkbox absolute block w-3.5 h-3.5 rounded-full bg-white border-2 border-slate-300 appearance-none cursor-pointer top-0.75 left-0.75 checked:right-0.75 checked:left-auto checked:border-blue-600 checked:bg-blue-600 transition-all"
          />
          <div className={`toggle-label block overflow-hidden h-5 rounded-full cursor-pointer transition-colors ${autoTranslate ? 'bg-blue-600' : 'bg-slate-300 dark:bg-slate-700'}`} />
        </div>
        <span className="flex items-center gap-1">
          <Zap className="w-3.5 h-3.5 text-amber-500" />
          Auto-translate while typing
        </span>
      </label>

      {/* Main Translate Button */}
      <div className="flex items-center gap-3 w-full sm:w-auto">
        <span className="hidden md:inline text-xs text-slate-400 font-mono">
          Press <kbd className="px-1.5 py-0.5 bg-slate-200 dark:bg-slate-800 rounded text-[10px] font-semibold">Ctrl</kbd> + <kbd className="px-1.5 py-0.5 bg-slate-200 dark:bg-slate-800 rounded text-[10px] font-semibold">Enter</kbd>
        </span>
        <button
          type="button"
          onClick={onTranslate}
          disabled={disabled || isLoading}
          className="w-full sm:w-auto flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 active:scale-95 text-white font-semibold shadow-lg shadow-blue-500/25 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Translating...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>Translate Now</span>
            </>
          )}
        </button>
      </div>

    </div>
  );
};

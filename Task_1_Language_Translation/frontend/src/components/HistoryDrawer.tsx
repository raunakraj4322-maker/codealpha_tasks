import React from 'react';
import { HistoryItem } from '../types';
import { getLanguageByCode } from '../data/languages';
import { X, Trash2, Copy, ArrowRight, Clock } from 'lucide-react';

interface HistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  history: HistoryItem[];
  onSelectHistory: (item: HistoryItem) => void;
  onDeleteItem: (id: string) => void;
  onClearAll: () => void;
  onCopyText: (text: string) => void;
}

export const HistoryDrawer: React.FC<HistoryDrawerProps> = ({
  isOpen,
  onClose,
  history,
  onSelectHistory,
  onDeleteItem,
  onClearAll,
  onCopyText,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-900/50 backdrop-blur-xs transition-opacity animate-fade-in">
      <div className="absolute inset-0" onClick={onClose} />
      
      <div className="absolute inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white dark:bg-slate-800 shadow-2xl border-l border-slate-200 dark:border-slate-700 flex flex-col">
          
          {/* Drawer Header */}
          <div className="p-4 border-b border-slate-100 dark:border-slate-700 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100">
                Translation History
              </h2>
            </div>
            <div className="flex items-center gap-2">
              {history.length > 0 && (
                <button
                  onClick={onClearAll}
                  className="px-2.5 py-1 text-xs font-semibold text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/50 rounded-lg transition-colors"
                >
                  Clear All
                </button>
              )}
              <button
                onClick={onClose}
                className="p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-400"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Drawer Content */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {history.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 dark:text-slate-500 py-12">
                <Clock className="w-12 h-12 stroke-1 mb-2" />
                <p className="text-sm font-medium">No recent translations found</p>
                <p className="text-xs text-slate-400 mt-1">
                  Your translation history will be saved locally.
                </p>
              </div>
            ) : (
              history.map((item) => {
                const src = getLanguageByCode(item.sourceLanguage);
                const tgt = getLanguageByCode(item.targetLanguage);

                return (
                  <div
                    key={item.id}
                    className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700/60 hover:border-blue-400 dark:hover:border-blue-500 transition-all cursor-pointer group"
                    onClick={() => {
                      onSelectHistory(item);
                      onClose();
                    }}
                  >
                    <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-2">
                      <div className="flex items-center gap-1.5">
                        <span>{src.flag} {src.name}</span>
                        <ArrowRight className="w-3 h-3 text-slate-400" />
                        <span>{tgt.flag} {tgt.name}</span>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteItem(item.id);
                        }}
                        className="p-1 rounded opacity-0 group-hover:opacity-100 hover:bg-rose-100 dark:hover:bg-rose-900 text-rose-500 transition-opacity"
                        title="Delete item"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>

                    <p className="text-sm font-medium text-slate-800 dark:text-slate-200 line-clamp-2 mb-1">
                      {item.sourceText}
                    </p>
                    <p className="text-sm text-blue-600 dark:text-blue-400 line-clamp-2 font-medium">
                      {item.translatedText}
                    </p>

                    <div className="mt-2.5 pt-2 border-t border-slate-200/50 dark:border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
                      <span>{new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onCopyText(item.translatedText);
                        }}
                        className="flex items-center gap-1 text-slate-500 hover:text-blue-600 dark:hover:text-blue-400"
                      >
                        <Copy className="w-3 h-3" />
                        <span>Copy</span>
                      </button>
                    </div>
                  </div>
                );
              })
            )}
          </div>

        </div>
      </div>
    </div>
  );
};

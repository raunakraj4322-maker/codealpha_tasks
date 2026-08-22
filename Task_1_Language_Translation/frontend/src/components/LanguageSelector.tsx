import React, { useState } from 'react';
import { ArrowLeftRight, ChevronDown, Search } from 'lucide-react';
import { POPULAR_LANGUAGES, getLanguageByCode } from '../data/languages';

interface LanguageSelectorProps {
  sourceLang: string;
  targetLang: string;
  onSourceChange: (code: string) => void;
  onTargetChange: (code: string) => void;
  onSwap: () => void;
}

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  sourceLang,
  targetLang,
  onSourceChange,
  onTargetChange,
  onSwap,
}) => {
  const [activeDropdown, setActiveDropdown] = useState<'source' | 'target' | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const currentSource = getLanguageByCode(sourceLang);
  const currentTarget = getLanguageByCode(targetLang);

  const filteredLanguages = (isSource: boolean) => {
    const list = isSource ? POPULAR_LANGUAGES : POPULAR_LANGUAGES.filter((l) => l.code !== 'auto');
    if (!searchQuery) return list;
    const query = searchQuery.toLowerCase();
    return list.filter(
      (l) =>
        l.name.toLowerCase().includes(query) ||
        (l.nativeName && l.nativeName.toLowerCase().includes(query))
    );
  };

  const handleSelect = (code: string, isSource: boolean) => {
    if (isSource) {
      onSourceChange(code);
    } else {
      onTargetChange(code);
    }
    setActiveDropdown(null);
    setSearchQuery('');
  };

  return (
    <div className="relative z-20 bg-white dark:bg-slate-800/90 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 p-3 sm:p-4 mb-6">
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        
        {/* Source Language Selector */}
        <div className="w-full sm:flex-1 relative">
          <label className="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1">
            SOURCE LANGUAGE
          </label>
          <button
            type="button"
            onClick={() => setActiveDropdown(activeDropdown === 'source' ? null : 'source')}
            className="w-full flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-blue-500 dark:hover:border-blue-500 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <span className="text-xl">{currentSource.flag}</span>
              <span className="font-semibold text-slate-800 dark:text-slate-100">{currentSource.name}</span>
              {currentSource.nativeName && currentSource.code !== 'auto' && (
                <span className="text-xs text-slate-400 font-normal">({currentSource.nativeName})</span>
              )}
            </div>
            <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${activeDropdown === 'source' ? 'rotate-180' : ''}`} />
          </button>

          {/* Source Dropdown Menu */}
          {activeDropdown === 'source' && (
            <div className="absolute left-0 top-full mt-2 w-full max-h-80 bg-white dark:bg-slate-800 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-700 overflow-hidden z-50 animate-fade-in">
              <div className="p-2 border-b border-slate-100 dark:border-slate-700 flex items-center gap-2 bg-slate-50 dark:bg-slate-900/50">
                <Search className="w-4 h-4 text-slate-400 ml-2" />
                <input
                  type="text"
                  placeholder="Search language..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-transparent text-sm p-1.5 focus:outline-none text-slate-800 dark:text-slate-100"
                  autoFocus
                />
              </div>
              <div className="overflow-y-auto max-h-60 p-1">
                {filteredLanguages(true).map((lang) => (
                  <button
                    key={lang.code}
                    onClick={() => handleSelect(lang.code, true)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${
                      lang.code === sourceLang
                        ? 'bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 font-semibold'
                        : 'hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <span className="text-lg">{lang.flag}</span>
                      <span>{lang.name}</span>
                    </div>
                    {lang.nativeName && <span className="text-xs text-slate-400">{lang.nativeName}</span>}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Swap Button */}
        <div className="sm:self-end sm:mb-1">
          <button
            type="button"
            onClick={onSwap}
            disabled={sourceLang === 'auto'}
            className={`p-3 rounded-full bg-slate-100 dark:bg-slate-700 hover:bg-blue-500 hover:text-white dark:hover:bg-blue-600 text-slate-600 dark:text-slate-300 transition-all duration-200 shadow-sm ${
              sourceLang === 'auto' ? 'opacity-40 cursor-not-allowed' : 'active:scale-90 hover:rotate-180'
            }`}
            title={sourceLang === 'auto' ? 'Cannot swap when Auto Detect is selected' : 'Swap Source & Target Languages (Alt+S)'}
          >
            <ArrowLeftRight className="w-5 h-5" />
          </button>
        </div>

        {/* Target Language Selector */}
        <div className="w-full sm:flex-1 relative">
          <label className="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1">
            TARGET LANGUAGE
          </label>
          <button
            type="button"
            onClick={() => setActiveDropdown(activeDropdown === 'target' ? null : 'target')}
            className="w-full flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-blue-500 dark:hover:border-blue-500 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <span className="text-xl">{currentTarget.flag}</span>
              <span className="font-semibold text-slate-800 dark:text-slate-100">{currentTarget.name}</span>
              {currentTarget.nativeName && (
                <span className="text-xs text-slate-400 font-normal">({currentTarget.nativeName})</span>
              )}
            </div>
            <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${activeDropdown === 'target' ? 'rotate-180' : ''}`} />
          </button>

          {/* Target Dropdown Menu */}
          {activeDropdown === 'target' && (
            <div className="absolute right-0 top-full mt-2 w-full max-h-80 bg-white dark:bg-slate-800 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-700 overflow-hidden z-50 animate-fade-in">
              <div className="p-2 border-b border-slate-100 dark:border-slate-700 flex items-center gap-2 bg-slate-50 dark:bg-slate-900/50">
                <Search className="w-4 h-4 text-slate-400 ml-2" />
                <input
                  type="text"
                  placeholder="Search target language..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-transparent text-sm p-1.5 focus:outline-none text-slate-800 dark:text-slate-100"
                  autoFocus
                />
              </div>
              <div className="overflow-y-auto max-h-60 p-1">
                {filteredLanguages(false).map((lang) => (
                  <button
                    key={lang.code}
                    onClick={() => handleSelect(lang.code, false)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${
                      lang.code === targetLang
                        ? 'bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 font-semibold'
                        : 'hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <span className="text-lg">{lang.flag}</span>
                      <span>{lang.name}</span>
                    </div>
                    {lang.nativeName && <span className="text-xs text-slate-400">{lang.nativeName}</span>}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>

      {/* Quick Select Language Pills */}
      <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-700/60 flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
        <span className="text-slate-400 font-medium shrink-0 mr-1">Popular:</span>
        {['hi', 'es', 'fr', 'de', 'ja', 'zh'].map((code) => {
          const l = getLanguageByCode(code);
          return (
            <button
              key={code}
              type="button"
              onClick={() => onTargetChange(code)}
              className={`px-2.5 py-1 rounded-full border transition-all shrink-0 flex items-center gap-1 ${
                targetLang === code
                  ? 'bg-blue-600 text-white border-blue-600 shadow-xs font-medium'
                  : 'bg-slate-100 dark:bg-slate-700/60 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-600 hover:border-blue-400'
              }`}
            >
              <span>{l.flag}</span>
              <span>{l.name}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

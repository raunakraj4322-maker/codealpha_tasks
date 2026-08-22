import { useState, useEffect, useCallback } from 'react';

interface SpeechState {
  isPlaying: boolean;
  isSupported: boolean;
  speakingText: string | null;
}

export function useSpeechSynthesis() {
  const [state, setState] = useState<SpeechState>({
    isPlaying: false,
    isSupported: typeof window !== 'undefined' && 'speechSynthesis' in window,
    speakingText: null,
  });

  useEffect(() => {
    return () => {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const speak = useCallback(
    (text: string, bcp47Tag: string = 'en-US'): boolean => {
      if (!state.isSupported) {
        return false;
      }

      if (!text.trim()) return false;

      // Stop any current utterance
      window.speechSynthesis.cancel();

      if (state.isPlaying && state.speakingText === text) {
        setState((prev) => ({ ...prev, isPlaying: false, speakingText: null }));
        return true;
      }

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = bcp47Tag;
      utterance.rate = 0.95;

      // Try matching voice for the target language
      const voices = window.speechSynthesis.getVoices();
      const matchedVoice = voices.find(
        (v) => v.lang.toLowerCase() === bcp47Tag.toLowerCase() || v.lang.startsWith(bcp47Tag.substring(0, 2))
      );

      if (matchedVoice) {
        utterance.voice = matchedVoice;
      }

      utterance.onend = () => {
        setState((prev) => ({ ...prev, isPlaying: false, speakingText: null }));
      };

      utterance.onerror = () => {
        setState((prev) => ({ ...prev, isPlaying: false, speakingText: null }));
      };

      setState({ isPlaying: true, isSupported: true, speakingText: text });
      window.speechSynthesis.speak(utterance);
      return true;
    },
    [state.isSupported, state.isPlaying, state.speakingText]
  );

  const stop = useCallback(() => {
    if (state.isSupported) {
      window.speechSynthesis.cancel();
      setState((prev) => ({ ...prev, isPlaying: false, speakingText: null }));
    }
  }, [state.isSupported]);

  return {
    speak,
    stop,
    isPlaying: state.isPlaying,
    speakingText: state.speakingText,
    isSupported: state.isSupported,
  };
}

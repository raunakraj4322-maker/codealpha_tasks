interface SuggestedQuestionsProps {
  questions: string[];
  onSelectQuestion: (question: string) => void;
  disabled: boolean;
}

export default function SuggestedQuestions({ questions, onSelectQuestion, disabled }: SuggestedQuestionsProps) {
  if (questions.length === 0) return null;

  return (
    <div className="border-b border-gray-200 bg-gray-50 p-4">
      <p className="text-sm text-gray-600 mb-3 font-medium">Suggested questions:</p>
      <div className="flex flex-wrap gap-2">
        {questions.map((question, index) => (
          <button
            key={index}
            onClick={() => onSelectQuestion(question)}
            disabled={disabled}
            className="px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-primary-50 hover:border-primary-300 hover:text-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
}

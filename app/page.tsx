'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';

interface Senator {
  bioguide_id: string;
  name: string;
  first_name: string;
  last_name: string;
  state: string;
  party: string;
  image_file: string;
}

export default function Home() {
  const [senators, setSenators] = useState<Senator[]>([]);
  const [currentSenator, setCurrentSenator] = useState<Senator | null>(null);
  const [score, setScore] = useState({ correct: 0, total: 0 });
  const [feedback, setFeedback] = useState<'correct' | 'incorrect' | null>(null);
  const [usedSenators, setUsedSenators] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetch('/senators_metadata.json')
      .then(res => res.json())
      .then((data: Senator[]) => {
        setSenators(data);
        setCurrentSenator(data[Math.floor(Math.random() * data.length)]);
        setLoading(false);
      });
  }, []);

  const handleGuess = (guess: 'Republican' | 'Democrat') => {
    if (!currentSenator || feedback) return;

    // Accept Democrat for Independents (like Bernie Sanders who caucuses with Democrats)
    const isCorrect = currentSenator.party === guess ||
                     (currentSenator.party === 'Independent' && guess === 'Democrat');
    setFeedback(isCorrect ? 'correct' : 'incorrect');
    setScore(prev => ({
      correct: prev.correct + (isCorrect ? 1 : 0),
      total: prev.total + 1,
    }));

    setTimeout(() => {
      nextSenator();
    }, 1500);
  };

  const nextSenator = () => {
    setFeedback(null);
    const newUsed = new Set(usedSenators);
    if (currentSenator) {
      newUsed.add(currentSenator.bioguide_id);
    }

    if (newUsed.size >= senators.length) {
      newUsed.clear();
    }

    const availableSenators = senators.filter(
      s => !newUsed.has(s.bioguide_id)
    );

    if (availableSenators.length > 0) {
      const randomIndex = Math.floor(Math.random() * availableSenators.length);
      setCurrentSenator(availableSenators[randomIndex]);
      setUsedSenators(newUsed);
    }
  };

  const handleShare = () => {
    const shareText = `Senatordle\n\nScore: ${score.correct}/${score.total}\nAccuracy: ${accuracy}%\n\nsenatordle.com`;
    navigator.clipboard.writeText(shareText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-red-50 flex items-center justify-center">
        <div className="text-2xl font-semibold text-gray-600">Loading...</div>
      </div>
    );
  }

  if (!currentSenator) {
    return null;
  }

  const accuracy = score.total > 0 ? ((score.correct / score.total) * 100).toFixed(1) : '0.0';

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-red-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Senatordle
          </h1>
          <p className="text-gray-600">
            Can you tell if they&apos;re Republican or Democrat from their portrait?
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <div className="flex justify-between items-center mb-6">
            <div className="text-lg font-semibold text-gray-700">
              Score: {score.correct}/{score.total}
            </div>
            <div className="text-lg font-semibold text-gray-700">
              Accuracy: {accuracy}%
            </div>
          </div>

          {score.total > 0 && (
            <div className="flex justify-center mb-6">
              <button
                onClick={handleShare}
                className="px-6 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors"
              >
                {copied ? 'Copied!' : 'Share Score'}
              </button>
            </div>
          )}

          <div className="mb-6 relative flex justify-center">
            <div className="relative w-full max-w-sm aspect-[4/5] bg-gray-100 rounded-lg overflow-hidden">
              <Image
                src={`/portraits/${currentSenator.image_file}`}
                alt="Senator portrait"
                fill
                className="object-cover"
                priority
              />
            </div>
          </div>

          {feedback && (
            <div
              className={`mb-6 p-4 rounded-lg text-center font-semibold ${
                feedback === 'correct'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {feedback === 'correct' ? (
                <>
                  ✓ Correct! {currentSenator.name} is a {currentSenator.party} from {currentSenator.state}
                </>
              ) : (
                <>
                  ✗ Wrong! {currentSenator.name} is a {currentSenator.party} from {currentSenator.state}
                </>
              )}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => handleGuess('Republican')}
              disabled={feedback !== null}
              className={`py-4 px-6 rounded-lg font-semibold text-white transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none ${
                feedback === null
                  ? 'bg-red-600 hover:bg-red-700'
                  : 'bg-red-400'
              }`}
            >
              Republican
            </button>
            <button
              onClick={() => handleGuess('Democrat')}
              disabled={feedback !== null}
              className={`py-4 px-6 rounded-lg font-semibold text-white transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none ${
                feedback === null
                  ? 'bg-blue-600 hover:bg-blue-700'
                  : 'bg-blue-400'
              }`}
            >
              Democrat
            </button>
          </div>
        </div>

        <div className="text-center text-sm text-gray-500">
          <p>
            {senators.length} current US Senators • {usedSenators.size} seen in this round
          </p>
        </div>
      </div>
    </div>
  );
}

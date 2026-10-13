
import { useState } from 'react'
import StoryPlayer from './components/StoryPlayer'
import type { Language } from './types/story'

function App() {
  const [language, setLanguage] = useState<Language>('en')
  const [storyStarted, setStoryStarted] = useState(false)

  const languages: { code: Language; label: string; native: string }[] = [
    { code: 'en', label: 'English', native: 'English' },
    { code: 'ta', label: 'Tamil', native: 'தமிழ்' },
    { code: 'hi', label: 'Hindi', native: 'हिन्दी' },
    { code: 'ml', label: 'Malayalam', native: 'മലയാളം' },
    { code: 'kn', label: 'Kannada', native: 'ಕನ್ನಡ' },
    { code: 'te', label: 'Telugu', native: 'తెలుగు' },
  ]

  if (storyStarted) {
    return (
      <StoryPlayer
        language={language}
        onExit={() => setStoryStarted(false)}
      />
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-indigo-100 via-sky-50 to-amber-50 px-6">
      <div className="mx-auto flex min-h-screen max-w-4xl flex-col items-center justify-center text-center">
        <div className="mb-5 text-7xl">🌙</div>

        <p className="mb-3 text-sm font-bold uppercase tracking-[0.3em] text-sky-600">
          Stories that grow with you
        </p>

        <h1 className="mb-5 text-5xl font-black text-slate-800 sm:text-7xl">
          KADHAI
        </h1>

        <p className="mb-10 max-w-xl text-lg leading-8 text-slate-600 sm:text-xl">
          Step into a story where your choices help shape what happens next.
        </p>

        <div className="mb-8 w-full max-w-xl rounded-3xl bg-white p-6 shadow-xl">
          <p className="mb-5 font-bold text-slate-700">
            Choose your language
          </p>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {languages.map((item) => (
              <button
                key={item.code}
                type="button"
                onClick={() => setLanguage(item.code)}
                aria-pressed={language === item.code}
                className={`rounded-2xl border-2 px-4 py-4 font-bold transition ${
                  language === item.code
                    ? 'border-sky-600 bg-sky-600 text-white shadow-md'
                    : 'border-slate-100 bg-slate-50 text-slate-700 hover:border-sky-300 hover:bg-sky-50'
                }`}
              >
                <span className="block text-base">{item.native}</span>
                <span
                  className={`mt-1 block text-xs ${
                    language === item.code
                      ? 'text-sky-100'
                      : 'text-slate-500'
                  }`}
                >
                  {item.label}
                </span>
              </button>
            ))}
          </div>
        </div>

        <button
          type="button"
          onClick={() => setStoryStarted(true)}
          className="rounded-full bg-sky-600 px-10 py-5 text-xl font-black text-white shadow-xl transition hover:-translate-y-1 hover:bg-sky-700"
        >
          Start a Story ✨
        </button>

        <p className="mt-8 text-sm text-slate-400">
          A safe little world for curious minds.
        </p>
      </div>
    </main>
  )
}
export default App
import { useState } from 'react'
import StoryPlayer from './components/StoryPlayer'
import type { Language } from './types/story'

function App() {
  const [language, setLanguage] = useState<Language>('en')
  const [storyStarted, setStoryStarted] = useState(false)

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

        <div className="mb-8 rounded-3xl bg-white p-6 shadow-xl">
          <p className="mb-4 font-bold text-slate-700">
            Choose your language
          </p>

          <div className="flex gap-3">
            <button
              onClick={() => setLanguage('en')}
              className={`rounded-full px-6 py-3 font-bold transition ${
                language === 'en'
                  ? 'bg-sky-600 text-white'
                  : 'bg-slate-100 text-slate-600'
              }`}
            >
              English
            </button>

            <button
              onClick={() => setLanguage('ta')}
              className={`rounded-full px-6 py-3 font-bold transition ${
                language === 'ta'
                  ? 'bg-sky-600 text-white'
                  : 'bg-slate-100 text-slate-600'
              }`}
            >
              தமிழ்
            </button>
          </div>
        </div>

        <button
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
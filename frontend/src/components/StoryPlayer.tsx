import { useEffect, useRef, useState } from 'react'
import { createStorySession, takeStoryTurn } from '../api/client'
import type { Language, Scene, Session } from '../types/story'

interface StoryPlayerProps {
  language: Language
  onExit: () => void
}

interface StoryState {
  session: Session
  scene: Scene
}

function StoryPlayer({ language, onExit }: StoryPlayerProps) {
  const [storyState, setStoryState] = useState<StoryState | null>(null)
  const [loading, setLoading] = useState(true)
  const [choiceLoading, setChoiceLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const startedRef = useRef(false)

  async function startStory() {
    try {
      setLoading(true)
      setError(null)

      const result = await createStorySession({
        story_id: 'fixture-elephant-moon',
        child_id: 'demo-child',
        language,
      })

      setStoryState(result)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Something went wrong while starting the story.',
      )
    } finally {
      setLoading(false)
    }
  }

  async function handleChoice(optionId?: string) {
    if (!storyState || choiceLoading) {
      return
    }

    try {
      setChoiceLoading(true)
      setError(null)

      const result = await takeStoryTurn(
        storyState.session.session_id,
        optionId,
      )

      setStoryState(result)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Something went wrong while continuing the story.',
      )
    } finally {
      setChoiceLoading(false)
    }
  }

  useEffect(() => {
    if (startedRef.current) {
      return
    }

    startedRef.current = true
    void startStory()
  }, [])

  if (loading && !storyState) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-sky-50">
        <div className="text-center">
          <div className="mb-4 text-6xl">🌙</div>
          <p className="text-xl font-semibold text-slate-700">
            Opening your story...
          </p>
        </div>
      </div>
    )
  }

  if (error && !storyState) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-sky-50 px-6">
        <div className="max-w-md rounded-3xl bg-white p-8 text-center shadow-xl">
          <div className="mb-4 text-5xl">😕</div>

          <h2 className="mb-3 text-2xl font-bold text-slate-800">
            We couldn't open the story
          </h2>

          <p className="mb-6 text-slate-600">
            {error}
          </p>

          <div className="flex justify-center gap-3">
            <button
              onClick={startStory}
              className="rounded-full bg-sky-600 px-6 py-3 font-semibold text-white transition hover:bg-sky-700"
            >
              Try again
            </button>

            <button
              onClick={onExit}
              className="rounded-full bg-slate-100 px-6 py-3 font-semibold text-slate-700"
            >
              Back
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!storyState) {
    return null
  }

  const { session, scene } = storyState

  const narration =
    language === 'ta'
      ? scene.narration.ta
      : scene.narration.en

  if (scene.is_ending) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-indigo-100 via-sky-50 to-amber-50 px-6">
        <div className="w-full max-w-3xl rounded-[2rem] bg-white p-8 text-center shadow-2xl sm:p-12">
          <div className="mb-6 text-7xl">🌙🐘✨</div>

          <p className="mb-8 text-xl leading-9 text-slate-700 sm:text-2xl">
            {narration}
          </p>

          <div className="flex flex-col justify-center gap-3 sm:flex-row">
            <button
              onClick={startStory}
              className="rounded-full bg-sky-600 px-8 py-4 text-lg font-bold text-white shadow-lg transition hover:bg-sky-700"
            >
              Read Again
            </button>

            <button
              onClick={onExit}
              className="rounded-full bg-slate-100 px-8 py-4 text-lg font-bold text-slate-700 transition hover:bg-slate-200"
            >
              Choose Another Story
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-100 via-sky-50 to-amber-50 px-4 py-6 sm:px-8">
      <div className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-5xl flex-col">
        
        {/* Header */}
        <header className="mb-6 flex items-center justify-between">
          <button
            onClick={onExit}
            className="rounded-full bg-white/80 px-4 py-2 font-semibold text-slate-600 shadow-sm transition hover:bg-white"
          >
            ← Back
          </button>

          <div className="text-2xl font-black tracking-wide text-sky-700">
            KADHAI 🌙
          </div>

          <div className="rounded-full bg-white/80 px-4 py-2 text-sm font-semibold text-slate-500">
            {language === 'ta' ? 'தமிழ்' : 'English'}
          </div>
        </header>

        {/* Story scene */}
        <main className="flex flex-1 flex-col justify-center">
          <div className="overflow-hidden rounded-[2rem] bg-white shadow-2xl">
            
            {/* Visual area */}
            <div className="flex min-h-[280px] items-center justify-center bg-gradient-to-br from-indigo-200 via-sky-100 to-amber-100 sm:min-h-[360px]">
              <div className="text-center">
                <div className="mb-4 text-8xl">
                  🐘
                </div>

                <p className="px-6 text-sm font-medium text-slate-500">
                  {scene.characters.length > 0
                    ? scene.characters.join(' · ')
                    : 'A KADHAI story scene'}
                </p>
              </div>
            </div>

            {/* Narration */}
            <div className="p-6 sm:p-10">
              <p className="text-center text-xl font-medium leading-9 text-slate-700 sm:text-2xl">
                {narration}
              </p>

              {/* Choices */}
              {scene.interaction?.options &&
                scene.interaction.options.length > 0 && (
                  <div className="mt-8 grid gap-4 sm:grid-cols-2">
                    {scene.interaction.options.map((option) => (
                      <button
                        key={option.id}
                        disabled={choiceLoading}
                        onClick={() => handleChoice(option.id)}
                        className="rounded-2xl border-2 border-sky-100 bg-sky-50 px-6 py-5 text-left text-lg font-bold text-slate-700 transition hover:-translate-y-1 hover:border-sky-300 hover:bg-sky-100 disabled:cursor-not-allowed disabled:opacity-60"
                      >
                        {language === 'ta'
                          ? option.label.ta
                          : option.label.en}
                      </button>
                    ))}
                  </div>
                )}

              {/* Continue for linear scenes */}
              {!scene.interaction && !scene.is_ending && (
                <div className="mt-8 text-center">
                  <button
                    disabled={choiceLoading}
                    onClick={() => handleChoice()}
                    className="rounded-full bg-sky-600 px-8 py-4 text-lg font-bold text-white shadow-lg transition hover:bg-sky-700 disabled:opacity-60"
                  >
                    {choiceLoading ? 'Loading...' : 'Continue →'}
                  </button>
                </div>
              )}

              {error && (
                <p className="mt-5 text-center font-medium text-red-600">
                  {error}
                </p>
              )}
            </div>
          </div>

          {/* Development information */}
          <p className="mt-4 text-center text-xs text-slate-400">
            Scene: {session.current_scene_id}
          </p>
        </main>
      </div>
    </div>
  )
}

export default StoryPlayer
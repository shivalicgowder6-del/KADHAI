
import { useEffect, useRef, useState } from 'react'
import {
  createStorySession,
  generateNarration,
  getAudioUrl,
  takeStoryTurn,
} from '../api/client'
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

  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [audioLoading, setAudioLoading] = useState(false)
  const [audioError, setAudioError] = useState<string | null>(null)

  const startedRef = useRef(false)

  async function startStory() {
    try {
      setLoading(true)
      setError(null)
      setStoryState(null)
      setAudioUrl(null)
      setAudioError(null)

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

  const sessionId = storyState?.session.session_id
  const sceneId = storyState?.scene.scene_id
  const narration = storyState?.scene.narration[language]

  // Generate narration whenever the scene or selected language changes.
  useEffect(() => {
    if (!sessionId || !sceneId || narration == null) {
      setAudioUrl(null)
      setAudioLoading(false)
      return
    }

    // Capture narrowed values so TypeScript knows they are defined
    // inside the asynchronous function.
    const currentSessionId = sessionId
    const currentSceneId = sceneId
    const currentNarration = narration

    let cancelled = false

    async function loadNarration() {
      setAudioLoading(true)
      setAudioError(null)
      setAudioUrl(null)

      try {
        const safeSessionId = currentSessionId.replace(
          /[^a-zA-Z0-9_-]/g,
          '_',
        )
        const safeSceneId = currentSceneId.replace(
          /[^a-zA-Z0-9_-]/g,
          '_',
        )

        const filename = `narration_${safeSessionId}_${safeSceneId}_${language}.mp3`

        const result = await generateNarration(
          currentNarration,
          language,
          filename,
        )

        if (cancelled) {
          return
        }

        const audioFilename = result.audio_path.split(/[\\/]/).pop()

        if (!audioFilename) {
          throw new Error('The audio filename was not returned.')
        }

        setAudioUrl(getAudioUrl(audioFilename))
      } catch (err) {
        if (!cancelled) {
          setAudioError(
            err instanceof Error
              ? err.message
              : 'Unable to generate narration audio.',
          )
        }
      } finally {
        if (!cancelled) {
          setAudioLoading(false)
        }
      }
    }

    void loadNarration()

    return () => {
      cancelled = true
    }
  }, [sessionId, sceneId, language, narration])

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

          <p className="mb-6 text-slate-600">{error}</p>

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
  const currentNarration = scene.narration[language]

  const languageNames: Record<Language, string> = {
    en: 'English',
    ta: 'தமிழ்',
    hi: 'हिन्दी',
    ml: 'മലയാളം',
    kn: 'ಕನ್ನಡ',
    te: 'తెలుగు',
  }

  const continueLabels: Record<Language, string> = {
    en: 'Continue →',
    ta: 'தொடரவும் →',
    hi: 'जारी रखें →',
    ml: 'തുടരുക →',
    kn: 'ಮುಂದುವರಿಸಿ →',
    te: 'కొనసాగించండి →',
  }

  const readAgainLabels: Record<Language, string> = {
    en: 'Read Again',
    ta: 'மீண்டும் படிக்கவும்',
    hi: 'फिर से पढ़ें',
    ml: 'വീണ്ടും വായിക്കുക',
    kn: 'ಮತ್ತೆ ಓದಿ',
    te: 'మళ్లీ చదవండి',
  }

  const chooseStoryLabels: Record<Language, string> = {
    en: 'Choose Another Story',
    ta: 'வேறொரு கதையைத் தேர்ந்தெடுக்கவும்',
    hi: 'दूसरी कहानी चुनें',
    ml: 'മറ്റൊരു കഥ തിരഞ്ഞെടുക്കുക',
    kn: 'ಮತ್ತೊಂದು ಕಥೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
    te: 'మరో కథను ఎంచుకోండి',
  }

  const backLabels: Record<Language, string> = {
    en: '← Back',
    ta: '← பின்னால்',
    hi: '← वापस',
    ml: '← തിരികെ',
    kn: '← ಹಿಂದೆ',
    te: '← వెనక్కి',
  }

  const preparingLabels: Record<Language, string> = {
    en: 'Preparing your story narration...',
    ta: 'கதைக்கான குரலைத் தயாரிக்கிறது...',
    hi: 'कहानी की आवाज़ तैयार हो रही है...',
    ml: 'കഥയുടെ ശബ്ദം തയ്യാറാക്കുന്നു...',
    kn: 'ಕಥೆಯ ಧ್ವನಿಯನ್ನು ಸಿದ್ಧಪಡಿಸಲಾಗುತ್ತಿದೆ...',
    te: 'కథకు వాయిస్ సిద్ధమవుతోంది...',
  }

  const audioUnavailableLabels: Record<Language, string> = {
    en: 'Narration audio is unavailable.',
    ta: 'கதைக்கான ஒலி கிடைக்கவில்லை.',
    hi: 'कहानी का ऑडियो उपलब्ध नहीं है।',
    ml: 'കഥയുടെ ഓഡിയോ ലഭ്യമല്ല.',
    kn: 'ಕಥೆಯ ಆಡಿಯೊ ಲಭ್ಯವಿಲ್ಲ.',
    te: 'కథ ఆడియో అందుబాటులో లేదు.',
  }

  function renderAudioPlayer() {
    return (
      <div className="mt-6">
        {audioLoading && (
          <p className="text-center text-sm text-slate-500">
            {preparingLabels[language]}
          </p>
        )}

        {audioUrl && (
          <audio
            key={audioUrl}
            controls
            preload="none"
            className="mx-auto w-full max-w-md"
          >
            <source src={audioUrl} type="audio/mpeg" />
            Your browser does not support audio playback.
          </audio>
        )}

        {audioError && (
          <p role="status" className="mt-3 text-center text-sm text-red-600">
            {audioUnavailableLabels[language]} {audioError}
          </p>
        )}
      </div>
    )
  }

  if (scene.is_ending) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-indigo-100 via-sky-50 to-amber-50 px-6">
        <div className="w-full max-w-3xl rounded-[2rem] bg-white p-8 text-center shadow-2xl sm:p-12">
          <div className="mb-6 text-7xl">🌙🐘✨</div>

          <p className="text-xl leading-9 text-slate-700 sm:text-2xl">
            {currentNarration}
          </p>

          {renderAudioPlayer()}

          <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
            <button
              onClick={startStory}
              className="rounded-full bg-sky-600 px-8 py-4 text-lg font-bold text-white shadow-lg transition hover:bg-sky-700"
            >
              {readAgainLabels[language]}
            </button>

            <button
              onClick={onExit}
              className="rounded-full bg-slate-100 px-8 py-4 text-lg font-bold text-slate-700 transition hover:bg-slate-200"
            >
              {chooseStoryLabels[language]}
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
            {backLabels[language]}
          </button>

          <div className="text-2xl font-black tracking-wide text-sky-700">
            KADHAI 🌙
          </div>

          <div className="rounded-full bg-white/80 px-4 py-2 text-sm font-semibold text-slate-500">
            {languageNames[language]}
          </div>
        </header>

        {/* Story scene */}
        <main className="flex flex-1 flex-col justify-center">
          <div className="overflow-hidden rounded-[2rem] bg-white shadow-2xl">
            {/* Visual area */}
            <div className="flex min-h-[280px] items-center justify-center bg-gradient-to-br from-indigo-200 via-sky-100 to-amber-100 sm:min-h-[360px]">
              <div className="text-center">
                <div className="mb-4 text-8xl">🐘</div>

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
                {currentNarration}
              </p>

              {renderAudioPlayer()}

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
                        {option.label[language]}
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
                    {choiceLoading ? 'Loading...' : continueLabels[language]}
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

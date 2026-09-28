export type Language = 'en' | 'ta'

export interface LocalizedText {
  en: string
  ta: string
}

export interface Character {
  id: string
  appearance: string
  personality: string
}

export interface InteractionOption {
  id: string
  label: LocalizedText
  next_scene: string
}

export interface Interaction {
  template: 'choice'
  skill_ids: string[]
  options: InteractionOption[]
}

export interface Scene {
  scene_id: string
  narration: LocalizedText
  visual_prompt: string
  characters: string[]
  interaction: Interaction | null
  is_ending: boolean
}

export interface Session {
  session_id: string
  child_id: string | null
  story_id: string
  language: string
  current_scene_id: string
  choices: string[]
  started_at: string
  completed_at: string | null
}

export interface SessionWithScene {
  session: Session
  scene: Scene
}

export interface TurnResponse {
  session: Session
  scene: Scene
}

export interface CreateSessionRequest {
  story_id: string
  child_id?: string
  language: Language
}
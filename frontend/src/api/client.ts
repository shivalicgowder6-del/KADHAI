import type {
  CreateSessionRequest,
  SessionWithScene,
  TurnResponse,
} from '../types/story'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

async function request<T>(
  url: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {}),
    },
    ...options,
  })

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`

    try {
      const error = await response.json()

      if (typeof error.detail === 'string') {
        message = error.detail
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  return response.json() as Promise<T>
}

export async function createStorySession(
  data: CreateSessionRequest,
): Promise<SessionWithScene> {
  return request<SessionWithScene>('/api/sessions', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function takeStoryTurn(
  sessionId: string,
  optionId?: string,
): Promise<TurnResponse> {
  return request<TurnResponse>(
    `/api/sessions/${sessionId}/turns`,
    {
      method: 'POST',
      body: JSON.stringify(
        optionId
          ? { option_id: optionId }
          : {},
      ),
    },
  )
}
export interface CreateTTSResponse {
  audio_path: string
}

export async function generateNarration(
  text: string,
  language: string,
  filename: string,
): Promise<CreateTTSResponse> {
  return request<CreateTTSResponse>('/api/media/tts', {
    method: 'POST',
    body: JSON.stringify({
      text,
      language,
      filename,
    }),
  })
}
export function getAudioUrl(filename: string): string {
  return `${API_BASE_URL}/api/media/audio/${encodeURIComponent(filename)}`
}
import { useState } from 'react'

export interface ScoreDetail {
    criteria: string
    metric: string
    score: number
    max_score: number
    feedback: string
    approach: string
}

export interface ScoreSummary {
    content_structure: number
    speech_rate: number
    language_grammar: number
    clarity: number
    engagement: number
}

export interface ScoreResult {
    overall_score: number
    total_points: number
    max_points: number
    word_count: number
    wpm: number
    ttr: number
    details: ScoreDetail[]
    summary: ScoreSummary
}

const API_URL = 'http://localhost:8000'

export function useScoring() {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<ScoreResult | null>(null)
    const [error, setError] = useState<string | null>(null)

    const scoreTranscript = async (transcript: string) => {
        setLoading(true)
        setError(null)

        try {
            const response = await fetch(`${API_URL}/score`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ transcript }),
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Failed to score transcript')
            }

            const data = await response.json()
            setResult(data)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred')
        } finally {
            setLoading(false)
        }
    }

    return { loading, result, error, scoreTranscript }
}

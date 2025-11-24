import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { ScoreResult } from "@/hooks/useScoring"

interface OverallScoreCardProps {
    result: ScoreResult
}

export function OverallScoreCard({ result }: OverallScoreCardProps) {
    return (
        <Card className="border-2 border-primary/50 bg-gradient-to-br from-primary/5 to-primary/10 shadow-lg">
            <CardHeader>
                <CardTitle className="flex items-center justify-between">
                    <span className="text-2xl">Overall Score</span>
                    <span className="text-5xl font-bold text-primary">
                        {result.overall_score.toFixed(1)}
                        <span className="text-2xl text-muted-foreground">/100</span>
                    </span>
                </CardTitle>
                <CardDescription className="flex flex-wrap gap-4 text-base pt-2">
                    <span className="flex items-center gap-1">
                        <strong>{result.total_points.toFixed(1)}</strong>/{result.max_points} points
                    </span>
                    <span className="flex items-center gap-1">
                        <strong>{result.word_count}</strong> words
                    </span>
                    <span className="flex items-center gap-1">
                        <strong>{result.wpm.toFixed(0)}</strong> WPM
                    </span>
                    <span className="flex items-center gap-1">
                        TTR: <strong>{result.ttr.toFixed(3)}</strong>
                    </span>
                </CardDescription>
            </CardHeader>
        </Card>
    )
}

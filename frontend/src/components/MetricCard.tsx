import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { ScoreDetail } from "@/hooks/useScoring"
import { ApproachBadge } from "./ApproachBadge"
import { getScoreColor } from "@/lib/scoreUtils"

interface MetricCardProps {
    detail: ScoreDetail
}

export function MetricCard({ detail }: MetricCardProps) {
    return (
        <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
                <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                        <CardTitle className="text-lg leading-tight">
                            {detail.metric}
                        </CardTitle>
                        <CardDescription className="text-xs mt-1">
                            {detail.criteria}
                        </CardDescription>
                    </div>
                    <ApproachBadge approach={detail.approach} />
                </div>
            </CardHeader>
            <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-muted-foreground">Score</span>
                    <span className={`text-2xl font-bold ${getScoreColor(detail.score, detail.max_score)}`}>
                        {detail.score.toFixed(1)}
                        <span className="text-sm text-muted-foreground">/{detail.max_score}</span>
                    </span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                    <div
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${(detail.score / detail.max_score) * 100}%` }}
                    />
                </div>
                <div className="text-sm text-slate-700 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 p-3 rounded-md border-l-4 border-primary/50">
                    {detail.feedback}
                </div>
            </CardContent>
        </Card>
    )
}

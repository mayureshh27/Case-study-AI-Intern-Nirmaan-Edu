import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { ScoreSummary } from "@/hooks/useScoring"
import { formatCategoryName } from "@/lib/scoreUtils"

interface CategorySummaryProps {
    summary: ScoreSummary
}

export function CategorySummary({ summary }: CategorySummaryProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Score by Category</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-5">
                    {Object.entries(summary).map(([category, score]) => (
                        <div key={category} className="bg-slate-50 dark:bg-slate-800 p-3 rounded-lg">
                            <div className="text-xs text-muted-foreground mb-1">
                                {formatCategoryName(category)}
                            </div>
                            <div className="text-2xl font-bold text-primary">
                                {score.toFixed(1)}
                            </div>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    )
}

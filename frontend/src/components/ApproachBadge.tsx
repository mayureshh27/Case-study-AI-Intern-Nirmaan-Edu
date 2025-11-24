import { Brain, CheckCircle2 } from "lucide-react"

interface ApproachBadgeProps {
    approach: string
}

export function ApproachBadge({ approach }: ApproachBadgeProps) {
    if (approach.includes('Rule-based') && approach.includes('NLP')) {
        return (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300 rounded-full">
                <Brain className="h-3 w-3" /> Hybrid
            </span>
        )
    } else if (approach.includes('NLP')) {
        return (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 rounded-full">
                <Brain className="h-3 w-3" /> NLP
            </span>
        )
    } else {
        return (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300 rounded-full">
                <CheckCircle2 className="h-3 w-3" /> Rule-based
            </span>
        )
    }
}

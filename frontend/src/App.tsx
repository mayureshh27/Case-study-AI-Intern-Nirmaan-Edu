import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, AlertCircle, TrendingUp, MessageSquare } from "lucide-react"
import { useScoring } from "@/hooks/useScoring"
import { OverallScoreCard } from "@/components/OverallScoreCard"
import { CategorySummary } from "@/components/CategorySummary"
import { MetricCard } from "@/components/MetricCard"

function App() {
  const [transcript, setTranscript] = useState('')
  const { loading, result, error, scoreTranscript } = useScoring()

  const handleScore = () => {
    if (transcript.trim()) {
      scoreTranscript(transcript)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-4 md:p-8">
      <div className="mx-auto max-w-6xl space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI Communication Coach
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400">
            Analyze your spoken communication skills with AI-powered feedback
          </p>
        </div>

        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5" />
              Transcript Input
            </CardTitle>
            <CardDescription>
              Paste your speech transcript below to get a detailed analysis across multiple metrics.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea
              placeholder="Example: Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School..."
              className="min-h-[200px] font-mono text-sm"
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
            />
            <Button
              onClick={handleScore}
              disabled={loading || !transcript.trim()}
              className="w-full"
              size="lg"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing with AI...
                </>
              ) : (
                <>
                  <TrendingUp className="mr-2 h-4 w-4" />
                  Analyze Transcript
                </>
              )}
            </Button>
            {error && (
              <div className="flex items-center gap-2 text-red-500 bg-red-50 dark:bg-red-950 p-3 rounded-md">
                <AlertCircle className="h-4 w-4 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}
          </CardContent>
        </Card>

        {result && (
          <div className="space-y-6 animate-in fade-in duration-500">
            <OverallScoreCard result={result} />
            <CategorySummary summary={result.summary} />

            <div>
              <h2 className="text-2xl font-bold mb-4 text-slate-900 dark:text-slate-50">
                Detailed Metrics
              </h2>
              <div className="grid gap-4 md:grid-cols-2">
                {result.details.map((detail, index) => (
                  <MetricCard key={index} detail={detail} />
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

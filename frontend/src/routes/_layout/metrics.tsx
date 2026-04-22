import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Suspense } from "react"

import { canViewMetrics } from "@/authz"
import { MetricsService, UsersService } from "@/client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

function getMetricsQueryOptions() {
  return {
    queryFn: () => MetricsService.readMetrics(),
    queryKey: ["metrics"],
  }
}

export const Route = createFileRoute("/_layout/metrics")({
  component: Metrics,
  beforeLoad: async () => {
    const user = await UsersService.readUserMe()
    if (!canViewMetrics(user)) {
      throw new Error("FORBIDDEN")
    }
  },
  head: () => ({
    meta: [
      {
        title: "Metrics - FastAPI Template",
      },
    ],
  }),
})

function MetricsContent() {
  const { data } = useSuspenseQuery(getMetricsQueryOptions())

  return (
    <Card>
      <CardHeader>
        <CardTitle>Insights</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">{data.message}</p>
      </CardContent>
    </Card>
  )
}

function Metrics() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Metrics</h1>
        <p className="text-muted-foreground">Role-protected insights</p>
      </div>
      <Suspense fallback={<Skeleton className="h-32 w-full" />}>
        <MetricsContent />
      </Suspense>
    </div>
  )
}

import { Link } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { LoadingSpinner, ErrorAlert, EmptyState } from "@/components/common";
import { useJobs } from "@/hooks";
import { formatRelativeTime } from "@/utils/formatters";
import { FileText, Calendar, Users, AlertCircle } from "lucide-react";
import type { Job } from "@/types/job.types";

/**
 * Get status badge variant
 */
function getStatusVariant(status: Job["status"]) {
  switch (status) {
    case "completed":
      return "default"; // green
    case "processing":
      return "secondary"; // blue
    case "pending":
      return "outline"; // gray
    case "failed":
      return "destructive"; // red
    default:
      return "outline";
  }
}

/**
 * JobCard component - Display individual job information
 */
interface JobCardProps {
  job: Job;
}

function JobCard({ job }: JobCardProps) {
  const progress =
    job.total_rows && job.processed_rows
      ? (job.processed_rows / job.total_rows) * 100
      : 0;
  const isActive = job.status === "pending" || job.status === "processing";

  return (
    <Link to={`/jobs/${job.id}`}>
      <Card className="hover:shadow-md transition-shadow cursor-pointer">
        <CardContent className="p-6">
          <div className="space-y-4">
            {/* Header */}
            <div className="flex items-start justify-between">
              <div className="space-y-1 flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-muted-foreground shrink-0" />
                  <h3 className="font-semibold truncate">{job.filename}</h3>
                </div>
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <span className="truncate">ID: {job.id.slice(0, 8)}...</span>
                </div>
              </div>
              <Badge variant={getStatusVariant(job.status)}>{job.status}</Badge>
            </div>

            {/* Progress Bar (for active jobs) */}
            {isActive && job.total_rows && job.processed_rows !== null && (
              <div className="space-y-1">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">
                    {job.current_step || "Processing"}
                  </span>
                  <span className="font-medium">{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-2" />
                <div className="text-xs text-muted-foreground">
                  {job.processed_rows.toLocaleString()} /{" "}
                  {job.total_rows.toLocaleString()} rows
                </div>
              </div>
            )}

            {/* Results Summary (for completed jobs) */}
            {job.status === "completed" && (
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center gap-2 text-sm">
                  <Users className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="font-medium">
                      {job.processed_rows?.toLocaleString() || 0}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Processed
                    </div>
                  </div>
                </div>
                {job.error_rows && job.error_rows > 0 && (
                  <div className="flex items-center gap-2 text-sm">
                    <AlertCircle className="h-4 w-4 text-destructive" />
                    <div>
                      <div className="font-medium text-destructive">
                        {job.error_rows}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        Errors
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Timestamp */}
            <div className="flex items-center gap-2 text-xs text-muted-foreground pt-2 border-t">
              <Calendar className="h-3 w-3" />
              <span>
                {job.completed_at
                  ? formatRelativeTime(job.completed_at, 'Completed')
                  : job.started_at
                  ? formatRelativeTime(job.started_at, 'Started')
                  : formatRelativeTime(job.created_at, 'Created')}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

/**
 * JobsListPage component - Main jobs list view
 */
function JobsListPage() {
  const { data, isLoading, error } = useJobs({
    page: 1,
    page_size: 50,
    sort_by: "started_at",
    order: "desc",
  });

  // Loading state
  if (isLoading) {
    return (
      <div className="p-6">
        <Card>
          <CardContent className="py-12">
            <LoadingSpinner text="Loading jobs..." />
          </CardContent>
        </Card>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="p-6">
        <ErrorAlert error={error as Error} title="Failed to load jobs" />
      </div>
    );
  }

  // Empty state
  if (!data || data.items.length === 0) {
    return (
      <div className="p-6">
        <EmptyState
          title="No Jobs Yet"
          description="Upload an Excel file to create your first job"
        />
      </div>
    );
  }

  return (
    <div className="p-6 space-y-4">
      {/* Jobs Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data.items.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
}

export default JobsListPage;

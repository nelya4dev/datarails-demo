import { useParams, Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LoadingSpinner, ErrorAlert } from "@/components/common";
import {
  ProgressBar,
  ProcessingTimeline,
  ErrorSummary,
  StatusBadge,
} from "@/components/status";
import { useJobStatus } from "@/hooks";
import { calculateProgress } from "@/utils/statusHelpers";
import type { JobError } from "@/types/job.types";

function JobStatusPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const { data, isLoading, error } = useJobStatus(jobId);

  // Loading state
  if (isLoading) {
    return (
      <div className="py-8 px-6">
        <Card>
          <CardContent className="py-12">
            <LoadingSpinner text="Loading job status..." />
          </CardContent>
        </Card>
      </div>
    );
  }

  // Error state
  if (error || !data) {
    return (
      <div className="py-8 px-6">
        <Card>
          <CardHeader>
            <CardTitle>Job Not Found</CardTitle>
          </CardHeader>
          <CardContent>
            <ErrorAlert
              error={(error as Error) || "Job not found"}
              title="Error"
            />
            <Button asChild className="mt-4">
              <Link to="/">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Jobs
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Calculate progress
  const progress = calculateProgress(data.processed_rows, data.total_rows);

  // Parse errors from error_details
  const parseErrors = (errorDetails: Record<string, unknown> | null): JobError[] => {
    if (!errorDetails || typeof errorDetails !== 'object') return [];

    const errorsArray = (errorDetails as { errors?: unknown[] }).errors;
    if (!Array.isArray(errorsArray)) return [];

    return errorsArray.map((err: any) => ({
      row: err.row || 0,
      field: err.sheet || '',
      message: err.error || err.message || 'Unknown error'
    }));
  };

  const errors = parseErrors(data.error_details);

  return (
    <div className="py-8 px-6">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <Button variant="ghost" asChild>
            <Link to="/">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Jobs
            </Link>
          </Button>
          <StatusBadge status={data.status} />
        </div>

        {/* Job Info Card */}
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle>Job Status</CardTitle>
                <CardDescription className="mt-2">
                  <span className="font-medium">File:</span> {data.filename}
                </CardDescription>
                <CardDescription>
                  <span className="font-medium">Job ID:</span> {data.id}
                </CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Progress Bar */}
            {(data.status === "processing" || data.status === "completed") && (
              <ProgressBar
                value={progress}
                totalRows={data.total_rows}
                processedRows={data.processed_rows}
              />
            )}

            {/* Processing Timeline */}
            <div>
              <h3 className="text-sm font-medium mb-4">Processing Steps</h3>
              <ProcessingTimeline
                status={data.status}
                currentStep={data.current_step}
              />
            </div>

            {/* Error Summary */}
            {data.status === "failed" && data.error_details && (
              <ErrorSummary
                errors={errors}
                errorRows={data.error_rows ?? 0}
              />
            )}

            {/* Error Summary for completed jobs with errors */}
            {data.status === "completed" && data.error_rows && data.error_rows > 0 && (
              <ErrorSummary
                errors={errors}
                errorRows={data.error_rows}
              />
            )}

            {/* Timestamps */}
            <div className="text-xs text-muted-foreground pt-4 border-t space-y-1">
              {data.started_at && (
                <p>Started: {new Date(data.started_at).toLocaleString()}</p>
              )}
              {data.completed_at && (
                <p>Completed: {new Date(data.completed_at).toLocaleString()}</p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default JobStatusPage;

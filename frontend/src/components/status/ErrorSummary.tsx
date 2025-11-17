import { useState } from 'react';
import { AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import type { JobError } from '@/types/job.types';

interface ErrorSummaryProps {
  errors: JobError[];
  errorRows: number;
}

/**
 * ErrorSummary component displays job processing errors
 *
 * Collapsible component that shows error count by default.
 * Click to expand and view all errors.
 *
 * @example
 * ```tsx
 * <ErrorSummary
 *   errors={jobErrors}
 *   errorRows={5}
 * />
 * ```
 */
export function ErrorSummary({ errors, errorRows }: ErrorSummaryProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const displayErrors = isExpanded ? errors : errors.slice(0, 3);
  const hasMoreErrors = errors.length > 3;

  return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center justify-between w-full text-left hover:opacity-80 transition-opacity"
        >
          <span>Processing Errors ({errorRows} row{errorRows !== 1 ? 's' : ''})</span>
          {isExpanded ? (
            <ChevronUp className="h-4 w-4 ml-2" />
          ) : (
            <ChevronDown className="h-4 w-4 ml-2" />
          )}
        </button>
      </AlertTitle>
      <AlertDescription>
        <div className="mt-2 space-y-2">
          {!isExpanded && (
            <p className="text-sm">
              Click to view {hasMoreErrors ? 'all ' : ''}{errors.length} validation error{errors.length !== 1 ? 's' : ''}
            </p>
          )}

          {isExpanded && (
            <ul className="list-disc list-inside space-y-1 text-sm max-h-96 overflow-y-auto">
              {displayErrors.map((error, index) => (
                <li key={index}>
                  <span className="font-medium">Row {error.row}</span>
                  {' - '}
                  <span className="text-muted-foreground">{error.field}:</span>
                  {' '}
                  {error.message}
                </li>
              ))}
            </ul>
          )}
        </div>
      </AlertDescription>
    </Alert>
  );
}

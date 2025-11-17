import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

interface ErrorAlertProps {
  error: Error | string;
  title?: string;
  className?: string;
}

/**
 * ErrorAlert component displays error messages in a consistent format
 *
 * Handles different error types and provides user-friendly messages.
 *
 * @example
 * ```tsx
 * <ErrorAlert error={error} title="Upload Failed" />
 * ```
 */
export function ErrorAlert({ error, title = 'Error', className }: ErrorAlertProps) {
  const getErrorMessage = (err: Error | string): string => {
    if (typeof err === 'string') return err;
    if (err instanceof Error) return err.message;
    return 'An unexpected error occurred';
  };

  return (
    <Alert variant="destructive" className={className} role="alert">
      <AlertCircle className="h-4 w-4" aria-hidden="true" />
      <AlertTitle>{title}</AlertTitle>
      <AlertDescription>{getErrorMessage(error)}</AlertDescription>
    </Alert>
  );
}

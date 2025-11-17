import { useQuery } from '@tanstack/react-query';
import { getJobStatus } from '@/services/endpoints';
import { shouldRetry, getRetryDelay } from '@/utils/retryConfig';

/**
 * Custom hook for fetching job status with conditional polling
 *
 * Automatically polls every 2 seconds while job is processing or pending.
 * Stops polling when job is completed or failed.
 * Uses smart retry logic - only retries on network/server errors.
 *
 * @param jobId - The unique identifier for the job
 * @returns TanStack Query result with job status data
 *
 * @example
 * ```tsx
 * function JobStatusPage({ jobId }: { jobId: string }) {
 *   const { data, isLoading, error } = useJobStatus(jobId);
 *
 *   if (isLoading) return <LoadingSpinner />;
 *   if (error) return <ErrorMessage error={error} />;
 *
 *   return (
 *     <div>
 *       <p>Status: {data.status}</p>
 *       <ProgressBar
 *         value={(data.processed_rows / data.total_rows) * 100}
 *       />
 *     </div>
 *   );
 * }
 * ```
 */
export function useJobStatus(jobId: string | undefined) {
  return useQuery({
    queryKey: ['jobStatus', jobId],
    queryFn: () => getJobStatus(jobId!),
    enabled: !!jobId, // Only run query when jobId exists
    retry: shouldRetry,
    retryDelay: getRetryDelay,
    // Conditional polling based on job status
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === 'processing' || data?.status === 'pending') {
        return parseInt(import.meta.env.VITE_POLLING_INTERVAL_MS || '2000');
      }
      return false;
    },
    // Only refetch on mount if job is still processing
    refetchOnMount: (query) => {
      const data = query.state.data;
      // If no data yet, refetch
      if (!data) return true;
      // If processing or pending, refetch
      if (data.status === 'processing' || data.status === 'pending') return true;
      // If completed or failed, DON'T refetch
      return false;
    },
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  });
}

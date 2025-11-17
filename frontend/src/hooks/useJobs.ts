import { useQuery } from '@tanstack/react-query';
import { getJobs } from '@/services/endpoints';
import type { JobsQueryParams } from '@/types/job.types';

/**
 * useJobs hook - Fetch jobs list with conditional polling
 *
 * Automatically polls for in-progress jobs to show real-time updates
 *
 * @param params - Query parameters (page, page_size, status, sort, order)
 * @returns Query result with jobs data
 */
export function useJobs(params: JobsQueryParams = {}) {
  return useQuery({
    queryKey: ['jobs', params],
    queryFn: () => getJobs(params),
    refetchInterval: (query) => {
      const data = query.state.data;

      // Check if there are any in-progress jobs
      const hasActiveJobs = data?.items?.some(
        (job) => job.status === 'pending' || job.status === 'processing'
      );

      // Poll every 2 seconds if there are active jobs
      return hasActiveJobs
        ? parseInt(import.meta.env.VITE_POLLING_INTERVAL_MS || '2000')
        : false;
    },
  });
}

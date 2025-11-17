import { CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import type { JobStatus } from '@/types/job.types';
import type { LucideIcon } from 'lucide-react';

/**
 * Status badge configuration
 */
export interface StatusBadgeConfig {
  variant: 'default' | 'destructive' | 'secondary' | 'outline';
  className?: string;
  icon: LucideIcon;
  label: string;
}

/**
 * Get status badge configuration for a job status
 *
 * Returns consistent badge styling across the application.
 *
 * @param status - Job status value
 * @returns Badge configuration object
 */
export function getStatusBadgeConfig(status: JobStatus): StatusBadgeConfig {
  switch (status) {
    case 'completed':
      return {
        variant: 'default',
        className: 'bg-success text-white',
        icon: CheckCircle2,
        label: 'Completed',
      };
    case 'failed':
      return {
        variant: 'destructive',
        icon: XCircle,
        label: 'Failed',
      };
    case 'processing':
      return {
        variant: 'default',
        className: 'bg-processing text-white',
        icon: Loader2,
        label: 'Processing',
      };
    case 'pending':
      return {
        variant: 'secondary',
        icon: Loader2,
        label: 'Pending',
      };
    default:
      return {
        variant: 'outline',
        icon: Loader2,
        label: status,
      };
  }
}

/**
 * Calculate job progress percentage
 *
 * @param processedRows - Number of rows processed
 * @param totalRows - Total number of rows (can be null during early processing)
 * @returns Progress percentage (0-100)
 */
export function calculateProgress(processedRows: number | null, totalRows: number | null): number {
  if (!totalRows || totalRows === 0) return 0;
  if (!processedRows) return 0;
  return Math.min((processedRows / totalRows) * 100, 100);
}

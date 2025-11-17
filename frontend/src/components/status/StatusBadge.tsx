import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { getStatusBadgeConfig } from '@/utils/statusHelpers';
import type { JobStatus } from '@/types/job.types';

interface StatusBadgeProps {
  status: JobStatus;
  className?: string;
}

/**
 * StatusBadge component displays job status with appropriate styling
 *
 * Uses centralized status configuration for consistency.
 *
 * @example
 * ```tsx
 * <StatusBadge status="completed" />
 * ```
 */
export function StatusBadge({ status, className }: StatusBadgeProps) {
  const config = getStatusBadgeConfig(status);
  const Icon = config.icon;
  const isAnimated = status === 'processing' || status === 'pending';

  return (
    <Badge
      variant={config.variant}
      className={cn(config.className, className)}
      role="status"
      aria-label={`Job status: ${config.label}`}
    >
      <Icon
        className={cn('h-3 w-3 mr-1', isAnimated && 'animate-spin')}
        aria-hidden="true"
      />
      {config.label}
    </Badge>
  );
}

import { Progress } from '@/components/ui/progress';

interface ProgressBarProps {
  value: number;
  totalRows: number | null;
  processedRows: number | null;
}

/**
 * ProgressBar component displays processing progress
 *
 * Shows progress percentage and row counts.
 *
 * @example
 * ```tsx
 * <ProgressBar
 *   value={75}
 *   totalRows={1000}
 *   processedRows={750}
 * />
 * ```
 */
export function ProgressBar({ value, totalRows, processedRows }: ProgressBarProps) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="text-muted-foreground">Processing Progress</span>
        <span className="font-medium">{Math.round(value)}%</span>
      </div>
      <Progress value={value} className="h-3" />
      <p className="text-xs text-muted-foreground text-right">
        {(processedRows ?? 0).toLocaleString()} / {(totalRows ?? 0).toLocaleString()} rows processed
      </p>
    </div>
  );
}

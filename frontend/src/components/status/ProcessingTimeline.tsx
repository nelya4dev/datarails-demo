import { CheckCircle2, Circle, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { JobStatus } from '@/types/job.types';

interface ProcessingTimelineProps {
  status: JobStatus;
  currentStep: string;
}

const PROCESSING_STEPS = [
  { key: 'pending', label: 'Pending' },
  { key: 'reading', label: 'Reading Excel' },
  { key: 'validating', label: 'Validating Data' },
  { key: 'transforming', label: 'Transforming' },
  { key: 'persisting', label: 'Saving to Database' },
  { key: 'completed', label: 'Completed' },
] as const;

/**
 * ProcessingTimeline component shows job processing steps
 *
 * Displays 6-step timeline with status icons.
 *
 * @example
 * ```tsx
 * <ProcessingTimeline
 *   status="processing"
 *   currentStep="validating"
 * />
 * ```
 */
export function ProcessingTimeline({ status, currentStep }: ProcessingTimelineProps) {
  const getStepStatus = (stepKey: string): 'completed' | 'current' | 'pending' => {
    const currentIndex = PROCESSING_STEPS.findIndex((s) => s.key === currentStep);
    const stepIndex = PROCESSING_STEPS.findIndex((s) => s.key === stepKey);

    if (status === 'completed') return 'completed';
    if (status === 'failed') {
      return stepIndex <= currentIndex ? 'current' : 'pending';
    }
    if (stepIndex < currentIndex) return 'completed';
    if (stepIndex === currentIndex) return 'current';
    return 'pending';
  };

  return (
    <div className="space-y-1">
      {PROCESSING_STEPS.map((step, index) => {
        const stepStatus = getStepStatus(step.key);
        const isLast = index === PROCESSING_STEPS.length - 1;

        return (
          <div key={step.key} className="relative">
            <div className="flex items-center gap-3">
              {/* Icon */}
              <div className="flex-shrink-0">
                {stepStatus === 'completed' && (
                  <CheckCircle2 className="h-5 w-5 text-success" />
                )}
                {stepStatus === 'current' && (
                  <Loader2 className="h-5 w-5 text-processing animate-spin" />
                )}
                {stepStatus === 'pending' && (
                  <Circle className="h-5 w-5 text-muted-foreground" />
                )}
              </div>

              {/* Label */}
              <p
                className={cn(
                  'text-sm font-medium',
                  stepStatus === 'completed' && 'text-success',
                  stepStatus === 'current' && 'text-processing',
                  stepStatus === 'pending' && 'text-muted-foreground'
                )}
              >
                {step.label}
              </p>
            </div>

            {/* Connector line */}
            {!isLast && (
              <div
                className={cn(
                  'ml-2.5 h-6 w-0.5',
                  stepStatus === 'completed' ? 'bg-success' : 'bg-border'
                )}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

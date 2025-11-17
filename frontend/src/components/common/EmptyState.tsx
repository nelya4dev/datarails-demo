import { FileX2, type LucideIcon } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import type { ReactNode } from 'react';

interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: LucideIcon;
  action?: ReactNode;
  className?: string;
}

/**
 * EmptyState component displays when no data is available
 *
 * Reusable component for empty states with optional action button.
 *
 * @example
 * ```tsx
 * <EmptyState
 *   title="No Employees Found"
 *   description="Upload a file to import employee data"
 *   action={<Button asChild><Link to="/">Go to Upload</Link></Button>}
 * />
 * ```
 */
export function EmptyState({
  title,
  description,
  icon: Icon = FileX2,
  action,
  className,
}: EmptyStateProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex flex-col items-center text-center">
          <div className="rounded-full p-3 bg-muted mb-4">
            <Icon className="h-10 w-10 text-muted-foreground" aria-hidden="true" />
          </div>
          <CardTitle>{title}</CardTitle>
          {description && <CardDescription className="mt-2">{description}</CardDescription>}
        </div>
      </CardHeader>
      {action && (
        <CardContent className="flex justify-center">
          {action}
        </CardContent>
      )}
    </Card>
  );
}

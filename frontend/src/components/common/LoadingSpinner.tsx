import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  text?: string;
  className?: string;
}

const sizeClasses = {
  sm: "h-6 w-6",
  md: "h-12 w-12",
  lg: "h-16 w-16",
};

/**
 * LoadingSpinner component displays a loading indicator
 *
 * Reusable loading state component with optional text.
 *
 * @example
 * ```tsx
 * <LoadingSpinner size="md" text="Loading employees..." />
 * ```
 */
export function LoadingSpinner({
  size = "md",
  text,
  className,
}: LoadingSpinnerProps) {
  return (
    <div
      className={cn("flex flex-col items-center gap-4", className)}
      role="status"
      aria-live="polite"
    >
      <Loader2
        className={cn("animate-spin text-primary", sizeClasses[size])}
        aria-hidden="true"
      />
      {text && <p className="text-muted-foreground">{text}</p>}
      <span className="sr-only">{text || "Loading..."}</span>
    </div>
  );
}

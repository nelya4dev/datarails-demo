import { ArrowUpDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import type { Column } from '@tanstack/react-table';

interface SortableHeaderProps<TData, TValue> {
  column: Column<TData, TValue>;
  label: string;
}

/**
 * SortableHeader component for table column headers
 *
 * Reusable sortable header with consistent styling.
 * Follows DRY principle to avoid repeating sortable header logic.
 *
 * @example
 * ```tsx
 * {
 *   accessorKey: 'name',
 *   header: ({ column }) => <SortableHeader column={column} label="Name" />,
 * }
 * ```
 */
export function SortableHeader<TData, TValue>({ column, label }: SortableHeaderProps<TData, TValue>) {
  return (
    <Button
      variant="ghost"
      onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
      className="-ml-4"
      aria-label={`Sort by ${label}`}
    >
      {label}
      <ArrowUpDown className="ml-2 h-4 w-4" aria-hidden="true" />
    </Button>
  );
}

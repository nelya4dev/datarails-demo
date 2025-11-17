import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type ColumnDef,
  type SortingState,
} from "@tanstack/react-table";
import { useState, useMemo } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatCurrency, formatDate } from "@/utils/formatters";
import { SortableHeader } from "./SortableHeader";
import type { Employee } from "@/types/employee.types";

interface EmployeesTableProps {
  data: Employee[];
}

/**
 * EmployeesTable component displays employee data in a sortable table
 *
 * Uses TanStack Table for advanced table features.
 * Column definitions are memoized to prevent unnecessary re-renders.
 *
 * @example
 * ```tsx
 * <EmployeesTable data={employees} />
 * ```
 */
export function EmployeesTable({ data }: EmployeesTableProps) {
  const [sorting, setSorting] = useState<SortingState>([]);

  // Memoize columns to prevent recreation on every render
  const columns = useMemo<ColumnDef<Employee>[]>(
    () => [
      {
        accessorKey: "employee_id",
        header: "Employee ID",
        cell: ({ row }) => (
          <span className="font-mono text-sm">
            {row.getValue("employee_id")}
          </span>
        ),
      },
      {
        accessorKey: "name",
        header: ({ column }) => <SortableHeader column={column} label="Name" />,
        cell: ({ row }) => (
          <span className="font-medium">{row.getValue("name")}</span>
        ),
      },
      {
        accessorKey: "department_name",
        header: ({ column }) => (
          <SortableHeader column={column} label="Department" />
        ),
      },
      {
        accessorKey: "salary",
        header: ({ column }) => (
          <SortableHeader column={column} label="Salary (USD)" />
        ),
        cell: ({ row }) => formatCurrency(row.getValue("salary")),
      },
      {
        accessorKey: "annual_salary_eur",
        header: ({ column }) => (
          <SortableHeader column={column} label="Salary (EUR)" />
        ),
        cell: ({ row }) => {
          const value = row.getValue("annual_salary_eur") as number;
          return `€${value.toLocaleString()}`;
        },
      },
      {
        accessorKey: "tenure_years",
        header: ({ column }) => (
          <SortableHeader column={column} label="Tenure (Years)" />
        ),
        cell: ({ row }) => `${row.getValue("tenure_years")} years`,
      },
      {
        accessorKey: "hire_date",
        header: ({ column }) => (
          <SortableHeader column={column} label="Hire Date" />
        ),
        cell: ({ row }) => formatDate(row.getValue("hire_date")),
      },
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <TableHead key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">
                No employees found.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}

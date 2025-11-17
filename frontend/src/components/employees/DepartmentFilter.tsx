import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface DepartmentFilterProps {
  value: string;
  onChange: (value: string) => void;
}

/**
 * DepartmentFilter component - Dropdown to filter employees by department
 *
 * Provides a select dropdown with predefined department options.
 * Sends department_name to backend API for filtering.
 */
export function DepartmentFilter({ value, onChange }: DepartmentFilterProps) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-[200px]">
        <SelectValue placeholder="All Departments" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="all">All Departments</SelectItem>
        <SelectItem value="Engineering">Engineering</SelectItem>
        <SelectItem value="Human Resources">Human Resources</SelectItem>
        <SelectItem value="Sales">Sales</SelectItem>
        <SelectItem value="Marketing">Marketing</SelectItem>
        <SelectItem value="Finance">Finance</SelectItem>
        <SelectItem value="Operations">Operations</SelectItem>
      </SelectContent>
    </Select>
  );
}

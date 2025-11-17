export interface Employee {
  // Internal fields
  id: string;
  created_at: string;
  updated_at: string;

  // Source data (from Excel)
  employee_id: string;
  name: string;
  department_code: string;
  salary: number;
  hire_date: string;

  // Transformed data (from config.csv)
  department_name: string;
  annual_salary_eur: number;
  tenure_years: number;
}

export interface EmployeesResponse {
  items: Employee[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface EmployeeQueryParams {
  page?: number;
  page_size?: number;
  sort_by?: string;
  order?: 'asc' | 'desc';
  search?: string;
  department?: string;
}

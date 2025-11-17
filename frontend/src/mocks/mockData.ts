/**
 * Mock data based on actual input.xlsx file
 *
 * Contains realistic employee data for testing frontend functionality
 * without requiring a real backend.
 */

import type { Employee } from '@/types/employee.types';
import type { JobStatusResponse, JobError, Job } from '@/types/job.types';

/**
 * Department mapping from codes to full names
 */
const DEPARTMENTS: Record<string, string> = {
  DEV: 'Development',
  FIN: 'Finance',
  MKT: 'Marketing',
  HR: 'Human Resources',
  RND: 'Research & Development',
  OPS: 'Operations',
};

/**
 * Generate realistic employee data based on input.xlsx
 */
export const generateEmployees = (count: number = 100): Employee[] => {
  const names = [
    'Kevin Davis', 'Deborah Scott', 'Kenneth Johnson', 'Donna Moore', 'Sarah Martinez',
    'Matthew Campbell', 'Anthony Garcia', 'Melissa Jones', 'William Harris', 'Brian Moore',
    'Edward Thomas', 'Amanda Lee', 'Sarah Jones', 'Betty Robinson', 'Donna Ramirez',
    'Patricia Davis', 'Anthony Campbell', 'Amanda Davis', 'Christopher Ramirez', 'Kevin Martin',
    'Andrew Wright', 'Karen Thomas', 'Andrew Rodriguez', 'Edward Gonzalez', 'Michael Perez',
    'Kevin Brown', 'Brian Allen', 'Jessica Young', 'Mark Robinson', 'Edward Perez',
    'Margaret Lopez', 'Emily Miller', 'Richard Clark', 'James Harris', 'Emily Allen',
    'Patricia Lee', 'Paul Garcia', 'Linda Peterson', 'Joshua Wright', 'Betty Rodriguez',
    'Michelle Peterson', 'Matthew Jones', 'Karen Wright', 'David Taylor', 'Susan Perez',
    'Patricia Garcia', 'Charles Hernandez', 'George Martinez', 'Karen White', 'William Thompson',
  ];

  const deptCodes = ['DEV', 'FIN', 'MKT', 'HR', 'RND', 'OPS'];
  const employees: Employee[] = [];

  for (let i = 0; i < count; i++) {
    const deptCode = deptCodes[i % deptCodes.length];
    const hireDate = new Date(2015 + Math.floor(i / 100), (i % 12), 1 + (i % 28));
    const today = new Date();
    const tenureYears = Math.floor((today.getTime() - hireDate.getTime()) / (365.25 * 24 * 60 * 60 * 1000));
    const salary = 35000 + Math.floor(Math.random() * 65000);

    employees.push({
      // Internal fields
      id: `${crypto.randomUUID()}`,
      created_at: hireDate.toISOString(),
      updated_at: new Date().toISOString(),

      // Source data (from Excel)
      employee_id: `E${String(i + 1).padStart(4, '0')}`,
      name: names[i % names.length],
      department_code: deptCode,
      salary: salary,
      hire_date: hireDate.toISOString().split('T')[0],

      // Transformed data (from config.csv)
      department_name: DEPARTMENTS[deptCode],
      annual_salary_eur: Math.round(salary * 0.92), // USD to EUR conversion
      tenure_years: tenureYears,
    });
  }

  return employees;
};

/**
 * Mock employees database (500 records)
 */
export const MOCK_EMPLOYEES = generateEmployees(500);

/**
 * Mock job errors (simulating validation failures from Excel)
 */
export const MOCK_JOB_ERRORS: JobError[] = [
  {
    row: 15,
    field: 'salary',
    message: 'Invalid numeric value: expected number, got "fifty"',
  },
  {
    row: 142,
    field: 'department_code',
    message: 'Invalid department code: "fin" (expected uppercase)',
  },
  {
    row: 156,
    field: 'employee_id',
    message: 'Missing required field: employee_id',
  },
  {
    row: 223,
    field: 'department_code',
    message: 'Invalid department code: "ops" (expected uppercase)',
  },
  {
    row: 259,
    field: 'name',
    message: 'Name contains extra whitespace: "  Richard Allen  "',
  },
  {
    row: 329,
    field: 'department_code',
    message: 'Department code contains extra whitespace: "  HR  "',
  },
  {
    row: 468,
    field: 'department_code',
    message: 'Invalid department code: "hr" (expected uppercase)',
  },
  {
    row: 512,
    field: 'hire_date',
    message: 'Invalid date format: expected YYYY-MM-DD',
  },
];

/**
 * Mock active jobs storage
 */
interface MockJob {
  job_id: string;
  filename: string;
  file_size: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  current_step: string;
  started_at: string;
  completed_at: string | null;
  processed_rows: number; // Track actual progress
  employee_count: number;
}

export const MOCK_JOBS = new Map<string, MockJob>();

/**
 * Initialize with sample jobs for demo purposes
 */
function initializeSampleJobs() {
  // Sample completed job from 2 hours ago
  const completedJobId = 'demo-completed-job-001';
  const completedJob: MockJob = {
    job_id: completedJobId,
    filename: 'employees_2024_q4.xlsx',
    file_size: 245760, // ~240 KB
    status: 'completed',
    current_step: 'completed',
    started_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
    completed_at: new Date(Date.now() - 2 * 60 * 60 * 1000 + 12000).toISOString(),
    processed_rows: 508,
    employee_count: 500,
  };
  MOCK_JOBS.set(completedJobId, completedJob);

  // Sample completed job from yesterday
  const oldJobId = 'demo-completed-job-002';
  const oldJob: MockJob = {
    job_id: oldJobId,
    filename: 'january_payroll.xlsx',
    file_size: 189440, // ~185 KB
    status: 'completed',
    current_step: 'completed',
    started_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
    completed_at: new Date(Date.now() - 24 * 60 * 60 * 1000 + 12000).toISOString(),
    processed_rows: 508,
    employee_count: 500,
  };
  MOCK_JOBS.set(oldJobId, oldJob);

  // Sample failed job from 1 hour ago
  const failedJobId = 'demo-failed-job-001';
  const failedJob: MockJob = {
    job_id: failedJobId,
    filename: 'corrupted_data.xls',
    file_size: 98304, // ~96 KB
    status: 'failed',
    current_step: 'validating',
    started_at: new Date(Date.now() - 60 * 60 * 1000).toISOString(), // 1 hour ago
    completed_at: new Date(Date.now() - 60 * 60 * 1000 + 3000).toISOString(),
    processed_rows: 150,
    employee_count: 0,
  };
  MOCK_JOBS.set(failedJobId, failedJob);
}

// Initialize sample jobs on module load
initializeSampleJobs();

/**
 * Create a new mock job
 */
export function createMockJob(filename: string, fileSize: number): string {
  const job_id = crypto.randomUUID();
  const started_at = new Date().toISOString();

  MOCK_JOBS.set(job_id, {
    job_id,
    filename,
    file_size: fileSize,
    status: 'pending',
    current_step: 'pending',
    started_at,
    completed_at: null,
    processed_rows: 0,
    employee_count: 0,
  });

  // Simulate job progression
  simulateJobProgress(job_id);

  return job_id;
}

/**
 * Get mock job status
 */
export function getMockJobStatus(job_id: string): JobStatusResponse | null {
  const job = MOCK_JOBS.get(job_id);
  if (!job) return null;

  const total_rows = 508; // Based on Excel data
  const error_rows = job.status === 'completed' ? MOCK_JOB_ERRORS.length : 0;

  return {
    job_id: job.job_id,
    filename: job.filename,
    status: job.status,
    current_step: job.current_step,
    total_rows,
    processed_rows: job.processed_rows,
    error_rows,
    errors: job.status === 'completed' ? MOCK_JOB_ERRORS : [],
    started_at: job.started_at,
    completed_at: job.completed_at,
  };
}

/**
 * Simulate job processing progression
 */
function simulateJobProgress(job_id: string) {
  const job = MOCK_JOBS.get(job_id);
  if (!job) return;

  const total_rows = 508;
  const steps = [
    { name: 'pending', duration: 1000, rows: 0 },
    { name: 'reading', duration: 2000, rows: 100 },
    { name: 'validating', duration: 3000, rows: 300 },
    { name: 'transforming', duration: 4000, rows: 450 },
    { name: 'persisting', duration: 2000, rows: 500 },
  ];

  let currentStep = 0;

  const processStep = () => {
    const job = MOCK_JOBS.get(job_id);
    if (!job) return;

    if (currentStep === 0) {
      job.status = 'processing';
    }

    if (currentStep < steps.length) {
      const step = steps[currentStep];
      job.current_step = step.name;

      // Gradually increment processed_rows during this step
      const startRows = currentStep > 0 ? steps[currentStep - 1].rows : 0;
      const endRows = step.rows;
      const stepDuration = step.duration;
      const updateInterval = 200; // Update every 200ms
      const rowsPerUpdate = (endRows - startRows) / (stepDuration / updateInterval);

      let currentRows = startRows;
      const progressInterval = setInterval(() => {
        const job = MOCK_JOBS.get(job_id);
        if (!job) {
          clearInterval(progressInterval);
          return;
        }

        currentRows = Math.min(currentRows + rowsPerUpdate, endRows);
        job.processed_rows = Math.floor(currentRows);
      }, updateInterval);

      currentStep++;
      setTimeout(() => {
        clearInterval(progressInterval);
        processStep();
      }, stepDuration);
    } else {
      job.status = 'completed';
      job.current_step = 'completed';
      job.processed_rows = total_rows;
      job.completed_at = new Date().toISOString();

      // Calculate employee count (backend would merge into shared table)
      const employeeCount = total_rows - MOCK_JOB_ERRORS.length;
      job.employee_count = employeeCount;
      console.log(`[MOCK] Job ${job_id} completed - processed ${employeeCount} employees into shared table`);
    }
  };

  setTimeout(processStep, 500);
}

/**
 * Filter and paginate employees
 */
export function filterEmployees(params: {
  page?: number;
  page_size?: number;
  sort_by?: string;
  order?: 'asc' | 'desc';
  search?: string;
  department?: string;
}) {
  const {
    page = 1,
    page_size = 20,
    sort_by = 'employee_id',
    order = 'asc',
    search,
    department,
  } = params;

  let filtered = [...MOCK_EMPLOYEES];

  // Search filter
  if (search) {
    const searchLower = search.toLowerCase();
    filtered = filtered.filter(
      (emp) =>
        emp.name.toLowerCase().includes(searchLower) ||
        emp.employee_id.toLowerCase().includes(searchLower)
    );
  }

  // Department filter
  if (department) {
    filtered = filtered.filter((emp) => emp.department_name === department);
  }

  // Sort
  filtered.sort((a, b) => {
    const aValue = a[sort_by as keyof Employee];
    const bValue = b[sort_by as keyof Employee];

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return order === 'asc'
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue);
    }

    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return order === 'asc' ? aValue - bValue : bValue - aValue;
    }

    return 0;
  });

  // Paginate
  const total = filtered.length;
  const total_pages = Math.ceil(total / page_size);
  const start = (page - 1) * page_size;
  const end = start + page_size;
  const employees = filtered.slice(start, end);

  return {
    employees,
    total,
    page,
    page_size,
    total_pages,
  };
}

/**
 * Get all jobs with filtering and pagination
 */
export function getJobsList(params: {
  page?: number;
  page_size?: number;
  status?: 'pending' | 'processing' | 'completed' | 'failed';
  sort_by?: string;
  order?: 'asc' | 'desc';
}) {
  const {
    page = 1,
    page_size = 20,
    status,
    sort_by = 'started_at',
    order = 'desc',
  } = params;

  let jobs: Job[] = Array.from(MOCK_JOBS.values()).map((mockJob) => ({
    job_id: mockJob.job_id,
    filename: mockJob.filename,
    file_size: mockJob.file_size,
    status: mockJob.status,
    current_step: mockJob.current_step,
    total_rows: 508,
    processed_rows: mockJob.processed_rows,
    error_rows: mockJob.status === 'completed' ? MOCK_JOB_ERRORS.length : 0,
    successful_rows: mockJob.status === 'completed' ? 508 - MOCK_JOB_ERRORS.length : 0,
    employee_count: mockJob.employee_count,
    started_at: mockJob.started_at,
    completed_at: mockJob.completed_at,
  }));

  // Filter by status
  if (status) {
    jobs = jobs.filter((job) => job.status === status);
  }

  // Sort
  jobs.sort((a, b) => {
    const aValue = a[sort_by as keyof Job];
    const bValue = b[sort_by as keyof Job];

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return order === 'asc'
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue);
    }

    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return order === 'asc' ? aValue - bValue : bValue - aValue;
    }

    return 0;
  });

  // Paginate
  const total = jobs.length;
  const total_pages = Math.ceil(total / page_size);
  const start = (page - 1) * page_size;
  const end = start + page_size;
  const paginatedJobs = jobs.slice(start, end);

  return {
    jobs: paginatedJobs,
    total,
    page,
    page_size,
    total_pages,
  };
}


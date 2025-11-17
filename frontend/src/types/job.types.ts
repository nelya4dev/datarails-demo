export type JobStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface JobError {
  row: number;
  field: string;
  message: string;
}

export interface JobStatusResponse {
  id: string;
  filename: string;
  file_path: string;
  status: JobStatus;
  current_step: string | null;
  total_rows: number | null;
  processed_rows: number | null;
  error_rows: number | null;
  error_details: Record<string, unknown> | null;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface UploadResponse {
  job_id: string;
}

export interface Job {
  id: string;
  filename: string;
  file_path: string;
  status: JobStatus;
  current_step: string | null;
  total_rows: number | null;
  processed_rows: number | null;
  error_rows: number | null;
  error_details: Record<string, unknown> | null;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface JobsResponse {
  items: Job[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface JobsQueryParams {
  page?: number;
  page_size?: number;
  status?: JobStatus;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

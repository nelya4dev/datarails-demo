import api from './api';
import type { UploadResponse, JobStatusResponse, JobsResponse, JobsQueryParams } from '../types/job.types';
import type { EmployeesResponse, EmployeeQueryParams } from '../types/employee.types';

// Wrapped response type from backend
interface WrappedResponse<T> {
  success: boolean;
  data: T;
}

// Upload file
export const uploadFile = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<WrappedResponse<UploadResponse>>('/api/v1/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data.data;
};

// Get job status
export const getJobStatus = async (jobId: string): Promise<JobStatusResponse> => {
  const response = await api.get<WrappedResponse<JobStatusResponse>>(`/api/v1/upload/status/${jobId}`);
  return response.data.data;
};

// Get employees with filters and pagination
export const getEmployees = async (params: EmployeeQueryParams): Promise<EmployeesResponse> => {
  const response = await api.get<WrappedResponse<EmployeesResponse>>('/api/v1/employees', {
    params: {
      page: params.page || 1,
      size: params.page_size || 20,
      department: params.department,
    },
  });

  return response.data.data;
};

// Get all jobs with filters and pagination
export const getJobs = async (params: JobsQueryParams): Promise<JobsResponse> => {
  const response = await api.get<WrappedResponse<JobsResponse>>('/api/v1/upload/jobs', {
    params: {
      page: params.page || 1,
      size: params.page_size || 20,
      status: params.status,
    },
  });

  return response.data.data;
};

// Download error report
export const getErrorReportUrl = (jobId: string): string => {
  return `${import.meta.env.VITE_API_BASE_URL}/api/v1/upload/errors/${jobId}`;
};

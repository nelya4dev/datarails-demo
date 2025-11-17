import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { uploadFile } from '@/services/endpoints';
import { shouldRetryMutation, getMutationRetryDelay } from '@/utils/retryConfig';
import type { UploadResponse } from '@/types/job.types';

/**
 * Custom hook for uploading files
 *
 * Handles file upload to the backend and navigates to job status page on success.
 * Uses smart retry logic - only retries on network/gateway errors, not validation errors.
 *
 * @returns TanStack Query mutation result with mutate function
 *
 * @example
 * ```tsx
 * function FileUploader({ file }: { file: File }) {
 *   const { mutate, isPending, error } = useUpload();
 *
 *   const handleUpload = () => {
 *     mutate(file, {
 *       onError: (error) => {
 *         toast.error(`Upload failed: ${error.message}`);
 *       },
 *     });
 *   };
 *
 *   return (
 *     <Button onClick={handleUpload} disabled={isPending}>
 *       {isPending ? 'Uploading...' : 'Upload File'}
 *     </Button>
 *   );
 * }
 * ```
 */
export function useUpload() {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (file: File) => uploadFile(file),
    retry: shouldRetryMutation,
    retryDelay: getMutationRetryDelay,
    onSuccess: (data: UploadResponse) => {
      // Navigate to job detail page after successful upload
      navigate(`/jobs/${data.job_id}`);
    },
  });
}

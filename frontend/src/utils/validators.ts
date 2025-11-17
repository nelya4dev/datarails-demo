/**
 * File validation utilities for upload functionality
 */

const VALID_EXCEL_TYPES = [
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
  'application/vnd.ms-excel', // .xls
];

const MAX_FILE_SIZE = parseInt(import.meta.env.VITE_MAX_FILE_SIZE_MB || '10') * 1024 * 1024; // Default 10MB

/**
 * Validates if a file is an accepted Excel file type and size
 *
 * @param file - The file to validate
 * @returns Error message if invalid, null if valid
 *
 * @example
 * ```ts
 * const error = validateFile(selectedFile);
 * if (error) {
 *   console.error(error);
 * }
 * ```
 */
export const validateFile = (file: File): string | null => {
  // Check file type
  if (!VALID_EXCEL_TYPES.includes(file.type)) {
    return 'Only .xlsx and .xls files are supported';
  }

  // Check file size
  if (file.size > MAX_FILE_SIZE) {
    const maxSizeMB = MAX_FILE_SIZE / (1024 * 1024);
    return `File size must be less than ${maxSizeMB}MB`;
  }

  return null;
};

/**
 * Formats file size to human-readable format
 *
 * @param bytes - File size in bytes
 * @returns Formatted string (e.g., "2.5 MB")
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

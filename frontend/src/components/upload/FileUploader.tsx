import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload } from 'lucide-react';
import { validateFile } from '@/utils/validators';
import { cn } from '@/lib/utils';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  error?: string | null;
}

/**
 * FileUploader component with drag & drop functionality
 *
 * Allows users to select Excel files via drag & drop or file picker.
 * Validates file type and size before accepting.
 *
 * @example
 * ```tsx
 * <FileUploader
 *   onFileSelect={(file) => setSelectedFile(file)}
 *   selectedFile={selectedFile}
 *   error={validationError}
 * />
 * ```
 */
export function FileUploader({ onFileSelect, selectedFile, error }: FileUploaderProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        const validationError = validateFile(file);

        if (!validationError) {
          onFileSelect(file);
        }
      }
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
    },
    maxFiles: 1,
    multiple: false,
  });

  return (
    <div
      {...getRootProps()}
      className={cn(
        'border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors',
        'hover:border-primary hover:bg-accent/50',
        isDragActive && 'border-primary bg-accent',
        error && 'border-destructive',
        selectedFile && 'border-success bg-success/5'
      )}
      role="button"
      tabIndex={0}
      aria-label="File upload zone"
    >
      <input {...getInputProps()} aria-label="File input" />

      <div className="flex flex-col items-center gap-4">
        <div className={cn(
          'rounded-full p-4',
          isDragActive ? 'bg-primary/10' : 'bg-muted'
        )}>
          <Upload className={cn(
            'h-10 w-10',
            isDragActive ? 'text-primary' : 'text-muted-foreground'
          )} />
        </div>

        {isDragActive ? (
          <p className="text-lg font-medium text-primary">
            Drop the file here
          </p>
        ) : selectedFile ? (
          <div className="space-y-1">
            <p className="text-lg font-medium text-success">
              File selected
            </p>
            <p className="text-sm text-muted-foreground">
              Drop a new file to replace
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            <p className="text-lg font-medium">
              Drag & drop your Excel file here
            </p>
            <p className="text-sm text-muted-foreground">
              or click to browse
            </p>
            <p className="text-xs text-muted-foreground mt-2">
              Supports .xlsx and .xls files (max 10MB)
            </p>
          </div>
        )}

        {error && (
          <p className="text-sm text-destructive font-medium" role="alert">
            {error}
          </p>
        )}
      </div>
    </div>
  );
}

import { useState } from 'react';
import { X, Upload as UploadIcon } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ErrorAlert } from '@/components/common';
import { FileUploader, FilePreview } from '@/components/upload';
import { useUpload } from '@/hooks';
import { validateFile } from '@/utils/validators';

interface UploadSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

/**
 * UploadSidebar component - Floating sidebar for file uploads
 *
 * Appears as an overlay on the right side of the screen
 * Handles file selection, validation, and upload
 */
export function UploadSidebar({ isOpen, onClose }: UploadSidebarProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  const { mutate: uploadFile, isPending, error } = useUpload();

  const handleFileSelect = (file: File) => {
    const error = validateFile(file);
    if (error) {
      setValidationError(error);
      setSelectedFile(null);
    } else {
      setValidationError(null);
      setSelectedFile(file);
    }
  };

  const handleRemove = () => {
    setSelectedFile(null);
    setValidationError(null);
  };

  const handleUpload = () => {
    if (selectedFile) {
      uploadFile(selectedFile, {
        onSuccess: () => {
          // Close sidebar and reset state when upload succeeds
          onClose();
          setSelectedFile(null);
          setValidationError(null);
        }
      });
    }
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 z-40 transition-opacity"
        onClick={onClose}
      />

      {/* Sidebar */}
      <div className="fixed top-0 right-0 h-full w-full max-w-md bg-background border-l shadow-2xl z-50 overflow-y-auto">
        <div className="p-6 space-y-6">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <UploadIcon className="h-5 w-5 text-primary" />
              </div>
              <div>
                <h2 className="text-xl font-semibold">Upload Employee Data</h2>
                <p className="text-sm text-muted-foreground">
                  Upload an Excel file to process
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              className="h-8 w-8"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* File Uploader */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Select File</CardTitle>
              <CardDescription>
                Supports .xlsx or .xls files (max 10MB)
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FileUploader
                onFileSelect={handleFileSelect}
                selectedFile={selectedFile}
                error={validationError}
              />

              {selectedFile && (
                <FilePreview file={selectedFile} onRemove={handleRemove} />
              )}
            </CardContent>
          </Card>

          {/* Error Alert */}
          {error ? (
            <ErrorAlert error={error as Error} title="Upload Failed" />
          ) : null}

          {/* Upload Button */}
          <Button
            onClick={handleUpload}
            disabled={!selectedFile || isPending}
            className="w-full"
            size="lg"
          >
            {isPending ? 'Uploading...' : 'Upload File'}
          </Button>
        </div>
      </div>
    </>
  );
}

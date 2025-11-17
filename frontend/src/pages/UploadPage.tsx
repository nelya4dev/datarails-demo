import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ErrorAlert } from '@/components/common';
import { FileUploader, FilePreview } from '@/components/upload';
import { useUpload } from '@/hooks';
import { validateFile } from '@/utils/validators';

function UploadPage() {
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
      uploadFile(selectedFile);
    }
  };

  return (
    <div className="container max-w-2xl mx-auto py-8 px-4">
      <Card>
        <CardHeader>
          <CardTitle>Upload Employee Data</CardTitle>
          <CardDescription>
            Upload an Excel file (.xlsx or .xls) to process employee information
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <FileUploader
            onFileSelect={handleFileSelect}
            selectedFile={selectedFile}
            error={validationError}
          />

          {selectedFile && (
            <FilePreview file={selectedFile} onRemove={handleRemove} />
          )}

          {error ? (
            <ErrorAlert error={error as Error} title="Upload Failed" />
          ) : null}

          <Button
            onClick={handleUpload}
            disabled={!selectedFile || isPending}
            className="w-full"
            size="lg"
          >
            {isPending ? 'Uploading...' : 'Upload File'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

export default UploadPage;

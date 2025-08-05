import React, { useState, useRef } from 'react';

type Props = {
    onUpload: (file: File) => void;
};

const FileUploader: React.FC<Props> = ({ onUpload }) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) setSelectedFile(file);
    };

    const handleClick = () => {
        if (selectedFile) {
            onUpload(selectedFile);
            setSelectedFile(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    return (
        <div style={{ marginBottom: '1rem' }}>
            <input
                ref={fileInputRef}
                type="file"
                accept=".txt,.log,.csv"
                onChange={handleFileChange}
            />
            <button onClick={handleClick} disabled={!selectedFile} className="btn">
                Upload
            </button>
        </div>
    );
};

export default FileUploader;

import React, { useState } from 'react';

type Props = {
    onUpload: (file: File) => void;
};

const FileUploader: React.FC<Props> = ({ onUpload }) => {
    const [File, setFile] = useState<File | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) setFile(file);
    };

    const handleClick = () => {
        if (File) onUpload(File);
    };

    return (
        <div style={{ marginBottom: '1rem' }}>
            <input
                type="file"
                accept=".txt,.log,.csv"
                onChange={handleFileChange}
            />
            <button onClick={handleClick} disabled={!File} className="btn">
                Upload
            </button>
        </div>
    );
};

export default FileUploader;

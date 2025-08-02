import { useState } from 'react';
import SummaryTable from '../components/summaryTable';

export default function Home() {
    const [file, setFile] = useState<File | null>(null);//use state to manage file input to ensure UI updates correctly
    const [uploadStatus, setUploadStatus] = useState('');
    const [analysisResult, setAnalysisResult] = useState<any>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.length) {// Check if files are selected
            setFile(e.target.files[0]);//set the first file selected because we only allow one file for now
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setUploadStatus('No file selected.');
            return;
        }

        const formData = new FormData();//set up form data to send file
        formData.append('file', file);

        try {
            const res = await fetch('http://127.0.0.1:5000/upload', {// make the POST request to the backend
                method: 'POST',
                body: formData,
            });
            const contentType = res.headers.get("Content-Type") || "";
            let data: any = {};

            if (contentType.includes("application/json")) {//ensure we are getting JSON response
                data = await res.json();
            } else {
                throw new Error("Unexpected response format from server.");//if not JSON, throw error
            }

            if (res.ok && data.success) {
                setUploadStatus(`Upload successful: ${data.saved_filename}`);//set the status to success
                fetchAnalysis(data.saved_filename);
            } else {
                setUploadStatus(`Upload failed: ${data.error || "Unknown error."}`);
            }
        } catch (err) {
            console.error(err);
            setUploadStatus('Upload failed.');
        }
    };

    const fetchAnalysis = async (filename: string) => {
        try {
            const res = await fetch(`http://127.0.0.1:5000/analyze/${filename}`);
            const data = await res.json();
            setAnalysisResult(data);
        } catch (err) {
            console.error(err);
            setUploadStatus('Analysis failed.');
        }
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '100%', boxSizing: 'border-box' }}>
            <h1>Log File Analyzer</h1>

            <input type="file" accept=".txt,.log,.csv" onChange={handleFileChange} />
            <button disabled={!file} onClick={handleUpload}>Upload</button>

            <p>{uploadStatus}</p>

            {analysisResult?.summary && analysisResult?.summary.timeline && (
                <div>
                    <h2>Analysis Summary</h2>
                    <p>Total entries: {analysisResult.summary.total_entries}</p>
                    <p>High risk entries: {analysisResult.summary.high_risk_count}</p>
                    <p>Critical risk entries: {analysisResult.summary.critical_risk_count}</p>

                    <h3>Timeline of Events</h3>
                    <SummaryTable data={analysisResult.summary.timeline} />
                </div>
            )}
        </div>
    );
}

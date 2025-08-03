import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import AnalysisSummary from '../components/analysisSummary';
import FileUploader from '../components/fileUploader';
import LogoutButton from '../components/LogoutButton';

export default function Home() {
    const router = useRouter();
    const [uploadStatus, setUploadStatus] = useState('');
    const [analysisResult, setAnalysisResult] = useState<any>(null);

    const checkAuth = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/login');
            return;
        }

        try {
            const res = await fetch('http://127.0.0.1:5000/verifyJWT', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!res.ok) throw new Error('Invalid token');

        } catch (err) {
            localStorage.removeItem('token'); // cleanup
            router.push('/login');
        }
    };

    useEffect(() => {
        checkAuth();
    }, [router]);

    const handleUpload = async (file: File) => {

        const formData = new FormData();//set up form data to send file
        formData.append('file', file);

        try {
            const token = localStorage.getItem('token');
            const res = await fetch('http://127.0.0.1:5000/upload', {// make the POST request to the backend
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${token}`
                },
                body: formData
            });
            if (res.status === 401) {
                return checkAuth(); // recheck auth if unauthorized
            }
            const contentType = res.headers.get("Content-Type") || "";
            let data: any = {};

            if (contentType.includes("application/json")) {//ensure we are getting JSON response
                data = await res.json();
            } else {
                throw new Error("Invalid server response.");//if not JSON, throw error
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
            const token = localStorage.getItem('token');
            const res = await fetch(`http://127.0.0.1:5000/analyze/${filename}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (res.status === 401) {
                return checkAuth(); // recheck auth if unauthorized
            }
            const data = await res.json();
            setAnalysisResult(data);
        } catch (err) {
            console.error(err);
            setUploadStatus('Analysis failed.');
        }
    };

    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <h1>Log File Analyzer</h1>
                <LogoutButton />
            </div>

            <FileUploader onUpload={handleUpload} />

            <p style={{ fontStyle: 'italic', color: 'gray' }}>{uploadStatus}</p>

            {analysisResult?.summary?.timeline && (
                <AnalysisSummary summary={analysisResult.summary} />
            )}
        </div>
    );
}

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/router';
import AnalysisSummary from '../components/analysisSummary';
import FileUploader from '../components/fileUploader';
import LogoutButton from '../components/LogoutButton';

export default function Home() {
    const router = useRouter();
    const [uploadStatus, setUploadStatus] = useState('');
    const [analysisResult, setAnalysisResult] = useState<any>(null);
    const backendUrl =
        typeof window === "undefined"
            ? "http://backend:5000" // SSR (inside Docker)
            : "http://localhost:5000"; // browser (outside Docker)

    const checkAuth = useCallback(async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/login');
            return;
        }

        try {
            console.log('Checking authentication...');
            const res = await fetch(`${backendUrl}/verifyJWT`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!res.ok) throw new Error('Invalid token');
        } catch (err) {
            localStorage.removeItem('token');
            router.push('/login');
        }
    }, [router]);

    useEffect(() => {
        checkAuth();
    }, [checkAuth]);

    const handleUpload = async (file: File) => {

        const formData = new FormData();//Set up form data to send file
        formData.append('file', file);

        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`${backendUrl}/upload`, {// Make the POST request to the backend
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${token}`
                },
                body: formData
            });
            if (res.status === 401) {
                return checkAuth(); // Recheck auth if unauthorized
            }
            const contentType = res.headers.get("Content-Type") || "";
            let data: any = {};

            if (contentType.includes("application/json")) {//Ensure we are getting JSON response
                data = await res.json();
            } else {
                throw new Error("Invalid server response.");//If not JSON, throw error
            }

            if (res.ok && data.success) {
                setUploadStatus(`Upload successful: ${data.saved_filename}`);//Set the status to success
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
            const res = await fetch(`${backendUrl}/analyze/${filename}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (res.status === 401) {
                return checkAuth(); // Recheck auth if unauthorized
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

import { useState } from 'react';
import { useRouter } from 'next/router';

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const router = useRouter();
    const backendUrl =
        typeof window === "undefined"
            ? "http://backend:5000" // SSR (inside Docker)
            : "http://localhost:5000"; // browser (outside Docker)

    const handleLogin = async () => {
        setLoading(true);
        setError('');
        try {
            const res = await fetch(`${backendUrl}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await res.json();

            if (res.ok && data.access_token) {
                localStorage.setItem('token', data.access_token);
                router.push('/');
            } else {
                setError('Invalid username or password.');
            }
        } catch (err) {
            setError('An unexpected error occurred.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') handleLogin();
    };

    return (
        <div className="container">
            <div className="loginBox">
                <h1 className="title">Login</h1>
                <input
                    className="input"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    onKeyDown={handleKeyDown}
                />
                <input
                    className="input"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    onKeyDown={handleKeyDown}
                />
                <button className="button" onClick={handleLogin} disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
                {error && <div className="error">{error}</div>}
            </div>
        </div>
    );
}

import React from 'react';
import { useRouter } from 'next/router';

const LogoutButton = () => {
    const router = useRouter();

    const handleLogout = () => {
        localStorage.removeItem('token');
        router.push('/login');
    };

    return (
        <button onClick={handleLogout} className="btn danger">
            Logout
        </button>
    );
};

export default LogoutButton;

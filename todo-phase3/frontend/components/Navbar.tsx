'use client';

/**
Navigation bar component.
Displays app title, username, and logout button.
*/
import { getCurrentUser } from '@/lib/auth';
import Link from 'next/link';

interface NavbarProps {
    username: string;
    onLogout: () => void;
}

export default function Navbar({ username, onLogout }: NavbarProps) {
    return (
        <nav style={{
            backgroundColor: '#343a40',
            padding: '15px 30px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '30px' }}>
                <Link href="/" style={{
                    color: 'white',
                    fontSize: '24px',
                    margin: 0,
                    fontWeight: 'bold',
                    textDecoration: 'none'
                }}>
                    Todo App
                </Link>
                <Link href="/chat" style={{
                    color: 'white',
                    fontSize: '16px',
                    textDecoration: 'none',
                    padding: '8px 12px',
                    borderRadius: '4px',
                    transition: 'background-color 0.2s'
                }} onMouseOver={(e) => e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.1)'}
                     onMouseOut={(e) => e.currentTarget.style.backgroundColor = ''}>
                    Chat
                </Link>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                <span style={{ color: 'white', fontSize: '16px' }}>
                    Welcome, {username}!
                </span>
                <button
                    onClick={onLogout}
                    style={{
                        backgroundColor: '#dc3545',
                        color: 'white',
                        padding: '8px 16px',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: 'bold'
                    }}
                >
                    Logout
                </button>
            </div>
        </nav>
    );
}

import { useState, useEffect } from 'react';

let toastId = 0;

export const toast = {
    success: (message) => {
        const event = new CustomEvent('toast', { detail: { type: 'success', message, id: toastId++ } });
        window.dispatchEvent(event);
    },
    error: (message) => {
        const event = new CustomEvent('toast', { detail: { type: 'error', message, id: toastId++ } });
        window.dispatchEvent(event);
    },
    info: (message) => {
        const event = new CustomEvent('toast', { detail: { type: 'info', message, id: toastId++ } });
        window.dispatchEvent(event);
    },
};

export default function Toast() {
    const [toasts, setToasts] = useState([]);

    useEffect(() => {
        const handleToast = (event) => {
            const newToast = event.detail;
            setToasts((prev) => [...prev, newToast]);

            setTimeout(() => {
                setToasts((prev) => prev.filter((t) => t.id !== newToast.id));
            }, 3000);
        };

        window.addEventListener('toast', handleToast);
        return () => window.removeEventListener('toast', handleToast);
    }, []);

    const types = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        info: 'bg-blue-500',
    };

    return (
        <div className="fixed top-4 right-4 z-50 space-y-2">
            {toasts.map((t) => (
                <div
                    key={t.id}
                    className={`${types[t.type]} text-white px-6 py-3 rounded-lg shadow-lg animate-slide-down`}
                >
                    {t.message}
                </div>
            ))}
        </div>
    );
}

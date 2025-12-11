export default function Button({ children, variant = 'primary', loading = false, className = '', ...props }) {
    const variants = {
        primary: 'btn-primary',
        secondary: 'btn-secondary',
        danger: 'btn-danger',
    };

    return (
        <button
            className={`btn ${variants[variant]} ${className} ${loading ? 'opacity-70 cursor-wait' : ''}`}
            disabled={loading || props.disabled}
            {...props}
        >
            {loading ? (
                <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Loading...</span>
                </div>
            ) : (
                children
            )}
        </button>
    );
}

import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Input from '../components/Input';
import Button from '../components/Button';
import { toast } from '../components/Toast';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});
    const { login } = useAuth();
    const navigate = useNavigate();

    const validate = () => {
        const newErrors = {};
        if (!email) newErrors.email = 'Email is required';
        if (!password) newErrors.password = 'Password is required';
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validate()) return;

        setLoading(true);
        try {
            await login(email, password);
            toast.success('Login successful!');
            navigate('/projects');
        } catch (error) {
            // Show detailed backend message when available for easier debugging
            const backendMessage = error.response?.data?.detail || error.response?.data?.error?.message || JSON.stringify(error.response?.data);
            console.error('Login error:', error.response?.data || error.message);
            toast.error(backendMessage || error.message || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8 animate-fade-in">
                    <div className="inline-block w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
                        <span className="text-3xl font-bold text-white">HI</span>
                    </div>
                    <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent">
                        Welcome Back
                    </h1>
                    <p className="text-gray-400">Sign in to your account</p>
                </div>

                <div className="card animate-slide-up">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <Input
                            label="Email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            error={errors.email}
                            placeholder="you@example.com"
                        />

                        <Input
                            label="Password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            error={errors.password}
                            placeholder="••••••••"
                        />

                        <Button type="submit" loading={loading} className="w-full">
                            Sign In
                        </Button>
                    </form>

                    <div className="mt-6 text-center">
                        <p className="text-gray-400">
                            Don't have an account?{' '}
                            <Link to="/signup" className="text-primary-400 hover:text-primary-300 font-medium">
                                Sign up
                            </Link>
                        </p>
                    </div>

                    <div className="mt-6 p-4 glass rounded-lg">
                        <p className="text-sm text-gray-400 mb-2">Demo credentials:</p>
                        <p className="text-xs text-white font-semibold">alice@example.com / password123</p>
                        <p className="text-xs text-white font-semibold">bob@example.com / password123</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

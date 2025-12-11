import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Toast from './components/Toast';
import Spinner from './components/Spinner';
import Login from './pages/Login';
import Signup from './pages/Signup';
import ProjectsList from './pages/ProjectsList';
import ProjectDetail from './pages/ProjectDetail';
import IssueDetail from './pages/IssueDetail';

function ProtectedRoute({ children }) {
    const { user, loading } = useAuth();

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" />
            </div>
        );
    }

    return user ? children : <Navigate to="/login" />;
}

function PublicRoute({ children }) {
    const { user, loading } = useAuth();

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" />
            </div>
        );
    }

    return !user ? children : <Navigate to="/projects" />;
}

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Toast />
                <Routes>
                    <Route path="/" element={<Navigate to="/projects" />} />
                    <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
                    <Route path="/signup" element={<PublicRoute><Signup /></PublicRoute>} />
                    <Route path="/projects" element={<ProtectedRoute><ProjectsList /></ProtectedRoute>} />
                    <Route path="/projects/:projectId" element={<ProtectedRoute><ProjectDetail /></ProtectedRoute>} />
                    <Route path="/issues/:issueId" element={<ProtectedRoute><IssueDetail /></ProtectedRoute>} />
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;

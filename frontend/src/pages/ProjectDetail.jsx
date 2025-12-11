import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import Input from '../components/Input';
import Select from '../components/Select';
import Modal from '../components/Modal';
import Spinner from '../components/Spinner';
import { toast } from '../components/Toast';
import api from '../utils/api';

export default function ProjectDetail() {
    const { projectId } = useParams();
    const navigate = useNavigate();
    const [issues, setIssues] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [search, setSearch] = useState('');
    const [statusFilter, setStatusFilter] = useState('');
    const [priorityFilter, setPriorityFilter] = useState('');
    const [sortBy, setSortBy] = useState('created_at');
    const [formData, setFormData] = useState({ title: '', description: '', priority: 'medium' });
    const [creating, setCreating] = useState(false);

    useEffect(() => {
        fetchIssues();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [projectId, search, statusFilter, priorityFilter, sortBy]);

    const fetchIssues = async () => {
        try {
            const params = new URLSearchParams();
            if (search) params.append('q', search);
            if (statusFilter) params.append('status', statusFilter);
            if (priorityFilter) params.append('priority', priorityFilter);
            params.append('sort', sortBy);

            const response = await api.get(`/projects/${projectId}/issues?${params}`);
            setIssues(response.data);
        } catch (error) {
            toast.error('Failed to load issues');
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        setCreating(true);
        try {
            await api.post(`/projects/${projectId}/issues`, formData);
            toast.success('Issue created successfully!');
            setShowModal(false);
            setFormData({ title: '', description: '', priority: 'medium' });
            fetchIssues();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to create issue');
        } finally {
            setCreating(false);
        }
    };

    const getStatusBadge = (status) => {
        const badges = {
            open: 'badge-open',
            in_progress: 'badge-in-progress',
            resolved: 'badge-resolved',
            closed: 'badge-closed',
        };
        return `badge ${badges[status]}`;
    };

    const getPriorityBadge = (priority) => {
        const badges = {
            low: 'badge-low',
            medium: 'badge-medium',
            high: 'badge-high',
            critical: 'badge-critical',
        };
        return `badge ${badges[priority]}`;
    };

    if (loading) {
        return (
            <div className="min-h-screen">
                <Navbar />
                <div className="flex items-center justify-center h-96">
                    <Spinner size="lg" />
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen">
            <Navbar />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <button onClick={() => navigate('/projects')} className="text-gray-400 hover:text-white mb-2">
                            ← Back to Projects
                        </button>
                        <h1 className="text-3xl font-bold mb-2">Issues</h1>
                    </div>
                    <Button onClick={() => setShowModal(true)}>
                        + New Issue
                    </Button>
                </div>

                <div className="card mb-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <Input
                            placeholder="Search issues..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                        <Select
                            options={[
                                { value: '', label: 'All Statuses' },
                                { value: 'open', label: 'Open' },
                                { value: 'in_progress', label: 'In Progress' },
                                { value: 'resolved', label: 'Resolved' },
                                { value: 'closed', label: 'Closed' },
                            ]}
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                        />
                        <Select
                            options={[
                                { value: '', label: 'All Priorities' },
                                { value: 'low', label: 'Low' },
                                { value: 'medium', label: 'Medium' },
                                { value: 'high', label: 'High' },
                                { value: 'critical', label: 'Critical' },
                            ]}
                            value={priorityFilter}
                            onChange={(e) => setPriorityFilter(e.target.value)}
                        />
                        <Select
                            options={[
                                { value: 'created_at', label: 'Newest First' },
                                { value: 'updated_at', label: 'Recently Updated' },
                                { value: 'priority', label: 'Priority' },
                                { value: 'status', label: 'Status' },
                            ]}
                            value={sortBy}
                            onChange={(e) => setSortBy(e.target.value)}
                        />
                    </div>
                </div>

                {issues.length === 0 ? (
                    <div className="card text-center py-12">
                        <div className="text-6xl mb-4">🐛</div>
                        <h3 className="text-xl font-semibold mb-2">No issues found</h3>
                        <p className="text-gray-400 mb-4">Create your first issue to track bugs</p>
                        <Button onClick={() => setShowModal(true)}>Create Issue</Button>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {issues.map((issue) => (
                            <div
                                key={issue.id}
                                onClick={() => navigate(`/issues/${issue.id}`)}
                                className="card cursor-pointer hover:scale-[1.02] transition-transform"
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-2">
                                            <span className={getStatusBadge(issue.status)}>
                                                {issue.status.replace('_', ' ')}
                                            </span>
                                            <span className={getPriorityBadge(issue.priority)}>
                                                {issue.priority}
                                            </span>
                                        </div>
                                        <h3 className="text-lg font-semibold mb-1">{issue.title}</h3>
                                        <p className="text-gray-400 text-sm line-clamp-2">{issue.description}</p>
                                        <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
                                            <span>Reporter: {issue.reporter_name}</span>
                                            {issue.assignee_name && <span>Assignee: {issue.assignee_name}</span>}
                                            <span>{new Date(issue.created_at).toLocaleDateString()}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Create New Issue">
                <form onSubmit={handleCreate} className="space-y-4">
                    <Input
                        label="Title"
                        value={formData.title}
                        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                        placeholder="Issue title"
                        required
                    />
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">Description</label>
                        <textarea
                            className="input"
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            placeholder="Describe the issue..."
                            rows={4}
                        />
                    </div>
                    <Select
                        label="Priority"
                        options={[
                            { value: 'low', label: 'Low' },
                            { value: 'medium', label: 'Medium' },
                            { value: 'high', label: 'High' },
                            { value: 'critical', label: 'Critical' },
                        ]}
                        value={formData.priority}
                        onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    />
                    <Button type="submit" loading={creating} className="w-full">
                        Create Issue
                    </Button>
                </form>
            </Modal>
        </div>
    );
}

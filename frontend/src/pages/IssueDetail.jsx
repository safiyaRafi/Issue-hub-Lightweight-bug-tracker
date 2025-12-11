import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import Select from '../components/Select';
import Spinner from '../components/Spinner';
import { toast } from '../components/Toast';
import api from '../utils/api';

export default function IssueDetail() {
    const { issueId } = useParams();
    const navigate = useNavigate();
    const [issue, setIssue] = useState(null);
    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [commentBody, setCommentBody] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [isMaintainer, setIsMaintainer] = useState(false);

    useEffect(() => {
        const fetchIssue = async () => {
            try {
                const response = await api.get(`/issues/${issueId}`);
                setIssue(response.data);
                setIsMaintainer(true);
            } catch (error) {
                toast.error('Failed to load issue');
                navigate('/projects');
            } finally {
                setLoading(false);
            }
        };

        const fetchComments = async () => {
            try {
                const response = await api.get(`/issues/${issueId}/comments`);
                setComments(response.data);
            } catch (error) {
                console.error('Failed to load comments');
            }
        };

        fetchIssue();
        fetchComments();
    }, [issueId, navigate]);

    const handleAddComment = async (e) => {
        e.preventDefault();
        if (!commentBody.trim()) return;

        setSubmitting(true);
        try {
            await api.post(`/issues/${issueId}/comments`, { body: commentBody });
            setCommentBody('');
            toast.success('Comment added');
            const response = await api.get(`/issues/${issueId}/comments`);
            setComments(response.data);
        } catch (error) {
            toast.error('Failed to add comment');
        } finally {
            setSubmitting(false);
        }
    };

    const handleUpdateStatus = async (newStatus) => {
        try {
            await api.patch(`/issues/${issueId}`, { status: newStatus });
            toast.success('Status updated');
            const response = await api.get(`/issues/${issueId}`);
            setIssue(response.data);
        } catch (error) {
            toast.error('Failed to update status');
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
                <button onClick={() => navigate(-1)} className="text-gray-400 hover:text-white mb-4">
                    ← Back
                </button>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Main Content */}
                    <div className="lg:col-span-2 space-y-6">
                        <div className="card">
                            <div className="flex items-start gap-3 mb-4">
                                <span className={getStatusBadge(issue.status)}>
                                    {issue.status.replace('_', ' ')}
                                </span>
                                <span className={getPriorityBadge(issue.priority)}>
                                    {issue.priority}
                                </span>
                            </div>
                            <h1 className="text-3xl font-bold mb-4">{issue.title}</h1>
                            <p className="text-gray-300 whitespace-pre-wrap">{issue.description || 'No description provided'}</p>
                        </div>

                        {/* Comments */}
                        <div className="card">
                            <h2 className="text-xl font-semibold mb-4">Comments ({comments.length})</h2>

                            <div className="space-y-4 mb-6">
                                {comments.map((comment) => (
                                    <div key={comment.id} className="glass-dark rounded-lg p-4">
                                        <div className="flex items-center gap-2 mb-2">
                                            <span className="font-semibold">{comment.author_name}</span>
                                            <span className="text-xs text-gray-500">
                                                {new Date(comment.created_at).toLocaleString()}
                                            </span>
                                        </div>
                                        <p className="text-gray-300">{comment.body}</p>
                                    </div>
                                ))}
                            </div>

                            <form onSubmit={handleAddComment}>
                                <textarea
                                    className="input mb-3"
                                    value={commentBody}
                                    onChange={(e) => setCommentBody(e.target.value)}
                                    placeholder="Add a comment..."
                                    rows={3}
                                    required
                                />
                                <Button type="submit" loading={submitting}>
                                    Add Comment
                                </Button>
                            </form>
                        </div>
                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        <div className="card">
                            <h3 className="font-semibold mb-4">Details</h3>
                            <div className="space-y-3 text-sm">
                                <div>
                                    <span className="text-gray-400">Reporter:</span>
                                    <p className="font-medium">{issue.reporter_name}</p>
                                </div>
                                <div>
                                    <span className="text-gray-400">Assignee:</span>
                                    <p className="font-medium">{issue.assignee_name || 'Unassigned'}</p>
                                </div>
                                <div>
                                    <span className="text-gray-400">Created:</span>
                                    <p className="font-medium">{new Date(issue.created_at).toLocaleString()}</p>
                                </div>
                                <div>
                                    <span className="text-gray-400">Updated:</span>
                                    <p className="font-medium">{new Date(issue.updated_at).toLocaleString()}</p>
                                </div>
                            </div>
                        </div>

                        {isMaintainer && (
                            <div className="card">
                                <h3 className="font-semibold mb-4">Actions</h3>
                                <Select
                                    label="Change Status"
                                    options={[
                                        { value: 'open', label: 'Open' },
                                        { value: 'in_progress', label: 'In Progress' },
                                        { value: 'resolved', label: 'Resolved' },
                                        { value: 'closed', label: 'Closed' },
                                    ]}
                                    value={issue.status}
                                    onChange={(e) => handleUpdateStatus(e.target.value)}
                                />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import Input from '../components/Input';
import Modal from '../components/Modal';
import Spinner from '../components/Spinner';
import { toast } from '../components/Toast';
import api from '../utils/api';

export default function ProjectsList() {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({ name: '', key: '', description: '' });
    const [creating, setCreating] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        fetchProjects();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const fetchProjects = async () => {
        try {
            const response = await api.get('/projects');
            setProjects(response.data);
        } catch (error) {
            toast.error('Failed to load projects');
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        setCreating(true);
        try {
            await api.post('/projects', formData);
            toast.success('Project created successfully!');
            setShowModal(false);
            setFormData({ name: '', key: '', description: '' });
            fetchProjects();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to create project');
        } finally {
            setCreating(false);
        }
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
                        <h1 className="text-3xl font-bold mb-2">Projects</h1>
                        <p className="text-gray-400">Manage your bug tracking projects</p>
                    </div>
                    <Button onClick={() => setShowModal(true)}>
                        + New Project
                    </Button>
                </div>

                {projects.length === 0 ? (
                    <div className="card text-center py-12">
                        <div className="text-6xl mb-4">📋</div>
                        <h3 className="text-xl font-semibold mb-2">No projects yet</h3>
                        <p className="text-gray-400 mb-4">Create your first project to get started</p>
                        <Button onClick={() => setShowModal(true)}>Create Project</Button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {projects.map((project) => (
                            <div
                                key={project.id}
                                onClick={() => navigate(`/projects/${project.id}`)}
                                className="card cursor-pointer hover:scale-105 transition-transform"
                            >
                                <div className="flex items-start justify-between mb-4">
                                    <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                                        <span className="text-white font-bold">{project.key}</span>
                                    </div>
                                </div>
                                <h3 className="text-xl font-semibold mb-2">{project.name}</h3>
                                <p className="text-gray-400 text-sm line-clamp-2">{project.description || 'No description'}</p>
                                <div className="mt-4 pt-4 border-t border-white/10">
                                    <span className="text-xs text-gray-500">
                                        Created {new Date(project.created_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Create New Project">
                <form onSubmit={handleCreate} className="space-y-4">
                    <Input
                        label="Project Name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        placeholder="My Awesome Project"
                        required
                    />
                    <Input
                        label="Project Key"
                        value={formData.key}
                        onChange={(e) => setFormData({ ...formData, key: e.target.value.toUpperCase() })}
                        placeholder="MAP"
                        required
                        maxLength={10}
                    />
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">Description</label>
                        <textarea
                            className="input"
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            placeholder="Project description..."
                            rows={3}
                        />
                    </div>
                    <Button type="submit" loading={creating} className="w-full">
                        Create Project
                    </Button>
                </form>
            </Modal>
        </div>
    );
}

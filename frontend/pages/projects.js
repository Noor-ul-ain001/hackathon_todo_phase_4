import Head from 'next/head'
import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'

export default function Projects() {
  const { user } = useAuth()
  const userId = user?.id || 'user_123'
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const [projects, setProjects] = useState([])
  const [filteredProjects, setFilteredProjects] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [showNewProjectModal, setShowNewProjectModal] = useState(false)
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    dueDate: ''
  })
  const [filterStatus, setFilterStatus] = useState('all') // all, active, completed, pending
  const [sortOption, setSortOption] = useState('newest') // newest, oldest, name, progress
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedProject, setSelectedProject] = useState(null)
  const [showProjectDetails, setShowProjectDetails] = useState(false)

  // Fetch projects on mount
  useEffect(() => {
    if (userId) {
      fetchProjects()
    }
  }, [userId])

  // Apply filtering and sorting when projects, filterStatus, sortOption, or searchQuery change
  useEffect(() => {
    let result = [...projects];

    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(project =>
        project.name.toLowerCase().includes(query) ||
        (project.description && project.description.toLowerCase().includes(query))
      );
    }

    // Apply status filter
    if (filterStatus !== 'all') {
      result = result.filter(project => project.status === filterStatus);
    }

    // Apply sorting
    switch (sortOption) {
      case 'newest':
        result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        break;
      case 'oldest':
        result.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
        break;
      case 'name':
        result.sort((a, b) => a.name.localeCompare(b.name));
        break;
      case 'progress':
        result.sort((a, b) => b.progress - a.progress);
        break;
      default:
        break;
    }

    setFilteredProjects(result);
  }, [projects, filterStatus, sortOption, searchQuery])

  const fetchProjects = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/projects`)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const projectsData = await response.json()
      // Calculate progress from task stats
      const enhancedProjects = projectsData.map(project => ({
        ...project,
        progress: project.tasks?.progress || (project.status === 'completed' ? 100 : 0),
        members: project.tasks?.members || 1,
        dueDate: project.due_date || null
      }))
      setProjects(enhancedProjects)
    } catch (error) {
      console.error('Failed to fetch projects:', error)
      setProjects([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateProject = async () => {
    if (!newProject.name.trim()) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: newProject.name,
          description: newProject.description || null,
          due_date: newProject.dueDate || null
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const createdProject = await response.json()

      // Add to local state
      setProjects([{
        ...createdProject,
        progress: 0,
        members: 1,
        dueDate: createdProject.due_date,
        tasks: { completed: 0, total: 0 }
      }, ...projects])

      setNewProject({ name: '', description: '', dueDate: '' })
      setShowNewProjectModal(false)
    } catch (error) {
      console.error('Failed to create project:', error)
      alert('Failed to create project. Please try again.')
    }
  }

  const handleUpdateProjectStatus = async (projectId, newStatus) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/projects/${projectId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          status: newStatus
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const updatedProject = await response.json()

      // Update the project in local state
      setProjects(projects.map(project =>
        project.id === projectId
          ? { ...project, status: updatedProject.status }
          : project
      ))
    } catch (error) {
      console.error('Failed to update project status:', error)
      alert('Failed to update project status. Please try again.')
    }
  }

  const handleDeleteProject = async (projectId) => {
    if (!window.confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/projects/${projectId}`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Remove the project from local state
      setProjects(projects.filter(project => project.id !== projectId));
    } catch (error) {
      console.error('Failed to delete project:', error);
      alert('Failed to delete project. Please try again.');
    }
  }

  const handleViewProjectDetails = (project) => {
    setSelectedProject(project);
    setShowProjectDetails(true);
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-teal-100 text-teal-700 border-teal-300'
      case 'completed': return 'bg-green-100 text-green-700 border-green-300'
      case 'pending': return 'bg-yellow-100 text-yellow-700 border-yellow-300'
      default: return 'bg-slate-100 text-slate-600 border-slate-300'
    }
  }

  return (
    <>
      <Head>
        <title>Projects - TaskFlow</title>
        <meta name="description" content="TaskFlow Projects" />
      </Head>

      {/* Header */}
      <div className="bg-brand-card-bg/80 backdrop-blur-sm border-b border-brand-card-border px-4 py-3 md:px-8 md:py-6 animate-fadeInDown">
        <h1 className="text-3xl font-bold text-white mb-1">
          <span className="bg-gradient-to-r from-brand-button to-brand-button-hover bg-clip-text text-transparent">Projects</span>
        </h1>
        <p className="text-white/70 text-sm">Manage your projects and teams</p>
      </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-4 py-3 md:px-8 md:py-6 animate-fadeIn">
          <div className="max-w-6xl mx-auto">
            {/* New Project Button */}
            <div className="mb-6 flex justify-end animate-fadeInDown animate-delay-100">
              <button
                onClick={() => setShowNewProjectModal(true)}
                className="px-6 py-2.5 bg-gradient-to-r from-brand-button to-brand-button-hover text-white rounded-xl font-semibold hover:from-brand-button-hover hover:to-brand-button transition-all inline-flex items-center space-x-2 shadow-lg shadow-brand-button/30 hover-lift"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span>New Project</span>
              </button>
            </div>

            {/* Search, Filter and Sort Controls */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
              <div className="w-full md:w-auto">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search projects..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full md:w-80 bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-2 pl-10 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                  />
                  <svg
                    className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setFilterStatus('all')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium ${
                    filterStatus === 'all'
                      ? 'bg-brand-button text-white'
                      : 'bg-brand-bg/30 text-white/70 border border-brand-card-border hover:bg-brand-bg/50'
                  }`}
                >
                  All Projects
                </button>
                <button
                  onClick={() => setFilterStatus('pending')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium ${
                    filterStatus === 'pending'
                      ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                      : 'bg-brand-bg/30 text-white/70 border border-brand-card-border hover:bg-brand-bg/50'
                  }`}
                >
                  Pending
                </button>
                <button
                  onClick={() => setFilterStatus('active')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium ${
                    filterStatus === 'active'
                      ? 'bg-teal-500/20 text-teal-400 border border-teal-500/30'
                      : 'bg-brand-bg/30 text-white/70 border border-brand-card-border hover:bg-brand-bg/50'
                  }`}
                >
                  Active
                </button>
                <button
                  onClick={() => setFilterStatus('completed')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium ${
                    filterStatus === 'completed'
                      ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                      : 'bg-brand-bg/30 text-white/70 border border-brand-card-border hover:bg-brand-bg/50'
                  }`}
                >
                  Completed
                </button>
              </div>

              <div className="flex items-center space-x-2">
                <span className="text-white/70 text-sm">Sort by:</span>
                <select
                  value={sortOption}
                  onChange={(e) => setSortOption(e.target.value)}
                  className="bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                >
                  <option value="newest">Newest</option>
                  <option value="oldest">Oldest</option>
                  <option value="name">Name</option>
                  <option value="progress">Progress</option>
                </select>
              </div>
            </div>

            {/* Projects Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 stagger-children">
              {isLoading ? (
                <div className="col-span-full text-center py-12 animate-pulse">
                  <div className="inline-block w-12 h-12 border-4 border-brand-button border-t-transparent rounded-full animate-spin mb-4"></div>
                  <p className="text-white/60">Loading projects...</p>
                </div>
              ) : filteredProjects.length === 0 ? (
                <div className="col-span-full text-center py-12 animate-fadeIn">
                  <svg className="w-20 h-20 text-brand-chat/20 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <h3 className="text-xl font-bold text-white mb-2">No Projects Found</h3>
                  <p className="text-white/70 mb-4">
                    {filterStatus === 'all'
                      ? 'Create your first project to get started'
                      : `No ${filterStatus} projects found`}
                  </p>
                  <button
                    onClick={() => setShowNewProjectModal(true)}
                    className="px-6 py-2.5 bg-gradient-to-r from-brand-button to-brand-button-hover text-white rounded-xl font-semibold hover:from-brand-button-hover hover:to-brand-button transition-all shadow-lg shadow-brand-button/30"
                  >
                    Create Project
                  </button>
                </div>
              ) : filteredProjects.map((project, index) => (
                <div
                  key={project.id}
                  className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all hover:shadow-lg hover:shadow-brand-button/20 hover:-translate-y-0.5 animate-fadeInUp group"
                  style={{animationDelay: `${index * 0.1}s`}}
                >
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-bold text-white group-hover:text-brand-button transition-colors duration-300">{project.name}</h3>
                    <span className={`text-xs px-3 py-1 rounded-full font-semibold ${
                      project.status === 'completed' ? 'bg-green-500/20 text-green-400 border border-green-500/30' :
                      project.status === 'active' ? 'bg-brand-button/20 text-brand-button border border-brand-button/30' :
                      'bg-brand-chat/10 text-brand-chat/60 border border-brand-chat/20'
                    }`}>
                      {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
                    </span>
                  </div>
                  <p className="text-white/70 mb-4 group-hover:text-white/90 transition-colors duration-300">{project.description}</p>

                  <div className="mb-4">
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-white/60 font-medium">Progress</span>
                      <span className="text-white font-semibold">{project.progress}%</span>
                    </div>
                    <div className="w-full bg-brand-bg/50 rounded-full h-3 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-brand-button to-brand-button-hover h-3 rounded-full transition-all duration-500 shadow-md shadow-brand-button/30"
                        style={{ width: `${project.progress}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center text-sm">
                    <div className="flex items-center space-x-4">
                      <span className="text-white/60">{project.tasks.completed}/{project.tasks.total} tasks</span>
                      <span className="text-white/60">{project.members} members</span>
                    </div>
                    <span className="text-white/50">{new Date(project.dueDate).toLocaleDateString()}</span>
                  </div>

                  <div className="mt-4 pt-4 border-t border-brand-card-border/30 flex justify-between">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleUpdateProjectStatus(project.id, 'pending')}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                          project.status === 'pending'
                            ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                            : 'bg-brand-bg/30 text-white/70 border border-brand-card-border hover:bg-brand-bg/50'
                        }`}
                      >
                        Pending
                      </button>
                      <button
                        onClick={() => handleUpdateProjectStatus(project.id, 'active')}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                          project.status === 'active'
                            ? 'bg-teal-500/20 text-teal-400 border border-teal-500/30'
                            : 'bg-brand-bg/30 text-white/70 border border-brand-card-border hover:bg-brand-bg/50'
                        }`}
                      >
                        Active
                      </button>
                      <button
                        onClick={() => handleUpdateProjectStatus(project.id, 'completed')}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                          project.status === 'completed'
                            ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                            : 'bg-brand-bg/30 text-white/70 border border-brand-card-border hover:bg-brand-bg/50'
                        }`}
                      >
                        Completed
                      </button>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleDeleteProject(project.id)}
                        className="text-red-400 hover:text-red-300 font-semibold text-sm transition-colors"
                      >
                        Delete
                      </button>
                      <button
                        onClick={() => handleViewProjectDetails(project)}
                        className="text-brand-button hover:text-brand-button-hover font-semibold text-sm hover-scale transition-all duration-300 group-hover:translate-x-1 transform"
                      >
                        View Project →
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

      {/* New Project Modal */}
      {showNewProjectModal && (
        <div className="fixed inset-0 bg-brand-bg/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-brand-card-bg border border-brand-card-border rounded-3xl w-full max-w-md p-4 md:p-6 shadow-2xl shadow-brand-button/20 animate-scaleIn">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Create New Project</h2>
              <button
                onClick={() => setShowNewProjectModal(false)}
                className="w-10 h-10 rounded-full bg-brand-bg/50 hover:bg-brand-bg/70 flex items-center justify-center transition-colors border border-brand-card-border"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-white text-sm mb-2 font-medium">Project Name</label>
                <input
                  type="text"
                  value={newProject.name}
                  onChange={(e) => setNewProject({...newProject, name: e.target.value})}
                  className="w-full bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                  placeholder="Enter project name"
                />
              </div>
              <div>
                <label className="block text-white text-sm mb-2 font-medium">Description</label>
                <textarea
                  value={newProject.description}
                  onChange={(e) => setNewProject({...newProject, description: e.target.value})}
                  rows="3"
                  className="w-full bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                  placeholder="Describe your project"
                />
              </div>
              <div>
                <label className="block text-white text-sm mb-2 font-medium">Due Date (Optional)</label>
                <input
                  type="date"
                  value={newProject.dueDate}
                  onChange={(e) => setNewProject({...newProject, dueDate: e.target.value})}
                  className="w-full bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                />
              </div>
            </div>

            <div className="mt-6 flex justify-end space-x-3">
              <button
                onClick={() => setShowNewProjectModal(false)}
                className="px-6 py-2.5 bg-brand-bg/50 text-white rounded-xl font-semibold hover:bg-brand-bg/70 transition-colors border border-brand-card-border"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateProject}
                className="px-6 py-2.5 bg-gradient-to-r from-brand-button to-brand-button-hover text-white rounded-xl font-semibold hover:from-brand-button-hover hover:to-brand-button transition-all shadow-lg shadow-brand-button/30 hover-lift"
              >
                Create Project
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Project Details Modal */}
      {showProjectDetails && selectedProject && (
        <div className="fixed inset-0 bg-brand-bg/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-brand-card-bg border border-brand-card-border rounded-3xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 shadow-2xl shadow-brand-button/20 animate-scaleIn">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">{selectedProject.name}</h2>
              <button
                onClick={() => setShowProjectDetails(false)}
                className="w-10 h-10 rounded-full bg-brand-bg/50 hover:bg-brand-bg/70 flex items-center justify-center transition-colors border border-brand-card-border"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Description</h3>
                <p className="text-white/80">
                  {selectedProject.description || 'No description provided.'}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">Status</h3>
                  <span className={`inline-block px-4 py-2 rounded-full font-semibold ${
                    selectedProject.status === 'completed' ? 'bg-green-500/20 text-green-400 border border-green-500/30' :
                    selectedProject.status === 'active' ? 'bg-brand-button/20 text-brand-button border border-brand-button/30' :
                    'bg-brand-chat/10 text-brand-chat/60 border border-brand-chat/20'
                  }`}>
                    {selectedProject.status.charAt(0).toUpperCase() + selectedProject.status.slice(1)}
                  </span>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">Due Date</h3>
                  <p className="text-white/80">
                    {selectedProject.dueDate ? new Date(selectedProject.dueDate).toLocaleDateString() : 'No due date set'}
                  </p>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Progress</h3>
                <div className="mb-2">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-white/60 font-medium">Progress</span>
                    <span className="text-white font-semibold">{selectedProject.progress}%</span>
                  </div>
                  <div className="w-full bg-brand-bg/50 rounded-full h-4 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-brand-button to-brand-button-hover h-4 rounded-full transition-all duration-500 shadow-md shadow-brand-button/30"
                      style={{ width: `${selectedProject.progress}%` }}
                    ></div>
                  </div>
                </div>
                <div className="text-sm text-white/70 mt-1">
                  {selectedProject.tasks.completed} of {selectedProject.tasks.total} tasks completed
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">Members</h3>
                  <p className="text-white/80">{selectedProject.members} member(s)</p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">Created</h3>
                  <p className="text-white/80">
                    {new Date(selectedProject.created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-brand-card-border/30 flex justify-end">
              <button
                onClick={() => setShowProjectDetails(false)}
                className="px-6 py-2.5 bg-gradient-to-r from-brand-button to-brand-button-hover text-white rounded-xl font-semibold hover:from-brand-button-hover hover:to-brand-button transition-all shadow-lg shadow-brand-button/30 hover-lift"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

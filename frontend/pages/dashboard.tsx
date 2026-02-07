import Head from 'next/head'
import { useState, useEffect, useRef, FC, FormEvent, ChangeEvent } from 'react'
import ProtectedRoute from '@/components/ProtectedRoute'
import { useAuth } from '@/contexts/AuthContext'

interface Task {
  id: string
  title: string
  description?: string
  status: 'pending' | 'in_progress' | 'completed'
  priority?: 'low' | 'medium' | 'high'
  due_date?: string
  created_at: string
  updated_at: string
}

interface Message {
  id: number
  text: string
  sender: 'user' | 'bot'
  timestamp: string
  image?: string
  modality?: 'text' | 'image'
  metadata?: any
  tasksAffected?: string[]
  isError?: boolean
}

interface SystemLog {
  id: string
  status: string
  text: string
  color: 'cyan' | 'green' | 'gray'
}

const Dashboard: FC = () => {
  const { user } = useAuth()

  // User state
  const userId = user?.id || 'user_123'
  const userName = user?.email?.split('@')[0] || 'User'

  // Tasks state
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoadingTasks, setIsLoadingTasks] = useState<boolean>(true)

  // Chat state
  const [showChatModal, setShowChatModal] = useState<boolean>(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [conversationId, setConversationId] = useState<string | null>(null)

  // Image upload state
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Filter state
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [filterPriority, setFilterPriority] = useState<string>('all')
  const [searchTerm, setSearchTerm] = useState<string>('')

  // Edit state
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null)
  const [editingTask, setEditingTask] = useState<Partial<Task> | null>(null)

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  // Auto-scroll chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Fetch tasks on mount
  useEffect(() => {
    if (userId) {
      fetchTasks()
    }
  }, [userId])

  const fetchTasks = async () => {
    setIsLoadingTasks(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const tasksData = await response.json()
      setTasks(tasksData)
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
      setTasks([])
    } finally {
      setIsLoadingTasks(false)
    }
  }

  const handleImageSelect = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file')
        return
      }
      if (file.size > 10 * 1024 * 1024) {
        alert('Image must be less than 10MB')
        return
      }
      setSelectedImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const removeImage = () => {
    setSelectedImage(null)
    setImagePreview(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if ((!inputValue.trim() && !selectedImage) || isLoading) return

    const currentInput = inputValue
    const currentImagePreview = imagePreview
    const modality = selectedImage ? 'image' : 'text'

    const userMessage: Message = {
      id: Date.now(),
      text: inputValue || (selectedImage ? 'Uploaded an image' : ''),
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
      image: currentImagePreview || undefined,
      modality: modality
    }
    setMessages(prev => [...prev, userMessage])

    setInputValue('')
    setSelectedImage(null)
    setImagePreview(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
    setIsLoading(true)

    try {
      const response = await callBackendAPI(currentInput, currentImagePreview, modality)

      const botMessage: Message = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        metadata: response.metadata,
        tasksAffected: response.tasks_affected || []
      }
      setMessages(prev => [...prev, botMessage])

      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id)
      }

      if (response.tasks_affected && response.tasks_affected.length > 0) {
        await fetchTasks()
      }
    } catch (error) {
      console.error('API Error:', error)
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: error instanceof Error ? error.message : 'Sorry, I encountered an error. Please make sure the backend server is running.',
        sender: 'bot',
        isError: true,
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const callBackendAPI = async (message: string, imageData: string | null, modality: string) => {
    const metadata: any = {}
    if (imageData) {
      metadata.image_data = imageData
    }

    const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message || 'Process this image',
        modality: modality,
        conversation_id: conversationId,
        metadata: metadata
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    return await response.json()
  }

  // Delete task function
  const deleteTask = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      if (!response.ok) {
        throw new Error(`Failed to delete task: ${response.status}`)
      }

      // Remove the task from the local state
      setTasks(tasks.filter(task => task.id !== taskId))
    } catch (error) {
      console.error('Failed to delete task:', error)
      alert('Failed to delete task. Please try again.')
    }
  }

  // Start editing a task
  const startEditingTask = (task: Task) => {
    setEditingTaskId(task.id);
    setEditingTask({
      title: task.title,
      description: task.description,
      status: task.status,
      priority: task.priority, // Keep as is (undefined or valid priority)
      due_date: task.due_date
    });
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingTaskId(null);
    setEditingTask(null);
  };

  // Save edited task
  const saveEditedTask = async (taskId: string) => {
    if (!editingTask) return;

    try {
      // Prepare the data to send, handling empty priority
      const taskData = {
        ...editingTask,
        priority: editingTask.priority || undefined // Convert empty string to undefined
      };

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData)
      });

      if (!response.ok) {
        throw new Error(`Failed to update task: ${response.status}`);
      }

      // Update the task in the local state
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, ...taskData } as Task : task
      ));

      // Reset editing state
      setEditingTaskId(null);
      setEditingTask(null);
    } catch (error) {
      console.error('Failed to update task:', error);
      alert('Failed to update task. Please try again.');
    }
  };

  // Update task status
  const updateTaskStatus = async (taskId: string, newStatus: 'pending' | 'in_progress' | 'completed') => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
      });

      if (!response.ok) {
        throw new Error(`Failed to update task status: ${response.status}`);
      }

      // Update the task in the local state
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, status: newStatus } as Task : task
      ));
    } catch (error) {
      console.error('Failed to update task status:', error);
      alert('Failed to update task status. Please try again.');
    }
  };

  // Calculate statistics
  const totalTasks = tasks.length
  const pendingTasks = tasks.filter(t => t.status === 'pending').length
  const inProgressTasks = tasks.filter(t => t.status === 'in_progress').length
  const completedTasks = tasks.filter(t => t.status === 'completed').length
  const activeTasks = pendingTasks + inProgressTasks

  // Filter tasks based on status, priority, and search term
  const filteredTasks = tasks.filter(task => {
    const matchesStatus = filterStatus === 'all' || task.status === filterStatus
    const matchesPriority = filterPriority === 'all' ||
      (filterPriority === 'none' ? !task.priority : task.priority === filterPriority) // Handle 'none' option
    const matchesSearch = searchTerm === '' ||
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()))

    return matchesStatus && matchesPriority && matchesSearch
  })

  // Generate system logs from tasks
  const systemLogs: SystemLog[] = tasks.slice(-6).reverse().map(task => ({
    id: task.id,
    status: task.status.toUpperCase().replace('_', '_'),
    text: task.title,
    color: task.status === 'completed' ? 'green' : task.status === 'in_progress' ? 'cyan' : 'gray'
  }))

  const quickCommands = [
    "Add new task: Review code",
    "Show pending tasks",
    "Complete task #1",
    "List all my tasks"
  ]

  return (
    <ProtectedRoute>
      <Head>
        <title>Dashboard - TaskFlow</title>
        <meta name="description" content="TaskFlow Dashboard" />
      </Head>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden bg-brand-bg">
          {/* Header */}
          <div className="bg-brand-card-bg/80 backdrop-blur-sm px-4 py-3 md:px-8 md:py-6 border-b border-brand-card-border animate-fadeInDown">
            <h1 className='text-3xl font-bold text-white mb-1'>Welcome back, <span className='bg-gradient-to-r from-brand-button to-brand-button-hover bg-clip-text text-transparent'>{userName}</span></h1>
            <p className="text-white/70 text-sm">
              System operational. {activeTasks} active task{activeTasks !== 1 ? 's' : ''}. {pendingTasks} pending directive{pendingTasks !== 1 ? 's' : ''}.
            </p>
          </div>

          {/* Main Content */}
          <div className="flex-1 flex flex-col overflow-hidden">

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-4 py-3 md:px-8 md:py-6 animate-fadeIn">
          {/* New Project Button + AI Chat Button */}
          <div className="mb-6 flex items-center space-x-3 animate-fadeInUp">
            {/* <button
              onClick={() => {
                setInputValue('Create a new project')
                setShowChatModal(true)
              }}
              className="px-6 py-2.5 bg-brand-button text-white rounded-xl font-semibold hover:bg-brand-button-hover transition-all duration-300 inline-flex items-center space-x-2 shadow-lg shadow-brand-button/30 hover:shadow-xl hover:shadow-brand-button/40 hover:-translate-y-0.5 transform"
            >
              <span>New Project</span>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </button> */}
            {/* <button
              onClick={() => setShowChatModal(true)}
              className="px-6 py-2.5 bg-white border-2 border-brand-chat text-brand-chat rounded-xl font-semibold hover:bg-brand-chat hover:text-white transition-all duration-300 inline-flex items-center space-x-2 hover:-translate-y-0.5 transform"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
             <span>AI Assistant</span>
            </button>  */}
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8 stagger-children">
            {/* Total Tasks */}
            <div className="bg-gradient-to-br from-brand-card-bg/50 to-brand-bg/30 backdrop-blur-sm border border-brand-card-border rounded-xl p-4 md:p-6 transition-all duration-500 hover:shadow-xl hover:shadow-brand-button/30 hover:-translate-y-1 hover:border-brand-button/70 animate-fadeInUp cursor-pointer group">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-white/60 text-sm mb-2 uppercase tracking-wider font-semibold">Total Tasks</p>
                  <p className="text-white text-5xl font-bold group-hover:text-brand-button transition-colors duration-300">{totalTasks}</p>
                </div>
                <div className="w-12 h-12 bg-gradient-to-br from-brand-button/30 to-brand-button/10 rounded-xl flex items-center justify-center group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                  <svg className="w-7 h-7 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
              </div>
              <div className="mt-4 w-full bg-brand-bg/50 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-brand-button to-brand-button-hover h-2 rounded-full animate-progress"
                  style={{ width: `${totalTasks > 0 ? Math.min(100, (totalTasks / (totalTasks + 10)) * 100) : 0}%`, animation: 'progressAnimation 1.5s ease-out forwards' }}
                ></div>
              </div>
            </div>

            {/* Active Tasks */}
            <div className="bg-gradient-to-br from-brand-card-bg/50 to-brand-bg/30 backdrop-blur-sm border border-brand-card-border rounded-xl p-4 md:p-6 transition-all duration-500 hover:shadow-xl hover:shadow-brand-button/30 hover:-translate-y-1 hover:border-brand-button/70 animate-fadeInUp animate-delay-100 cursor-pointer group">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-white/60 text-sm mb-2 uppercase tracking-wider font-semibold">Active</p>
                  <p className="text-white text-5xl font-bold group-hover:text-brand-button transition-colors duration-300">{activeTasks}</p>
                </div>
                <div className="w-12 h-12 bg-gradient-to-br from-brand-button/30 to-brand-button/10 rounded-xl flex items-center justify-center group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                  <svg className="w-7 h-7 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
              <div className="mt-4 w-full bg-brand-bg/50 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-brand-button to-brand-button-hover h-2 rounded-full animate-progress"
                  style={{ width: `${activeTasks > 0 ? Math.min(100, (activeTasks / (activeTasks + 10)) * 100) : 0}%`, animation: 'progressAnimation 1.5s ease-out forwards' }}
                ></div>
              </div>
            </div>

            {/* Pending */}
            <div className="bg-gradient-to-br from-brand-card-bg/50 to-brand-bg/30 backdrop-blur-sm border border-brand-card-border rounded-xl p-4 md:p-6 transition-all duration-500 hover:shadow-xl hover:shadow-brand-button/30 hover:-translate-y-1 hover:border-brand-button/70 animate-fadeInUp animate-delay-200 cursor-pointer group">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-white/60 text-sm mb-2 uppercase tracking-wider font-semibold">Pending</p>
                  <p className="text-white text-5xl font-bold group-hover:text-brand-button transition-colors duration-300">{pendingTasks}</p>
                </div>
                <div className="w-12 h-12 bg-gradient-to-br from-brand-button/30 to-brand-button/10 rounded-xl flex items-center justify-center group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                  <svg className="w-7 h-7 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div className="mt-4 w-full bg-brand-bg/50 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-brand-button to-brand-button-hover h-2 rounded-full animate-progress"
                  style={{ width: `${pendingTasks > 0 ? Math.min(100, (pendingTasks / (pendingTasks + 10)) * 100) : 0}%`, animation: 'progressAnimation 1.5s ease-out forwards' }}
                ></div>
              </div>
            </div>

            {/* Completed */}
            <div className="bg-gradient-to-br from-brand-card-bg/50 to-brand-bg/30 backdrop-blur-sm border border-brand-card-border rounded-xl p-4 md:p-6 transition-all duration-500 hover:shadow-xl hover:shadow-brand-button/30 hover:-translate-y-1 hover:border-brand-button/70 animate-fadeInUp animate-delay-300 cursor-pointer group">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-white/60 text-sm mb-2 uppercase tracking-wider font-semibold">Completed</p>
                  <p className="text-white text-5xl font-bold group-hover:text-brand-button transition-colors duration-300">{completedTasks}</p>
                </div>
                <div className="w-12 h-12 bg-gradient-to-br from-brand-button/30 to-brand-button/10 rounded-xl flex items-center justify-center group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                  <svg className="w-7 h-7 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div className="mt-4 w-full bg-brand-bg/50 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-brand-button to-brand-button-hover h-2 rounded-full animate-progress"
                  style={{ width: `${completedTasks > 0 ? Math.min(100, (completedTasks / (completedTasks + 10)) * 100) : 0}%`, animation: 'progressAnimation 1.5s ease-out forwards' }}
                ></div>
              </div>
            </div>
          </div>

          {/* Tasks List and System Logs */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fadeInUp">
            {/* Tasks List - Takes 2 columns */}
            <div className='lg:col-span-2 bg-brand-card-bg border border-brand-card-border rounded-xl p-4 md:p-6 transition-all duration-300 shadow-sm shadow-brand-chat/5'>
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-white text-xl font-bold">Tasks</h3>
                  <p className="text-white/60 text-sm">Manage your tasks</p>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="text"
                    placeholder="Search tasks..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className='bg-brand-bg border border-brand-card-border text-white rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200 w-48'
                  />
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className='bg-brand-bg border border-brand-card-border text-white rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200'
                  >
                    <option value="all">All Statuses</option>
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                  </select>
                  <select
                    value={filterPriority}
                    onChange={(e) => setFilterPriority(e.target.value)}
                    className='bg-brand-bg border border-brand-card-border text-white rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200'
                  >
                    <option value="all">All Priorities</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="none">No Priority</option>
                  </select>
                  <button
                    onClick={() => {
                      // Mark all pending tasks as completed
                      const pendingTasks = tasks.filter(t => t.status === 'pending');
                      if (pendingTasks.length > 0 && window.confirm(`Mark ${pendingTasks.length} pending tasks as completed?`)) {
                        pendingTasks.forEach(task => {
                          updateTaskStatus(task.id, 'completed');
                        });
                      }
                    }}
                    className="text-brand-button hover:text-brand-button-hover font-semibold text-sm flex items-center space-x-1 transition-colors duration-200"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span>BULK COMPLETE</span>
                  </button>
                  <button
                    onClick={() => {
                      // Clear all filters
                      setFilterStatus('all');
                      setFilterPriority('all');
                      setSearchTerm('');
                    }}
                    className="text-brand-button hover:text-brand-button-hover font-semibold text-sm flex items-center space-x-1 transition-colors duration-200"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>CLEAR FILTERS</span>
                  </button>
                  <button
                    onClick={() => setShowChatModal(true)}
                    className="text-brand-button hover:text-brand-button-hover font-semibold text-sm flex items-center space-x-1 transition-colors duration-200"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    <span>ADD TASK</span>
                  </button>
                </div>
              </div>

              {/* Task Items */}
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {isLoadingTasks ? (
                  <div className="text-center py-8">
                    <div className="inline-block w-8 h-8 border-4 border-brand-button border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-white/60 mt-2">Loading tasks...</p>
                  </div>
                ) : filteredTasks.length === 0 ? (
                  <div className="text-center py-8">
                    <svg className="w-16 h-16 text-brand-chat/20 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    <p className="text-white/60">No tasks found</p>
                    <button
                      onClick={() => {
                        setInputValue('Add a new task')
                        setShowChatModal(true)
                      }}
                      className="mt-3 text-brand-button hover:text-brand-button-hover text-sm transition-colors duration-200"
                    >
                      Create your first task
                    </button>
                  </div>
                ) : (
                  filteredTasks.map((task) => {
                    // Check if this task is currently being edited
                    const isEditing = editingTaskId === task.id;

                    return (
                      <div
                        key={task.id}
                        className='bg-brand-bg border border-brand-card-border rounded-xl p-4 hover:border-brand-button/30 hover:shadow-md transition-all duration-300 group shadow-sm shadow-brand-chat/5'
                      >
                        {isEditing ? (
                          // Editing view
                          <div className="space-y-3">
                            <input
                              type="text"
                              value={editingTask?.title || ''}
                              onChange={(e) => setEditingTask({...editingTask!, title: e.target.value})}
                              className="w-full bg-brand-bg border-2 border-brand-card-border rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200 font-semibold"
                            />
                            <textarea
                              value={editingTask?.description || ''}
                              onChange={(e) => setEditingTask({...editingTask!, description: e.target.value})}
                              className="w-full bg-brand-bg border-2 border-brand-card-border rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200 text-sm"
                              rows={2}
                              placeholder="Task description..."
                            />
                            <div className="flex items-center space-x-3">
                              <select
                                value={editingTask?.status || 'pending'}
                                onChange={(e) => setEditingTask({...editingTask!, status: e.target.value as any})}
                                className="bg-brand-bg border-2 border-brand-card-border text-white rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200"
                              >
                                <option value="pending">Pending</option>
                                <option value="in_progress">In Progress</option>
                                <option value="completed">Completed</option>
                              </select>
                              <select
                                value={editingTask?.priority || ''}
                                onChange={(e) => {
                                  const value = e.target.value || undefined;
                                  // Only allow valid priority values
                                  const priority = value && ['low', 'medium', 'high'].includes(value) ? value as 'low' | 'medium' | 'high' : undefined;
                                  setEditingTask({...editingTask!, priority});
                                }}
                                className="bg-brand-bg border-2 border-brand-card-border text-white rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200"
                              >
                                <option value="">No Priority</option>
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                              </select>
                              <input
                                type="date"
                                value={editingTask?.due_date || ''}
                                onChange={(e) => setEditingTask({...editingTask!, due_date: e.target.value || undefined})}
                                className="bg-brand-bg border-2 border-brand-card-border text-white rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200"
                              />
                            </div>
                            <div className="flex justify-end space-x-2">
                              <button
                                onClick={cancelEditing}
                                className="px-3 py-1 bg-gray-700 text-white rounded-lg text-sm hover:bg-gray-600 transition-colors duration-200"
                              >
                                Cancel
                              </button>
                              <button
                                onClick={() => saveEditedTask(task.id)}
                                className="px-3 py-1 bg-brand-button text-white rounded-lg text-sm hover:bg-brand-button-hover transition-colors duration-200"
                              >
                                Save
                              </button>
                            </div>
                          </div>
                        ) : (
                          // Normal view
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center space-x-3 mb-2">
                                <h4 className="text-white font-semibold">{task.title}</h4>
                                <button
                                  onClick={() => {
                                    // Cycle through statuses: pending -> in_progress -> completed -> pending
                                    let newStatus: 'pending' | 'in_progress' | 'completed' = 'pending';
                                    if (task.status === 'pending') newStatus = 'in_progress';
                                    else if (task.status === 'in_progress') newStatus = 'completed';
                                    else if (task.status === 'completed') newStatus = 'pending';
                                    updateTaskStatus(task.id, newStatus);
                                  }}
                                  className={`text-xs px-2 py-1 rounded-full font-medium cursor-pointer hover:opacity-80 transition-opacity ${
                                    task.status === 'completed' ? 'bg-green-900/30 text-green-400' :
                                    task.status === 'in_progress' ? 'bg-brand-button/20 text-brand-button' :
                                    'bg-brand-chat/30 text-brand-button'
                                  }`}
                                >
                                  {task.status.replace('_', ' ')}
                                </button>
                                {task.priority && (
                                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                                    task.priority === 'high' ? 'bg-red-900/30 text-red-400' :
                                    task.priority === 'medium' ? 'bg-yellow-900/30 text-yellow-400' :
                                    'bg-blue-900/30 text-blue-400'
                                  }`}>
                                    {task.priority}
                                  </span>
                                )}
                              </div>
                              {task.description && (
                                <p className="text-white/70 text-sm mb-2">{task.description}</p>
                              )}
                              <div className="flex items-center space-x-4 text-xs text-white/50">
                                {task.due_date && (
                                  <span>Due: {new Date(task.due_date).toLocaleDateString()}</span>
                                )}
                                <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                              </div>
                            </div>
                            <div className="flex space-x-2">
                              <button
                                onClick={() => startEditingTask(task)}
                                className="opacity-0 group-hover:opacity-100 transition-all duration-200 text-white/40 hover:text-brand-button hover:scale-110 transform"
                              >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                              </button>
                              <button
                                onClick={() => deleteTask(task.id)}
                                className="opacity-0 group-hover:opacity-100 transition-all duration-200 text-white/40 hover:text-red-400 hover:scale-110 transform"
                              >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })
                )}
              </div>
            </div>

            {/* System Logs - Takes 1 column */}
            <div className='bg-brand-card-bg border border-brand-card-border rounded-xl p-4 md:p-6 transition-all duration-300 shadow-sm shadow-brand-chat/5'>
              <h3 className="text-white text-lg font-bold mb-1">System Logs</h3>
              <p className="text-white/50 text-xs mb-4 uppercase tracking-wider font-semibold">Live Event Stream</p>

              <div className="space-y-2">
                {systemLogs.map((log) => (
                  <div key={log.id} className="flex items-center space-x-2 text-sm">
                    <span className="text-brand-button">•</span>
                    <span className={`font-mono text-xs font-semibold ${
                      log.color === 'cyan' ? 'text-brand-button' :
                      log.color === 'green' ? 'text-green-400' :
                      'text-white/60'
                    }`}>
                      [{log.status}]
                    </span>
                    <span className="text-white truncate">{log.text}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* AI Chat Modal */}
      {showChatModal && (
        <div className="fixed inset-0 bg-brand-chat/70 backdrop-blur-sm z-50 flex items-center justify-center p-0 md:p-4 animate-fadeIn">
          <div className="bg-brand-card-bg border-2 border-brand-card-border md:rounded-3xl w-full h-full md:h-auto md:max-w-2xl lg:max-w-4xl md:max-h-[85vh] flex flex-col shadow-2xl shadow-brand-chat/20 animate-scaleIn">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-4 md:p-6 border-b border-brand-card-border">
              <div>
                <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
                  <span className="bg-gradient-to-r from-brand-button to-brand-button-hover bg-clip-text text-transparent">TaskFlow AI Assistant</span>
                  <span className="inline-flex items-center px-2 py-1 bg-brand-button/20 border border-brand-button/50 rounded-full text-xs text-brand-button font-semibold">
                    Powered by Claude
                  </span>
                </h2>
                <p className="text-sm text-white/70">Natural language task management</p>
              </div>
              <button
                onClick={() => setShowChatModal(false)}
                className="w-10 h-10 rounded-full bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border hover:bg-brand-button/20 flex items-center justify-center transition-all duration-300 hover:scale-110 transform hover-lift"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 bg-brand-bg">
              {messages.length === 0 ? (
                <div className="text-center py-12">
                  <div className="w-20 h-20 bg-gradient-to-br from-brand-button to-brand-button-hover rounded-3xl mx-auto mb-4 flex items-center justify-center animate-pulse shadow-lg shadow-brand-button/30">
                    <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">Start Managing Tasks</h3>
                  <p className="text-white/70 mb-6">Use natural language to create, list, update, or complete tasks</p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 md:gap-3 max-w-2xl mx-auto">
                    {quickCommands.map((text, i) => (
                      <button
                        key={i}
                        onClick={() => setInputValue(text)}
                        className="px-4 py-3 bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border text-white rounded-xl hover:border-brand-button hover:shadow-lg hover:shadow-brand-button/20 transition-all duration-300 text-sm font-medium text-left hover:-translate-y-0.5 transform hover-lift"
                      >
                        {text}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <>
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fadeInUp`}
                    >
                      <div
                        className={`max-w-lg rounded-2xl px-6 py-4 transition-all duration-300 ${
                          msg.sender === 'user'
                            ? 'bg-gradient-to-br from-brand-button to-brand-button-hover text-white shadow-lg shadow-brand-button/30 hover:shadow-xl hover:shadow-brand-button/40'
                            : msg.isError
                              ? 'bg-red-900/30 text-red-400 border-2 border-red-700'
                              : 'bg-brand-card-bg/70 backdrop-blur-sm border border-brand-card-border/50 text-white shadow-lg shadow-brand-chat/10 hover:shadow-xl hover:shadow-brand-chat/20'
                        }`}
                      >
                        {msg.image && (
                          <img src={msg.image} alt="Uploaded" className="rounded-xl mb-3 max-h-48 border border-brand-button/30" />
                        )}
                        <p className="whitespace-pre-wrap">{msg.text}</p>
                        {msg.tasksAffected && msg.tasksAffected.length > 0 && (
                          <div className="mt-2 text-xs opacity-75">
                            Tasks affected: {msg.tasksAffected.join(', ')}
                          </div>
                        )}
                        <p className={`text-xs mt-2 ${msg.sender === 'user' ? 'text-white/80' : 'text-white/50'}`}>
                          {msg.timestamp}
                        </p>
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start animate-fadeInUp">
                      <div className="bg-brand-card-bg/70 backdrop-blur-sm border border-brand-card-border/50 rounded-2xl px-6 py-4 shadow-lg shadow-brand-button/10">
                        <div className="flex space-x-2">
                          <div className="w-2 h-2 bg-brand-button rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-brand-button rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                          <div className="w-2 h-2 bg-brand-button rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>

            {/* Input */}
            <div className="p-4 md:p-6 border-t-2 border-brand-card-border">
              {imagePreview && (
                <div className="mb-4 relative inline-block animate-fadeIn">
                  <img src={imagePreview} alt="Preview" className="rounded-xl max-h-32 border-2 border-brand-button/30 shadow-lg shadow-brand-button/20" />
                  <button
                    onClick={removeImage}
                    className="absolute -top-2 -right-2 w-7 h-7 bg-red-500/80 backdrop-blur-sm text-white rounded-full hover:bg-red-600/80 font-bold transition-all duration-300 hover:scale-110 transform hover-lift"
                  >
                    ×
                  </button>
                </div>
              )}
              <form onSubmit={handleSubmit} className="flex space-x-3">
                <input
                  type="file"
                  ref={fileInputRef}
                  accept="image/*"
                  onChange={handleImageSelect}
                  className="hidden"
                />
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                  className="w-12 h-12 bg-brand-bg/50 backdrop-blur-sm border-2 border-brand-card-border rounded-xl hover:border-brand-button hover:bg-brand-button/10 flex items-center justify-center transition-all duration-300 hover:scale-105 transform hover-lift"
                >
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </button>
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type a command... (e.g., 'Add task: Review PR')"
                  className="flex-1 border-2 border-brand-card-border bg-brand-bg/50 backdrop-blur-sm rounded-xl px-6 py-3 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-brand-button transition-all duration-200"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={isLoading || (!inputValue.trim() && !selectedImage)}
                  className="px-8 py-3 bg-gradient-to-r from-brand-button to-brand-button-hover text-white rounded-xl hover:from-brand-button-hover hover:to-brand-button disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-all duration-300 flex items-center space-x-2 shadow-lg shadow-brand-button/30 hover:shadow-xl hover:shadow-brand-button/40 hover:-translate-y-0.5 transform hover-lift"
                >
                  <span>Send</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                  </svg>
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
      </div>
    </ProtectedRoute>
  )
}

export default Dashboard

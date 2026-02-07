import Head from 'next/head'
import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'

export default function Analytics() {
  const { user } = useAuth()
  const userId = user?.id || 'user_123'
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const [timeRange, setTimeRange] = useState('7d')
  const [analytics, setAnalytics] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  // Fetch analytics on mount
  useEffect(() => {
    if (userId) {
      fetchAnalytics()
    }
  }, [userId, timeRange])

  const fetchAnalytics = async () => {
    setIsLoading(true)
    try {
      const days = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90
      const response = await fetch(`${API_BASE_URL}/api/${userId}/analytics?days=${days}`)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const analyticsData = await response.json()
      setAnalytics(analyticsData)
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
      // Set default empty data
      setAnalytics({
        task_stats: {
          total_tasks: 0,
          completed_tasks: 0,
          pending_tasks: 0,
          in_progress_tasks: 0,
          productivity: 0
        },
        project_stats: {
          total_projects: 0,
          completed_projects: 0,
          active_projects: 0,
          pending_projects: 0
        },
        daily_tasks: [],
        project_progress: []
      })
    } finally {
      setIsLoading(false)
    }
  }

  // Extract data from analytics or use defaults
  const taskData = analytics?.daily_tasks || []
  const projectData = analytics?.project_progress || []
  const stats = analytics ? {
    totalTasks: analytics.task_stats.total_tasks,
    completedTasks: analytics.task_stats.completed_tasks,
    pendingTasks: analytics.task_stats.pending_tasks,
    completedProjects: analytics.project_stats.completed_projects,
    totalProjects: analytics.project_stats.total_projects,
    productivity: analytics.task_stats.productivity
  } : {
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0,
    completedProjects: 0,
    totalProjects: 0,
    productivity: 0
  }

  return (
    <>
      <Head>
        <title>Analytics - TaskFlow</title>
        <meta name="description" content="TaskFlow Analytics Dashboard" />
      </Head>

      {/* Header */}
      <div className="bg-brand-card-bg/80 backdrop-blur-sm border-b border-brand-card-border px-4 py-3 md:px-8 md:py-6 animate-fadeInDown">
        <h1 className="text-3xl font-bold text-white mb-1">
          <span className="bg-gradient-to-r from-brand-button to-brand-button-hover bg-clip-text text-transparent">Analytics</span>
        </h1>
        <p className="text-white/70 text-sm">Track your productivity and task performance</p>
      </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-4 py-3 md:px-8 md:py-6 animate-fadeIn">
          <div className="max-w-7xl mx-auto">
            {/* Time Range Selector */}
            <div className="flex justify-end mb-6 animate-fadeInDown animate-delay-100">
              <div className="inline-flex rounded-xl border border-brand-card-border bg-brand-bg p-1 shadow-md">
                {['7d', '30d', '90d'].map((range) => (
                  <button
                    key={range}
                    onClick={() => setTimeRange(range)}
                    className={`px-4 py-2 text-sm font-semibold rounded-lg transition-all ${
                      timeRange === range
                        ? 'bg-gradient-to-r from-brand-button to-brand-button-hover text-white shadow-lg shadow-brand-button/30'
                        : 'text-white/70 hover:text-brand-button hover:bg-brand-card-bg/50'
                    }`}
                  >
                    {range}
                  </button>
                ))}
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 stagger-children">
              {/* Total Tasks */}
              <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all hover:shadow-lg hover:shadow-brand-button/20 hover:border-brand-button/50 animate-fadeInUp">
                <p className="text-white/60 text-sm mb-2 uppercase tracking-wider font-semibold">Total Tasks</p>
                <div className="flex items-center justify-between">
                  <p className="text-white text-4xl font-bold">{stats.totalTasks}</p>
                  <div className="w-12 h-12 bg-brand-button/20 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Completed Tasks */}
              <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all hover:shadow-lg hover:shadow-green-500/20 hover:border-green-500/50 animate-fadeInUp animate-delay-100">
                <p className="text-white/60 text-sm mb-2 uppercase tracking-wider font-semibold">Completed</p>
                <div className="flex items-center justify-between">
                  <p className="text-white text-4xl font-bold">{stats.completedTasks}</p>
                  <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Pending Tasks */}
              <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all hover:shadow-lg hover:shadow-yellow-500/20 hover:border-yellow-500/50 animate-fadeInUp animate-delay-200">
                <p className="text-white/60 text-sm mb-2 uppercase tracking-wider font-semibold">Pending</p>
                <div className="flex items-center justify-between">
                  <p className="text-white text-4xl font-bold">{stats.pendingTasks}</p>
                  <div className="w-12 h-12 bg-yellow-500/20 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Productivity */}
              <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all hover:shadow-lg hover:shadow-brand-button/20 hover:border-brand-button/50 animate-fadeInUp animate-delay-300">
                <p className="text-white/60 text-sm mb-2 uppercase tracking-wider font-semibold">Productivity</p>
                <div className="flex items-center justify-between">
                  <p className="text-white text-4xl font-bold">{stats.productivity}%</p>
                  <div className="w-12 h-12 bg-brand-button/20 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            {/* Charts and Data */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8 animate-fadeInUp animate-delay-400">
              {/* Task Completion Chart */}
              <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all">
                <h3 className="text-white text-lg font-bold mb-4">Task Completion</h3>
                <div className="h-64 flex items-end space-x-2">
                  {taskData.map((day, index) => (
                    <div key={index} className="flex flex-col items-center flex-1 animate-fadeInUp" style={{animationDelay: `${index * 0.1}s`}}>
                      <div className="flex items-end justify-center space-x-1 w-full h-40">
                        <div
                          className="w-3/5 bg-gradient-to-t from-green-500 to-green-400 rounded-t hover:shadow-lg hover:shadow-green-500/30 transition-all cursor-pointer"
                          style={{ height: `${(day.completed / 15) * 100}%` }}
                        ></div>
                        <div
                          className="w-3/5 bg-gradient-to-t from-slate-500 to-slate-400 rounded-t hover:shadow-lg hover:shadow-slate-500/30 transition-all cursor-pointer"
                          style={{ height: `${(day.pending / 15) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-white/60 text-xs mt-2 font-medium">{day.day}</span>
                    </div>
                  ))}
                </div>
                <div className="flex justify-center space-x-6 mt-4">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-gradient-to-r from-green-500 to-green-400 rounded mr-2"></div>
                    <span className="text-white/70 text-xs font-medium">Completed</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-gradient-to-r from-slate-500 to-slate-400 rounded mr-2"></div>
                    <span className="text-white/70 text-xs font-medium">Pending</span>
                  </div>
                </div>
              </div>

              {/* Project Progress */}
              <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all">
                <h3 className="text-white text-lg font-bold mb-4">Project Progress</h3>
                <div className="space-y-5">
                  {projectData.map((project, index) => (
                    <div key={index} className="animate-fadeInLeft" style={{animationDelay: `${index * 0.1}s`}}>
                      <div className="flex justify-between mb-1">
                        <span className="text-white text-sm font-semibold">{project.name}</span>
                        <span className="text-white/70 text-sm font-semibold">{project.progress}%</span>
                      </div>
                      <div className="w-full bg-brand-bg/50 rounded-full h-3 overflow-hidden">
                        <div
                          className="h-3 rounded-full bg-gradient-to-r from-brand-button to-brand-button-hover transition-all duration-500 shadow-md shadow-brand-button/30"
                          style={{ width: `${project.progress}%` }}
                        ></div>
                      </div>
                      <div className="flex justify-between mt-1">
                        <span className="text-white/50 text-xs">{project.tasks.completed} completed</span>
                        <span className="text-white/50 text-xs">{project.tasks.total} total</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all animate-fadeInUp animate-delay-500">
              <h3 className="text-white text-lg font-bold mb-4">Recent Activity</h3>
              <div className="space-y-4">
                {[
                  { action: 'Completed task', item: 'Review API documentation', time: '2 hours ago', type: 'completed' },
                  { action: 'Created project', item: 'Database Migration', time: '5 hours ago', type: 'created' },
                  { action: 'Updated task', item: 'Fix authentication bug', time: '1 day ago', type: 'updated' },
                  { action: 'Added comment', item: 'UI Redesign', time: '1 day ago', type: 'comment' },
                  { action: 'Completed task', item: 'Prepare presentation', time: '2 days ago', type: 'completed' }
                ].map((activity, index) => (
                  <div key={index} className="flex items-start border-b border-brand-card-border/30 pb-4 last:border-0 last:pb-0 hover:bg-brand-button/5 p-2 rounded-xl transition-all animate-fadeInLeft" style={{animationDelay: `${index * 0.1}s`}}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shadow-md ${
                      activity.type === 'completed' ? 'bg-green-500/20' :
                      activity.type === 'created' ? 'bg-brand-button/20' :
                      activity.type === 'updated' ? 'bg-yellow-500/20' :
                      'bg-slate-500/20'
                    }`}>
                      {activity.type === 'completed' ? (
                        <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      ) : activity.type === 'created' ? (
                        <svg className="w-4 h-4 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                      ) : activity.type === 'updated' ? (
                        <svg className="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      ) : (
                        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                        </svg>
                      )}
                    </div>
                    <div className="ml-4 flex-1">
                      <p className="text-white">
                        <span className="font-semibold">{activity.action}</span> {activity.item}
                      </p>
                      <p className="text-white/60 text-sm">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
    </>
  )
}

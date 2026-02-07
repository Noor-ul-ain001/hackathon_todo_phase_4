import Head from 'next/head'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'

export default function Settings() {
  const { user, logout } = useAuth()
  const router = useRouter()
  const userId = user?.id || 'user_123'
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const [activeTab, setActiveTab] = useState('account')
  const [userData, setUserData] = useState(null)
  const [settings, setSettings] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState(null) // null, 'success', 'error'
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })

  // Fetch settings on mount
  useEffect(() => {
    if (userId) {
      fetchProfileAndSettings()
    }
  }, [userId])

  const fetchProfileAndSettings = async () => {
    setIsLoading(true)
    try {
      // Fetch profile
      const profileResponse = await fetch(`${API_BASE_URL}/api/${userId}/profile`)
      const profileData = await profileResponse.json()

      // Fetch settings
      const settingsResponse = await fetch(`${API_BASE_URL}/api/${userId}/settings`)
      const settingsData = await settingsResponse.json()

      setUserData({
        name: profileData.name,
        email: profileData.email,
        avatar: profileData.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(profileData.name || 'User')}&background=14b8a6&color=fff&bold=true`
      })
      setSettings({
        ...settingsData,
        theme: settingsData.theme || 'light',
        language: settingsData.language || 'en',
        timezone: settingsData.timezone || 'UTC',
        dateFormat: settingsData.dateFormat || 'MM/DD/YYYY',
        timeFormat: settingsData.timeFormat || '12h',
        weeklyGoal: settingsData.weeklyGoal || 10,
        taskReminder: settingsData.taskReminder || true,
        taskReminderTime: settingsData.taskReminderTime || '09:00',
        autoSync: settingsData.autoSync || true,
        dataExport: settingsData.dataExport || false
      })
    } catch (error) {
      console.error('Failed to fetch settings:', error)
      setUserData({
        name: user?.email?.split('@')[0] || 'User',
        email: user?.email || 'user@example.com',
        avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(user?.email?.split('@')[0] || 'User')}&background=14b8a6&color=fff&bold=true`
      })
      setSettings({
        notifications: { email: true, push: true, sms: false },
        theme: 'light',
        language: 'en',
        timezone: 'UTC',
        dateFormat: 'MM/DD/YYYY',
        timeFormat: '12h',
        weeklyGoal: 10,
        taskReminder: true,
        taskReminderTime: '09:00',
        autoSync: true,
        dataExport: false
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.')
      if (parent === 'notifications') {
        setSettings(prev => ({
          ...prev,
          notifications: {
            ...prev.notifications,
            [child]: value
          }
        }))
      }
    } else if (field === 'name' || field === 'email') {
      setUserData(prev => ({
        ...prev,
        [field]: value
      }))
    } else {
      setSettings(prev => ({
        ...prev,
        [field]: value
      }))
    }
  }

  const handlePasswordChange = (field, value) => {
    setPasswordData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSave = async () => {
    setIsSaving(true)
    setSaveStatus(null)
    
    try {
      if (activeTab === 'account') {
        // Update profile
        const response = await fetch(`${API_BASE_URL}/api/${userId}/profile`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: userData.name,
            email: userData.email
          })
        })

        if (!response.ok) throw new Error('Failed to update profile')
      } else if (activeTab === 'security' && passwordData.newPassword) {
        // Update password
        if (passwordData.newPassword !== passwordData.confirmPassword) {
          throw new Error('New passwords do not match')
        }
        
        const response = await fetch(`${API_BASE_URL}/api/${userId}/password`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            currentPassword: passwordData.currentPassword,
            newPassword: passwordData.newPassword
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.message || 'Failed to update password')
        }
        
        // Reset password fields after successful update
        setPasswordData({
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        })
      } else {
        // Update settings
        const response = await fetch(`${API_BASE_URL}/api/${userId}/settings`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(settings)
        })

        if (!response.ok) throw new Error('Failed to update settings')
      }

      setSaveStatus('success')
      setTimeout(() => setSaveStatus(null), 3000)
    } catch (error) {
      console.error('Failed to save settings:', error)
      setSaveStatus('error')
      setTimeout(() => setSaveStatus(null), 3000)
    } finally {
      setIsSaving(false)
    }
  }

  const handleDataExport = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/export`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        }
      })

      if (!response.ok) throw new Error('Failed to export data')

      // Create a blob from the response and trigger download
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `taskflow-data-${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Failed to export data:', error)
      alert('Failed to export data. Please try again.')
    }
  }

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/account`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        }
      })

      if (!response.ok) throw new Error('Failed to delete account')

      alert('Account deleted successfully. You will be logged out.')
      // In a real app, you would log the user out here
    } catch (error) {
      console.error('Failed to delete account:', error)
      alert('Failed to delete account. Please try again.')
    }
  }

  return (
    <>
      <Head>
        <title>Settings - TaskFlow</title>
        <meta name="description" content="TaskFlow Settings" />
      </Head>

      {/* Header */}
      <div className="bg-gradient-to-br from-black via-[#1a1a1a] to-[#330033] border-b border-[#C459E0] px-4 py-3 md:px-8 md:py-6 animate-fadeInDown">
        <h1 className="text-3xl font-bold text-white mb-1">
          <span className="bg-gradient-to-r from-[#C459E0] to-[#9c27b0] bg-clip-text text-transparent">Settings</span>
        </h1>
        <p className="text-white/70 text-sm">Manage your account preferences</p>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-4 py-3 md:px-8 md:py-6 animate-fadeIn">
        <div className="max-w-4xl mx-auto">
          {/* Settings Tabs */}
          <div className="flex flex-wrap space-x-0 space-y-2 md:space-x-8 md:space-y-0 mb-8 border-b border-[#C459E0]">
            {['account', 'notifications', 'appearance', 'productivity', 'security', 'data'].map((tab, index) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`pb-4 px-1 capitalize font-semibold transition-all animate-fadeInDown ${
                  activeTab === tab
                    ? 'text-[#C459E0] border-b-2 border-[#C459E0]'
                    : 'text-white/70 hover:text-[#C459E0]'
                }`}
                style={{animationDelay: `${index * 0.1}s`}}
              >
                {tab === 'productivity' ? 'Productivity' : tab}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          {isLoading || !userData || !settings ? (
            <div className="text-center py-12">
              <div className="inline-block w-12 h-12 border-4 border-[#C459E0] border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-white/70">Loading settings...</p>
            </div>
          ) : (
            <div className="bg-black/80 backdrop-blur-sm border border-[#C459E0] rounded-2xl p-4 md:p-6 hover-lift transition-all animate-fadeInUp shadow-sm">
              {saveStatus && (
                <div className={`mb-4 p-3 rounded-lg ${
                  saveStatus === 'success'
                    ? 'bg-green-900/50 text-green-300 border border-green-700'
                    : 'bg-red-900/50 text-red-300 border border-red-700'
                }`}>
                  {saveStatus === 'success'
                    ? 'Settings saved successfully!'
                    : 'Failed to save settings. Please try again.'}
                </div>
              )}

              {activeTab === 'account' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Account Information</h2>
                  <div className="space-y-6">
                    <div className="flex items-center space-x-6">
                      <div className="w-16 h-16 rounded-full overflow-hidden border-2 border-[#C459E0]">
                        <img
                          src={userData.avatar}
                          alt="Avatar"
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div>
                        <button className="px-4 py-2 bg-[#C459E0]/20 text-[#C459E0] rounded-lg font-medium hover:bg-[#C459E0]/30 transition-colors">
                          Change Avatar
                        </button>
                        <p className="text-xs text-white/60 mt-1">JPG, GIF or PNG. Max size of 2MB</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-white text-sm mb-2 font-medium">Full Name</label>
                        <input
                          type="text"
                          value={userData.name}
                          onChange={(e) => handleInputChange('name', e.target.value)}
                          className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-white text-sm mb-2 font-medium">Email Address</label>
                        <input
                          type="email"
                          value={userData.email}
                          onChange={(e) => handleInputChange('email', e.target.value)}
                          className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                        />
                      </div>
                    </div>

                    <div className="flex justify-end">
                      <button
                        onClick={handleSave}
                        disabled={isSaving}
                        className="px-6 py-2.5 bg-gradient-to-r from-[#C459E0] to-[#9c27b0] text-white rounded-xl font-semibold hover:from-[#d06ae8] hover:to-[#aa3cc7] transition-all shadow-md hover:shadow-lg hover-lift disabled:opacity-70"
                      >
                        {isSaving ? 'Saving...' : 'Save Changes'}
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'notifications' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Notification Preferences</h2>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-black/50 rounded-xl hover:bg-black/70 transition-all border border-[#C459E0]">
                      <div>
                        <h3 className="text-white font-semibold">Email Notifications</h3>
                        <p className="text-white/60 text-sm">Receive updates via email</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={settings.notifications.email}
                          onChange={(e) => handleInputChange('notifications.email', e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-[#C459E0]/30 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-[#C459E0] after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C459E0]"></div>
                      </label>
                    </div>
                    <div className="flex items-center justify-between p-4 bg-black/50 rounded-xl hover:bg-black/70 transition-all border border-[#C459E0]">
                      <div>
                        <h3 className="text-white font-semibold">Push Notifications</h3>
                        <p className="text-white/60 text-sm">Receive push notifications</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={settings.notifications.push}
                          onChange={(e) => handleInputChange('notifications.push', e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-[#C459E0]/30 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-[#C459E0] after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C459E0]"></div>
                      </label>
                    </div>
                    <div className="flex items-center justify-between p-4 bg-black/50 rounded-xl hover:bg-black/70 transition-all border border-[#C459E0]">
                      <div>
                        <h3 className="text-white font-semibold">SMS Notifications</h3>
                        <p className="text-white/60 text-sm">Receive updates via SMS</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={settings.notifications.sms}
                          onChange={(e) => handleInputChange('notifications.sms', e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-[#C459E0]/30 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-[#C459E0] after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C459E0]"></div>
                      </label>
                    </div>
                    <div className="flex justify-end">
                      <button
                        onClick={handleSave}
                        disabled={isSaving}
                        className="px-6 py-2.5 bg-gradient-to-r from-[#C459E0] to-[#9c27b0] text-white rounded-xl font-semibold hover:from-[#d06ae8] hover:to-[#aa3cc7] transition-all shadow-md hover:shadow-lg hover-lift disabled:opacity-70"
                      >
                        {isSaving ? 'Saving...' : 'Save Changes'}
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'appearance' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Appearance</h2>
                  <div className="space-y-6">
                    <div>
                      <label className="block text-white text-sm mb-2 font-medium">Theme</label>
                      <select
                        value={settings.theme}
                        onChange={(e) => handleInputChange('theme', e.target.value)}
                        className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                      >
                        <option value="light" className="bg-black text-white">Light Theme</option>
                        <option value="dark" className="bg-black text-white">Dark Theme</option>
                        <option value="auto" className="bg-black text-white">System Default</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-white text-sm mb-2 font-medium">Language</label>
                      <select
                        value={settings.language}
                        onChange={(e) => handleInputChange('language', e.target.value)}
                        className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                      >
                        <option value="en" className="bg-black text-white">English</option>
                        <option value="es" className="bg-black text-white">Spanish</option>
                        <option value="fr" className="bg-black text-white">French</option>
                        <option value="de" className="bg-black text-white">German</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-white text-sm mb-2 font-medium">Timezone</label>
                      <select
                        value={settings.timezone}
                        onChange={(e) => handleInputChange('timezone', e.target.value)}
                        className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                      >
                        <option value="UTC" className="bg-black text-white">UTC</option>
                        <option value="EST" className="bg-black text-white">Eastern Standard Time (EST)</option>
                        <option value="PST" className="bg-black text-white">Pacific Standard Time (PST)</option>
                        <option value="CET" className="bg-black text-white">Central European Time (CET)</option>
                      </select>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-white text-sm mb-2 font-medium">Date Format</label>
                        <select
                          value={settings.dateFormat}
                          onChange={(e) => handleInputChange('dateFormat', e.target.value)}
                          className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                        >
                          <option value="MM/DD/YYYY" className="bg-black text-white">MM/DD/YYYY</option>
                          <option value="DD/MM/YYYY" className="bg-black text-white">DD/MM/YYYY</option>
                          <option value="YYYY-MM-DD" className="bg-black text-white">YYYY-MM-DD</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-white text-sm mb-2 font-medium">Time Format</label>
                        <select
                          value={settings.timeFormat}
                          onChange={(e) => handleInputChange('timeFormat', e.target.value)}
                          className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                        >
                          <option value="12h" className="bg-black text-white">12-hour</option>
                          <option value="24h" className="bg-black text-white">24-hour</option>
                        </select>
                      </div>
                    </div>
                    <div className="flex justify-end">
                      <button
                        onClick={handleSave}
                        disabled={isSaving}
                        className="px-6 py-2.5 bg-gradient-to-r from-[#C459E0] to-[#9c27b0] text-white rounded-xl font-semibold hover:from-[#d06ae8] hover:to-[#aa3cc7] transition-all shadow-md hover:shadow-lg hover-lift disabled:opacity-70"
                      >
                        {isSaving ? 'Saving...' : 'Save Changes'}
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'productivity' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Productivity Settings</h2>
                  <div className="space-y-6">
                    <div>
                      <label className="block text-white text-sm mb-2 font-medium">Weekly Goal</label>
                      <div className="relative">
                        <input
                          type="number"
                          min="1"
                          max="50"
                          value={settings.weeklyGoal}
                          onChange={(e) => handleInputChange('weeklyGoal', parseInt(e.target.value))}
                          className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                        />
                        <span className="absolute right-4 top-3.5 text-white/60">tasks</span>
                      </div>
                      <p className="text-sm text-white/60 mt-1">Set your weekly task completion goal</p>
                    </div>

                    <div className="flex items-center justify-between p-4 bg-black/50 rounded-xl hover:bg-black/70 transition-all border border-[#C459E0]">
                      <div>
                        <h3 className="text-white font-semibold">Task Reminders</h3>
                        <p className="text-white/60 text-sm">Receive daily reminders for pending tasks</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={settings.taskReminder}
                          onChange={(e) => handleInputChange('taskReminder', e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-[#C459E0]/30 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-[#C459E0] after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C459E0]"></div>
                      </label>
                    </div>

                    {settings.taskReminder && (
                      <div>
                        <label className="block text-white text-sm mb-2 font-medium">Reminder Time</label>
                        <input
                          type="time"
                          value={settings.taskReminderTime}
                          onChange={(e) => handleInputChange('taskReminderTime', e.target.value)}
                          className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                        />
                      </div>
                    )}

                    <div className="flex items-center justify-between p-4 bg-black/50 rounded-xl hover:bg-black/70 transition-all border border-[#C459E0]">
                      <div>
                        <h3 className="text-white font-semibold">Auto Sync</h3>
                        <p className="text-white/60 text-sm">Automatically sync data across devices</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={settings.autoSync}
                          onChange={(e) => handleInputChange('autoSync', e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-[#C459E0]/30 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-[#C459E0] after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C459E0]"></div>
                      </label>
                    </div>

                    <div className="flex justify-end">
                      <button
                        onClick={handleSave}
                        disabled={isSaving}
                        className="px-6 py-2.5 bg-gradient-to-r from-[#C459E0] to-[#9c27b0] text-white rounded-xl font-semibold hover:from-[#d06ae8] hover:to-[#aa3cc7] transition-all shadow-md hover:shadow-lg hover-lift disabled:opacity-70"
                      >
                        {isSaving ? 'Saving...' : 'Save Changes'}
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'security' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Security</h2>
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-white font-semibold mb-4">Change Password</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-white text-sm mb-2 font-medium">Current Password</label>
                          <input
                            type="password"
                            value={passwordData.currentPassword}
                            onChange={(e) => handlePasswordChange('currentPassword', e.target.value)}
                            className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-white text-sm mb-2 font-medium">New Password</label>
                          <input
                            type="password"
                            value={passwordData.newPassword}
                            onChange={(e) => handlePasswordChange('newPassword', e.target.value)}
                            className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-white text-sm mb-2 font-medium">Confirm New Password</label>
                          <input
                            type="password"
                            value={passwordData.confirmPassword}
                            onChange={(e) => handlePasswordChange('confirmPassword', e.target.value)}
                            className="w-full bg-black/50 border-2 border-[#C459E0] rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#C459E0] transition-all backdrop-blur-sm"
                          />
                        </div>
                      </div>
                    </div>

                    <div className="flex justify-end">
                      <button
                        onClick={handleSave}
                        disabled={isSaving || !passwordData.newPassword}
                        className="px-6 py-2.5 bg-gradient-to-r from-[#C459E0] to-[#9c27b0] text-white rounded-xl font-semibold hover:from-[#d06ae8] hover:to-[#aa3cc7] transition-all shadow-md hover:shadow-lg hover-lift disabled:opacity-70"
                      >
                        {isSaving ? 'Updating...' : 'Update Password'}
                      </button>
                    </div>

                    <div className="pt-6 border-t border-[#C459E0]">
                      <h3 className="text-white font-semibold mb-4">Two-Factor Authentication</h3>
                      <div className="flex items-center justify-between p-4 bg-black/50 rounded-xl border border-[#C459E0]">
                        <div>
                          <h4 className="text-white font-medium">2FA Status</h4>
                          <p className="text-white/60 text-sm">Add an extra layer of security to your account</p>
                        </div>
                        <button className="px-4 py-2 bg-[#C459E0]/20 text-[#C459E0] rounded-lg font-medium hover:bg-[#C459E0]/30 transition-colors">
                          Enable 2FA
                        </button>
                      </div>
                    </div>

                    <div className="pt-6 border-t border-[#C459E0]">
                      <h3 className="text-white font-semibold mb-4">Session Management</h3>
                      <div className="p-4 bg-black/50 rounded-xl border border-[#C459E0]">
                        <div className="flex justify-between items-center">
                          <div>
                            <h4 className="text-white font-medium">Log Out</h4>
                            <p className="text-white/60 text-sm">End your current session</p>
                          </div>
                          <button
                            onClick={async () => {
                              await logout();
                              router.push('/');
                            }}
                            className="px-4 py-2 bg-red-500/20 text-red-300 rounded-lg font-medium hover:bg-red-500/30 transition-colors"
                          >
                            Log Out
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'data' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Data Management</h2>
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-white font-semibold mb-4">Data Export</h3>
                      <div className="p-4 bg-black/50 rounded-xl border border-[#C459E0]">
                        <p className="text-white/60 mb-4">Export your data including tasks, projects, and settings in JSON format</p>
                        <button
                          onClick={handleDataExport}
                          className="px-4 py-2 bg-[#C459E0]/20 text-[#C459E0] rounded-lg font-medium hover:bg-[#C459E0]/30 transition-colors"
                        >
                          Export Data
                        </button>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-white font-semibold mb-4">Data Sync</h3>
                      <div className="flex items-center justify-between p-4 bg-black/50 rounded-xl border border-[#C459E0]">
                        <div>
                          <h4 className="text-white font-medium">Auto Sync</h4>
                          <p className="text-white/60 text-sm">Automatically sync data across devices</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={settings.autoSync}
                            onChange={(e) => handleInputChange('autoSync', e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-[#C459E0]/30 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-[#C459E0] after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C459E0]"></div>
                        </label>
                      </div>
                    </div>

                    <div className="pt-6 border-t border-[#C459E0]">
                      <h3 className="text-white font-semibold mb-4">Account Deletion</h3>
                      <div className="p-4 bg-red-900/30 rounded-xl border border-red-700">
                        <h4 className="text-red-300 font-medium">Delete Account</h4>
                        <p className="text-red-400 text-sm mb-4">Permanently delete your account and all associated data</p>
                        <button
                          onClick={handleDeleteAccount}
                          className="px-4 py-2 bg-red-500/20 text-red-300 rounded-lg font-medium hover:bg-red-500/30 transition-colors"
                        >
                          Delete Account
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  )
}
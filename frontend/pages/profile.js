import Head from 'next/head'
import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'

export default function Profile() {
  const { user } = useAuth()
  const userId = user?.id || 'user_123'
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const [userData, setUserData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [editData, setEditData] = useState({})

  // Fetch profile on mount
  useEffect(() => {
    if (userId) {
      fetchProfile()
    }
  }, [userId])

  const fetchProfile = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/profile`)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const profileData = await response.json()
      setUserData(profileData)
      setEditData(profileData)
    } catch (error) {
      console.error('Failed to fetch profile:', error)
      setUserData({
        name: user?.email?.split('@')[0] || 'User',
        email: user?.email || 'user@example.com',
        role: 'User',
        join_date: 'Recently',
        bio: '',
        location: '',
        website: '',
        tasks_completed: 0,
        projects_managed: 0,
        streak: 0
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleEditToggle = async () => {
    if (isEditing) {
      // Save changes via API
      try {
        const response = await fetch(`${API_BASE_URL}/api/${userId}/profile`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: editData.name,
            email: editData.email,
            bio: editData.bio,
            location: editData.location,
            website: editData.website
          })
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const updatedProfile = await response.json()
        setUserData(updatedProfile)
        setEditData(updatedProfile)
      } catch (error) {
        console.error('Failed to update profile:', error)
        alert('Failed to save changes. Please try again.')
        return // Don't toggle editing mode on error
      }
    }
    setIsEditing(!isEditing)
  }

  const handleInputChange = (field, value) => {
    setEditData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  return (
    <>
      <Head>
        <title>Profile - TaskFlow</title>
        <meta name="description" content="TaskFlow Profile" />
      </Head>

      {/* Header */}
      <div className="bg-brand-card-bg/80 backdrop-blur-sm border-b border-brand-card-border px-4 py-3 md:px-8 md:py-6 animate-fadeInDown">
        <h1 className="text-3xl font-bold text-white mb-1">
          <span className="bg-gradient-to-r from-brand-button to-brand-button-hover bg-clip-text text-transparent">Profile</span>
        </h1>
        <p className="text-white/70 text-sm">Manage your personal information</p>
      </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-4 py-3 md:px-8 md:py-6 animate-fadeIn">
          <div className="max-w-4xl mx-auto">
            {isLoading || !userData ? (
              <div className="text-center py-12">
                <div className="inline-block w-12 h-12 border-4 border-brand-button border-t-transparent rounded-full animate-spin mb-4"></div>
                <p className="text-white/60">Loading profile...</p>
              </div>
            ) : (
              <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all animate-fadeInUp">
                <div className="flex flex-col md:flex-row gap-8">
                  {/* Profile Picture and Info */}
                  <div className="md:w-1/3 flex flex-col items-center animate-fadeInLeft">
                    <div className="w-32 h-32 rounded-full bg-gradient-to-br from-brand-button to-brand-button-hover mb-4 flex items-center justify-center shadow-lg shadow-brand-button/30 hover-lift">
                      <span className="text-4xl font-bold text-white">{userData.name.charAt(0)}</span>
                    </div>
                    <h2 className="text-2xl font-bold text-white">{userData.name}</h2>
                    <p className="text-brand-button font-semibold">{userData.role}</p>
                    <p className="text-white/60 text-sm mt-1">Member since {userData.join_date}</p>

                  <div className="mt-6 w-full">
                    <button
                      onClick={handleEditToggle}
                      className="w-full min-h-[44px] bg-gradient-to-r from-brand-button to-brand-button-hover text-white rounded-xl font-semibold hover:from-brand-button-hover hover:to-brand-button transition-all shadow-lg shadow-brand-button/30 hover-lift"
                    >
                      {isEditing ? 'Save Changes' : 'Edit Profile'}
                    </button>
                  </div>
                </div>

                {/* Profile Details */}
                <div className="md:w-2/3 animate-fadeInRight">
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-bold text-white mb-3">Personal Information</h3>
                      <div className="space-y-4">
                        <div>
                          <label className="block text-white text-sm mb-1 font-medium">Full Name</label>
                          {isEditing ? (
                            <input
                              type="text"
                              value={editData.name}
                              onChange={(e) => setEditData({...editData, name: e.target.value})}
                              className="w-full bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                            />
                          ) : (
                            <p className="text-white font-medium">{userData.name}</p>
                          )}
                        </div>
                        <div>
                          <label className="block text-white text-sm mb-1 font-medium">Email</label>
                          {isEditing ? (
                            <input
                              type="email"
                              value={editData.email}
                              onChange={(e) => setEditData({...editData, email: e.target.value})}
                              className="w-full bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                            />
                          ) : (
                            <p className="text-white font-medium">{userData.email}</p>
                          )}
                        </div>
                        <div>
                          <label className="block text-white text-sm mb-1 font-medium">Location</label>
                          {isEditing ? (
                            <input
                              type="text"
                              value={editData.location}
                              onChange={(e) => setEditData({...editData, location: e.target.value})}
                              className="w-full bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                            />
                          ) : (
                            <p className="text-white font-medium">{userData.location}</p>
                          )}
                        </div>
                        <div>
                          <label className="block text-white text-sm mb-1 font-medium">Website</label>
                          {isEditing ? (
                            <input
                              type="text"
                              value={editData.website}
                              onChange={(e) => setEditData({...editData, website: e.target.value})}
                              className="w-full bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                            />
                          ) : (
                            <p className="text-white font-medium">{userData.website}</p>
                          )}
                        </div>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-lg font-bold text-white mb-3">About</h3>
                      {isEditing ? (
                        <textarea
                          value={editData.bio}
                          onChange={(e) => setEditData({...editData, bio: e.target.value})}
                          rows="4"
                          className="w-full bg-brand-bg/50 border-2 border-brand-card-border rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-brand-button transition-all backdrop-blur-sm"
                        />
                      ) : (
                        <p className="text-white/70">{userData.bio}</p>
                      )}
                    </div>

                    <div>
                      <h3 className="text-lg font-bold text-white mb-3">Statistics</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-brand-card-bg/30 border border-brand-card-border rounded-xl p-4 text-center hover-lift transition-all">
                          <p className="text-2xl font-bold text-brand-button">{userData.tasks_completed}</p>
                          <p className="text-white/60 text-sm font-medium">Tasks Completed</p>
                        </div>
                        <div className="bg-brand-card-bg/30 border border-brand-card-border rounded-xl p-4 text-center hover-lift transition-all">
                          <p className="text-2xl font-bold text-brand-button">{userData.projects_managed}</p>
                          <p className="text-white/60 text-sm font-medium">Projects</p>
                        </div>
                        <div className="bg-brand-card-bg/30 border border-brand-card-border rounded-xl p-4 text-center hover-lift transition-all">
                          <p className="text-2xl font-bold text-brand-button">{userData.streak} days</p>
                          <p className="text-white/60 text-sm font-medium">Streak</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              </div>
            )}
          </div>
        </div>
    </>
  )
}

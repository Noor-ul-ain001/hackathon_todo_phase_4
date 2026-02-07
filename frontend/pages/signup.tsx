/**
 * Sign Up Page for TaskFlow Intelligence Platform
 * Provides user registration with email and password
 */

import { FC, FormEvent, useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'

const SignUp: FC = () => {
  const router = useRouter()
  const { register } = useAuth()

  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [confirmPassword, setConfirmPassword] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError('')

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    // Validate password length
    if (password.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }

    setLoading(true)

    try {
      await register({ email, password })
      router.push('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-brand-bg flex">
      <Head>
        <title>Sign Up - TaskFlow Intelligence Platform</title>
        <meta name="description" content="Create your TaskFlow Intelligence Platform account" />
      </Head>

      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-brand-card-bg to-brand-bg p-12 flex-col justify-between relative overflow-hidden border-r border-brand-card-border">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-brand-button/20 to-brand-button/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gradient-to-br from-brand-chat/10 to-brand-button/10 rounded-full blur-3xl animate-pulse animate-delay-300"></div>

        <div className="relative z-10 animate-fadeInLeft">
          {/* Logo */}
          <Link href="/">
            <div className="flex items-center space-x-3 cursor-pointer group">
              <div className="w-12 h-12 bg-brand-button rounded-xl flex items-center justify-center group-hover:shadow-lg group-hover:shadow-brand-button/30 transition-all hover-lift">
                <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                  <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <span className="text-white text-2xl font-bold">TASKFLOW</span>
            </div>
          </Link>
        </div>

        <div className="relative z-10 animate-fadeInLeft animate-delay-200">
          {/* Decorative Lines */}
          <div className="flex items-center space-x-2 mb-8 animate-fadeInLeft animate-delay-300">
            <div className="h-px w-16 bg-gradient-to-r from-brand-button to-transparent animate-fadeInLeft"></div>
            <div className="h-px w-8 bg-gradient-to-r from-brand-button to-transparent animate-fadeInLeft animate-delay-100"></div>
            <div className="h-px w-4 bg-gradient-to-r from-brand-button to-transparent animate-fadeInLeft animate-delay-200"></div>
          </div>

          <h1 className="text-5xl font-bold text-white mb-6 leading-tight animate-fadeInUp">
            Start Your<br />
            <span className="gradient-text">Journey Today.</span>
          </h1>
          <p className="text-xl text-white/70 mb-2 animate-fadeInUp animate-delay-200">
            Join teams using AI-powered task management.
          </p>
          <p className="text-lg text-white/60 animate-fadeInUp animate-delay-300">
            Built for the Agent Era.
          </p>
        </div>

        <div className="relative z-10">
          <p className="text-slate-400 text-sm">
            © 2025 TaskFlow Intelligence Platform. All rights reserved.
          </p>
        </div>
      </div>

      {/* Right Side - Signup Form */}
      <div className="flex-1 flex items-center justify-center p-8 animate-fadeInRight bg-brand-card-bg/50 backdrop-blur-sm">
        <div className="w-full max-w-md animate-scaleIn">
          {/* Mobile Logo */}
          <div className="lg:hidden mb-8 text-center">
            <div className="flex items-center justify-center space-x-3 mb-6">
              <div className="w-12 h-12 bg-brand-button rounded-xl flex items-center justify-center">
                <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                  <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <span className="text-white text-2xl font-bold">TASKFLOW</span>
            </div>
          </div>

          {/* Form Header */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-white mb-2">Create Account</h2>
            <p className="text-white/70">Start managing tasks with AI</p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-900/30 border-2 border-red-700 rounded-xl animate-shake animate-fadeIn">
              <div className="flex items-center space-x-2">
                <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            </div>
          )}

          {/* Signup Form */}
          <form onSubmit={handleSubmit} className="space-y-6 stagger-children">
            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-white mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 bg-brand-card-bg border-2 border-brand-card-border rounded-xl text-white placeholder-white/40 focus:outline-none focus:border-brand-button transition-all duration-300 focus:scale-[1.02] hover-lift"
                placeholder="you@example.com"
              />
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-white mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-brand-card-bg border-2 border-brand-card-border rounded-xl text-white placeholder-white/40 focus:outline-none focus:border-brand-button transition-all duration-300 focus:scale-[1.02] hover-lift"
                placeholder="Min 8 characters"
              />
              <p className="mt-2 text-xs text-slate-400">Must be at least 8 characters</p>
            </div>

            {/* Confirm Password Field */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-white mb-2">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-3 bg-brand-card-bg border-2 border-brand-card-border rounded-xl text-white placeholder-white/40 focus:outline-none focus:border-brand-button transition-all duration-300 focus:scale-[1.02] hover-lift"
                placeholder="Re-enter password"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-brand-button text-white rounded-xl font-semibold hover:bg-brand-button-hover transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-brand-button/30 hover:shadow-xl hover:shadow-brand-button/40 hover:-translate-y-0.5 transform active:scale-95"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Creating account...</span>
                </div>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          {/* Terms */}
          <p className="mt-6 text-xs text-center text-white/60">
            By creating an account, you agree to our{' '}
            <Link href="/terms" className="text-brand-button hover:text-brand-button-hover transition-colors duration-200">
              Terms of Service
            </Link>{' '}
            and{' '}
            <Link href="/privacy" className="text-brand-button hover:text-brand-button-hover transition-colors duration-200">
              Privacy Policy
            </Link>
          </p>

          {/* Divider */}
          <div className="relative my-8">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-700"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-brand-bg text-slate-400">Or</span>
            </div>
          </div>

          {/* Sign In Link */}
          <div className="text-center">
            <p className="text-white/70 text-sm">
              Already have an account?{' '}
              <Link href="/login" className="text-brand-button hover:text-brand-button-hover font-semibold transition-colors duration-200">
                Sign in
              </Link>
            </p>
          </div>

          {/* Back to Home */}
          <div className="text-center mt-6">
            <Link href="/" className="text-white/60 hover:text-white text-sm inline-flex items-center space-x-1 transition-colors duration-200">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              <span>Back to home</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SignUp

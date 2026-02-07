import { FC, useEffect, useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'

/**
 * TaskFlow Intelligence Platform - Complete Landing Page
 * Modern design inspired by home-land.PNG with full sections
 */
const Home: FC = () => {
  const router = useRouter()
  const { isAuthenticated, loading } = useAuth()
  const [activeTab, setActiveTab] = useState<'text' | 'voice' | 'image'>('text')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, loading, router])

  return (
    <>
      <Head>
        <title>TaskFlow - Intelligence Platform</title>
        <meta name="description" content="The only project management platform designed for the Agent Era" />
        <link rel="icon" href="/favicon.ico" />
        <style>{`
          /* Color Palette - Brand Colors */
          body {
            background: #FAFAFA;
            min-height: 100vh;
          }

          .hero-gradient {
            background: linear-gradient(135deg, #FAFAFA 0%, #fff 50%, #FAFAFA 100%);
          }

          .glass-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.8);
            box-shadow: 0 8px 32px rgba(240, 173, 83, 0.1);
          }

          .floating-card {
            animation: float 3s ease-in-out infinite;
          }

          @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
          }

          .gradient-text {
            background: linear-gradient(135deg, #F0AD53 0%, #e09842 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }

          .section-light {
            background: #ffffff;
          }

          .section-gray {
            background: #FAFAFA;
          }
        `}</style>
      </Head>

      <div style={{ minHeight: '100vh' }}>
        {/* Navigation */}
        <nav className="max-w-[1400px] mx-auto sticky top-0 bg-brand-bg/95 backdrop-blur-sm z-1000 animate-fadeInDown px-4 py-3 md:px-8 lg:px-12">
          <div className="flex items-center justify-between">
            <div className="text-2xl font-bold text-white tracking-tight">
              TaskFlow
            </div>

            {/* Desktop Navigation Links */}
            <div className="hidden md:flex items-center gap-8 lg:gap-10">
              <a href="#home" className="text-white text-base font-medium hover:text-brand-button transition-colors duration-300">
                Home
              </a>
              <a href="#features" className="text-slate-400 text-base font-medium hover:text-brand-button transition-colors duration-300">
                Features
              </a>
              <a href="#how-it-works" className="text-slate-400 text-base font-medium hover:text-brand-button transition-colors duration-300">
                How it works
              </a>
              <a href="#chatbot" className="text-slate-400 text-base font-medium hover:text-brand-button transition-colors duration-300">
                AI Chatbot
              </a>
            </div>

            {/* Desktop Auth Buttons */}
            <div className="hidden md:flex items-center gap-3">
              <Link href="/login">
                <button className="hover-lift min-h-[44px] px-6 py-2.5 text-brand-button font-semibold border-0 rounded-lg transition-colors duration-300 hover:bg-brand-button/10">
                  Login
                </button>
              </Link>
              <Link href="/signup">
                <button className="min-h-[44px] px-7 py-2.5 bg-brand-button text-white font-semibold border-0 rounded-lg transition-all duration-300 hover:bg-brand-button-hover shadow-lg shadow-brand-button/30 hover:shadow-xl hover:shadow-brand-button/40 hover:-translate-y-0.5 transform">
                  Try Free
                </button>
              </Link>
            </div>

            {/* Mobile Hamburger Menu */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden w-10 h-10 flex items-center justify-center rounded-lg text-white hover:bg-slate-700 transition-colors"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-4 py-4 border-t border-slate-700 animate-fadeIn">
              <div className="flex flex-col space-y-4">
                <a
                  href="#home"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-white font-medium py-2 hover:text-brand-button transition-colors"
                >
                  Home
                </a>
                <a
                  href="#features"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-slate-400 font-medium py-2 hover:text-brand-button transition-colors"
                >
                  Features
                </a>
                <a
                  href="#how-it-works"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-slate-400 font-medium py-2 hover:text-brand-button transition-colors"
                >
                  How it works
                </a>
                <a
                  href="#chatbot"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-slate-400 font-medium py-2 hover:text-brand-button transition-colors"
                >
                  AI Chatbot
                </a>
                <div className="flex flex-col gap-3 pt-4 border-t border-slate-700">
                  <Link href="/login" className="w-full">
                    <button className="w-full min-h-[44px] py-2 px-4 text-brand-button font-semibold border-2 border-brand-button rounded-lg hover:bg-brand-button/10 transition-colors">
                      Login
                    </button>
                  </Link>
                  <Link href="/signup" className="w-full">
                    <button className="w-full min-h-[44px] py-2 px-4 bg-brand-button text-white font-semibold rounded-lg hover:bg-brand-button-hover transition-colors shadow-lg">
                      Try Free
                    </button>
                  </Link>
                </div>
              </div>
            </div>
          )}
        </nav>

        {/* Hero Section */}
        <section id="home" className="bg-gradient-to-br from-brand-bg to-brand-chat/20 min-h-[calc(100vh-100px)] px-4 py-8 md:px-8 md:py-12 lg:px-12 lg:py-16 relative overflow-hidden">
          {/* Animated background elements */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
            <div className="absolute top-20 left-10 w-72 h-72 bg-brand-button/10 rounded-full blur-3xl animate-pulse animate-infinite"></div>
            <div className="absolute bottom-10 right-10 w-96 h-96 bg-brand-button/5 rounded-full blur-3xl animate-pulse animate-delay-1000 animate-infinite"></div>
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-brand-button/5 rounded-full blur-3xl animate-pulse animate-delay-2000 animate-infinite"></div>

            {/* Floating particles */}
            {[...Array(15)].map((_, i) => (
              <div
                key={i}
                className="absolute rounded-full bg-brand-button/20 animate-float"
                style={{
                  width: `${Math.random() * 10 + 5}px`,
                  height: `${Math.random() * 10 + 5}px`,
                  top: `${Math.random() * 100}%`,
                  left: `${Math.random() * 100}%`,
                  animationDuration: `${Math.random() * 10 + 10}s`,
                  animationDelay: `${Math.random() * 5}s`
                }}
              ></div>
            ))}
          </div>

          <div className="max-w-[1400px] mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12 lg:gap-16 items-center relative z-10">
            {/* Left Side - Content */}
            <div className="animate-fadeInLeft lg:pr-8">
              <div className="inline-block px-4 py-1.5 bg-brand-button/20 rounded-full mb-4 border border-brand-button/30 animate-fadeInUp">
                <span className="text-sm font-medium text-brand-button">AI-Powered Task Management</span>
              </div>

              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 md:mb-6 text-white leading-tight tracking-tight animate-fadeInUp animate-delay-100">
                Transform Your<br />
                <span className="gradient-text">Workflow</span> with AI
              </h1>

              <p className="text-base md:text-lg lg:text-xl mb-6 md:mb-8 max-w-full lg:max-w-lg text-white/70 leading-relaxed animate-fadeInUp animate-delay-200">
                Plan with TaskFlow. Execute with Agents. Audit everything.
                The future of productivity is here.
              </p>

              <div className="flex flex-col sm:flex-row gap-3 md:gap-4 mb-6 animate-fadeInUp animate-delay-300">
                <div className="relative flex-1">
                  <input
                    type="email"
                    placeholder="Enter your email address"
                    className="w-full min-h-[44px] px-5 py-3 bg-brand-card-bg/50 border border-brand-card-border rounded-xl text-white placeholder-white/40 focus:outline-none focus:border-brand-button transition-all duration-300 backdrop-blur-sm hover:shadow-lg hover:shadow-brand-button/10"
                  />
                  <div className="absolute inset-0 bg-gradient-to-r from-brand-button/10 to-transparent rounded-xl pointer-events-none"></div>
                </div>
                <button className="px-6 py-3 bg-gradient-to-r from-brand-button to-brand-button-hover text-white font-semibold rounded-xl transition-all duration-300 hover:shadow-lg hover:shadow-brand-button/30 hover:-translate-y-0.5 transform active:scale-95 backdrop-blur-sm hover:animate-pulse">
                  Get Started
                </button>
              </div>

              <div className="flex items-center space-x-4 text-sm text-white/60 animate-fadeInUp animate-delay-400">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-green-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  No credit card required
                </div>
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-green-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Free 14-day trial
                </div>
              </div>

              {/* Stats bar */}
              <div className="mt-8 grid grid-cols-3 gap-4 animate-fadeInUp animate-delay-500">
                <div className="text-center p-4 bg-brand-card-bg/20 backdrop-blur-sm rounded-xl border border-brand-card-border/30">
                  <div className="text-2xl font-bold text-brand-button">99.9%</div>
                  <div className="text-xs text-white/70">Uptime</div>
                </div>
                <div className="text-center p-4 bg-brand-card-bg/20 backdrop-blur-sm rounded-xl border border-brand-card-border/30">
                  <div className="text-2xl font-bold text-brand-button">24/7</div>
                  <div className="text-xs text-white/70">Support</div>
                </div>
                <div className="text-center p-4 bg-brand-card-bg/20 backdrop-blur-sm rounded-xl border border-brand-card-border/30">
                  <div className="text-2xl font-bold text-brand-button">10K+</div>
                  <div className="text-xs text-white/70">Users</div>
                </div>
              </div>
            </div>

            {/* Right Side - Visual */}
            <div className="animate-fadeInRight relative">
              <div className="relative">
                <div className="absolute -inset-4 bg-gradient-to-r from-brand-button/20 to-brand-button/5 rounded-3xl blur-xl animate-pulse animate-infinite"></div>
                <div className="relative bg-brand-card-bg/30 backdrop-blur-xl border border-brand-card-border/50 rounded-2xl p-6 shadow-2xl transform hover:scale-[1.02] transition-transform duration-500">
                  <div className="flex justify-between items-center mb-6">
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 rounded-full bg-red-400 animate-pulse"></div>
                      <div className="w-3 h-3 rounded-full bg-yellow-400 animate-pulse animate-delay-200"></div>
                      <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse animate-delay-400"></div>
                    </div>
                    <div className="text-sm text-white/60">Dashboard</div>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-brand-bg/50 rounded-lg border border-brand-card-border/30 hover:bg-brand-bg/70 transition-colors duration-300 animate-fadeInUp animate-delay-100">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 rounded-lg bg-brand-button/20 flex items-center justify-center animate-bounce animate-delay-1000">
                          <svg className="w-5 h-5 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                          </svg>
                        </div>
                        <div>
                          <div className="font-medium text-white">Weekly Report</div>
                          <div className="text-xs text-white/60">Due in 2 days</div>
                        </div>
                      </div>
                      <div className="px-2 py-1 bg-brand-button/20 text-brand-button text-xs rounded-full animate-pulse">In Progress</div>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-brand-bg/50 rounded-lg border border-brand-card-border/30 hover:bg-brand-bg/70 transition-colors duration-300 animate-fadeInUp animate-delay-200">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 rounded-lg bg-brand-button/20 flex items-center justify-center animate-bounce animate-delay-1200">
                          <svg className="w-5 h-5 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                        </div>
                        <div>
                          <div className="font-medium text-white">Team Meeting</div>
                          <div className="text-xs text-white/60">Today, 3:00 PM</div>
                        </div>
                      </div>
                      <div className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full animate-pulse">Completed</div>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-brand-bg/50 rounded-lg border border-brand-card-border/30 hover:bg-brand-bg/70 transition-colors duration-300 animate-fadeInUp animate-delay-300">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 rounded-lg bg-brand-button/20 flex items-center justify-center animate-bounce animate-delay-1400">
                          <svg className="w-5 h-5 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <div>
                          <div className="font-medium text-white">Project Review</div>
                          <div className="text-xs text-white/60">Due tomorrow</div>
                        </div>
                      </div>
                      <div className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full animate-pulse">Pending</div>
                    </div>
                  </div>

                  <div className="mt-6 pt-4 border-t border-brand-card-border/30 animate-fadeInUp animate-delay-400">
                    <div className="flex justify-between text-sm">
                      <span className="text-white/60">Progress</span>
                      <span className="text-white">78%</span>
                    </div>
                    <div className="mt-2 w-full bg-brand-bg/50 rounded-full h-2.5 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-brand-button to-brand-button-hover h-2.5 rounded-full animate-progress"
                        style={{ width: '78%', animation: 'progressAnimation 2s ease-out forwards' }}
                      ></div>
                    </div>
                  </div>
                </div>

                {/* Floating notification */}
                <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-brand-button/10 rounded-full blur-xl animate-float animate-delay-2000"></div>
                <div className="absolute -top-6 -right-6 w-24 h-24 bg-brand-button/10 rounded-full blur-xl animate-float animate-delay-3000"></div>
              </div>
            </div>

          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="px-4 py-16 md:py-24 lg:py-32 bg-brand-bg/30 relative overflow-hidden">
          {/* Background elements */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
            <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-brand-button/5 rounded-full blur-2xl animate-pulse animate-infinite"></div>
            <div className="absolute bottom-1/3 right-1/4 w-72 h-72 bg-brand-button/5 rounded-full blur-2xl animate-pulse animate-delay-1000 animate-infinite"></div>

            {/* Floating particles */}
            {[...Array(10)].map((_, i) => (
              <div
                key={i}
                className="absolute rounded-full bg-brand-button/10 animate-float"
                style={{
                  width: `${Math.random() * 15 + 5}px`,
                  height: `${Math.random() * 15 + 5}px`,
                  top: `${Math.random() * 100}%`,
                  left: `${Math.random() * 100}%`,
                  animationDuration: `${Math.random() * 15 + 10}s`,
                  animationDelay: `${Math.random() * 5}s`
                }}
              ></div>
            ))}
          </div>

          <div className="max-w-[1400px] mx-auto">
            <div className="text-center mb-16 animate-fadeInUp">
              <div className="inline-block px-4 py-1.5 bg-brand-button/20 rounded-full mb-4 border border-brand-button/30 animate-fadeInUp animate-delay-100">
                <span className="text-sm font-medium text-brand-button">Why Choose TaskFlow</span>
              </div>
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 text-white animate-fadeInUp animate-delay-200">
                Powerful Features for Modern Teams
              </h2>
              <p className="text-base md:text-lg mx-auto max-w-full md:max-w-xl px-4 text-white/70 animate-fadeInUp animate-delay-300">
                Everything you need to manage tasks efficiently in the AI era
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[
                {
                  icon: '🤖',
                  title: 'AI-Powered Assistant',
                  description: 'Natural language task management. Just tell our AI what you need, and it handles the rest.',
                  color: 'brand'
                },
                {
                  icon: '📊',
                  title: 'Smart Analytics',
                  description: 'Get insights into your productivity with beautiful dashboards and real-time metrics.',
                  color: 'brand'
                },
                {
                  icon: '🔄',
                  title: 'Recursive Tasks',
                  description: 'Break down complex projects into manageable subtasks automatically.',
                  color: 'brand'
                },
                {
                  icon: '🎯',
                  title: 'Multi-Tenant Support',
                  description: 'Secure workspaces for teams with role-based access control.',
                  color: 'brand'
                },
                {
                  icon: '💬',
                  title: 'Multi-Modal Chat',
                  description: 'Text, voice, and image inputs - interact with your tasks however you prefer.',
                  color: 'brand'
                },
                {
                  icon: '🔒',
                  title: 'Enterprise Security',
                  description: 'Bank-level encryption, SOC 2 compliance, and full data ownership.',
                  color: 'brand'
                }
              ].map((feature, index) => (
                <div
                  key={index}
                  className="p-6 rounded-2xl bg-gradient-to-br from-brand-card-bg/50 to-brand-bg/30 backdrop-blur-sm border border-brand-card-border/50 transition-all duration-500 cursor-pointer hover:border-brand-button hover:shadow-xl hover:shadow-brand-button/20 animate-fadeInUp group"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="relative">
                    <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-brand-button/30 to-brand-button/10 flex items-center justify-center text-2xl mb-4 group-hover:bg-brand-button/40 transition-all duration-300 transform group-hover:scale-110 group-hover:rotate-3">
                      {feature.icon}
                    </div>
                    <div className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-brand-button flex items-center justify-center text-white text-xs animate-ping animate-delay-1000"></div>
                  </div>
                  <h3 className="text-lg md:text-xl font-bold mb-3 text-white group-hover:text-brand-button transition-colors duration-300">
                    {feature.title}
                  </h3>
                  <p className="text-sm md:text-base text-white/70 leading-relaxed group-hover:text-white/90 transition-colors duration-300">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>

            {/* Feature highlights */}
            <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/30 rounded-2xl p-6 text-center animate-fadeInUp animate-delay-400">
                <div className="text-4xl mb-4">🚀</div>
                <h3 className="text-lg font-bold text-white mb-2">Lightning Fast</h3>
                <p className="text-white/70 text-sm">Deploy in seconds, scale infinitely</p>
              </div>
              <div className="bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/30 rounded-2xl p-6 text-center animate-fadeInUp animate-delay-500">
                <div className="text-4xl mb-4">🛡️</div>
                <h3 className="text-lg font-bold text-white mb-2">Enterprise Security</h3>
                <p className="text-white/70 text-sm">Military-grade encryption & compliance</p>
              </div>
              <div className="bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/30 rounded-2xl p-6 text-center animate-fadeInUp animate-delay-600">
                <div className="text-4xl mb-4">📈</div>
                <h3 className="text-lg font-bold text-white mb-2">Growth Optimized</h3>
                <p className="text-white/70 text-sm">Scale your business with AI insights</p>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section id="how-it-works" className="px-4 py-16 md:py-24 lg:py-32 bg-brand-bg relative overflow-hidden">
          {/* Background elements */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
            <div className="absolute top-1/3 left-1/4 w-64 h-64 bg-brand-button/10 rounded-full blur-2xl animate-pulse animate-infinite"></div>
            <div className="absolute bottom-1/4 right-1/3 w-72 h-72 bg-brand-button/10 rounded-full blur-2xl animate-pulse animate-delay-1000 animate-infinite"></div>

            {/* Floating particles */}
            {[...Array(12)].map((_, i) => (
              <div
                key={i}
                className="absolute rounded-full bg-brand-button/5 animate-float"
                style={{
                  width: `${Math.random() * 12 + 4}px`,
                  height: `${Math.random() * 12 + 4}px`,
                  top: `${Math.random() * 100}%`,
                  left: `${Math.random() * 100}%`,
                  animationDuration: `${Math.random() * 12 + 8}s`,
                  animationDelay: `${Math.random() * 6}s`
                }}
              ></div>
            ))}
          </div>

          <div className="max-w-[1400px] mx-auto">
            <div className="text-center mb-16 animate-fadeInUp">
              <div className="inline-block px-4 py-1.5 bg-brand-button/20 rounded-full mb-4 border border-brand-button/30 animate-fadeInUp animate-delay-100">
                <span className="text-sm font-medium text-brand-button">Simple Process</span>
              </div>
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 text-white animate-fadeInUp animate-delay-200">
                How TaskFlow Works
              </h2>
              <p className="text-base md:text-lg mx-auto max-w-full md:max-w-xl px-4 text-white/70 animate-fadeInUp animate-delay-300">
                Get started in minutes with our simple three-step process
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                {
                  step: '01',
                  title: 'Create Your Workspace',
                  description: 'Sign up and create your secure workspace. Invite team members and set up roles in seconds.',
                  color: 'brand'
                },
                {
                  step: '02',
                  title: 'Talk to Your AI Assistant',
                  description: 'Use natural language to create, update, and manage tasks. Our AI understands context and intent.',
                  color: 'brand'
                },
                {
                  step: '03',
                  title: 'Track & Execute',
                  description: 'Watch your productivity soar with real-time analytics, smart notifications, and automated workflows.',
                  color: 'brand'
                }
              ].map((step, index) => (
                <div
                  key={index}
                  className="relative animate-fadeInUp group"
                  style={{ animationDelay: `${index * 200}ms` }}
                >
                  <div className="absolute -top-6 -left-6 w-24 h-24 bg-brand-button/10 rounded-full blur-xl -z-10 group-hover:scale-110 transition-transform duration-500 animate-pulse animate-infinite"></div>
                  <div className="relative bg-gradient-to-br from-brand-card-bg/30 to-brand-bg/30 backdrop-blur-sm border border-brand-card-border/30 rounded-2xl p-8 text-center transition-all duration-500 hover:border-brand-button hover:shadow-xl hover:shadow-brand-button/20 hover:-translate-y-2">
                    <div className="relative w-16 h-16 rounded-full bg-gradient-to-br from-brand-button to-brand-button-hover flex items-center justify-center text-white text-2xl font-bold mx-auto mb-6 shadow-lg shadow-brand-button/30 group-hover:animate-bounce">
                      {step.step}
                    </div>
                    <h3 className="text-xl md:text-2xl font-bold mb-4 text-white group-hover:text-brand-button transition-colors duration-300">
                      {step.title}
                    </h3>
                    <p className="text-base md:text-lg text-white/70 leading-relaxed group-hover:text-white/90 transition-colors duration-300">
                      {step.description}
                    </p>

                    {/* Decorative elements */}
                    <div className="absolute -bottom-4 -right-4 w-8 h-8 rounded-full bg-brand-button/20 animate-pulse"></div>
                    <div className="absolute -top-4 -right-8 w-4 h-4 rounded-full bg-brand-button/30 animate-pulse animate-delay-500"></div>
                  </div>
                </div>
              ))}
            </div>

            {/* Process visualization */}
            <div className="mt-20 relative">
              <div className="absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-brand-button/30 to-transparent transform -translate-y-1/2"></div>
              <div className="flex justify-between relative z-10">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-brand-button to-brand-button-hover flex items-center justify-center text-white text-xl font-bold shadow-lg shadow-brand-button/30 animate-pulse">
                  1
                </div>
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-brand-button to-brand-button-hover flex items-center justify-center text-white text-xl font-bold shadow-lg shadow-brand-button/30 animate-pulse animate-delay-500">
                  2
                </div>
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-brand-button to-brand-button-hover flex items-center justify-center text-white text-xl font-bold shadow-lg shadow-brand-button/30 animate-pulse animate-delay-1000">
                  3
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* AI Chat Section */}
        <section id="ai-chat" className="px-4 py-16 md:py-24 lg:py-32 bg-gradient-to-br from-brand-bg to-brand-chat/20 relative overflow-hidden">
          {/* Animated background elements */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
            <div className="absolute top-1/4 right-1/4 w-64 h-64 bg-brand-button/10 rounded-full blur-2xl animate-pulse animate-infinite"></div>
            <div className="absolute bottom-1/3 left-1/4 w-72 h-72 bg-brand-button/10 rounded-full blur-2xl animate-pulse animate-delay-1000 animate-infinite"></div>

            {/* Floating particles */}
            {[...Array(12)].map((_, i) => (
              <div
                key={i}
                className="absolute rounded-full bg-brand-button/5 animate-float"
                style={{
                  width: `${Math.random() * 12 + 4}px`,
                  height: `${Math.random() * 12 + 4}px`,
                  top: `${Math.random() * 100}%`,
                  left: `${Math.random() * 100}%`,
                  animationDuration: `${Math.random() * 10 + 10}s`,
                  animationDelay: `${Math.random() * 5}s`
                }}
              ></div>
            ))}
          </div>

          <div className="max-w-[1400px] mx-auto">
            <div className="text-center mb-16 animate-fadeInUp">
              <div className="inline-block px-4 py-1.5 bg-brand-button/20 rounded-full mb-4 border border-brand-button/30 animate-fadeInUp animate-delay-100">
                <span className="text-sm font-medium text-brand-button">AI Assistant</span>
              </div>
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 text-white animate-fadeInUp animate-delay-200">
                Meet Your AI Task Assistant
              </h2>
              <p className="text-base md:text-lg mx-auto max-w-full md:max-w-2xl px-4 text-white/70 animate-fadeInUp animate-delay-300">
                Communicate naturally with TaskFlow using text, voice, or images. Our AI understands context and helps you stay productive.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12 lg:gap-16 items-center">
              {/* Left - Chat Interface Demo */}
              <div className="animate-fadeInLeft bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/50 rounded-3xl p-8 shadow-2xl shadow-brand-button/10">
                {/* Tabs */}
                <div className="flex gap-4 mb-8 pb-4 border-b border-brand-card-border/30">
                  {['text', 'voice', 'image'].map((tab, index) => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab as any)}
                      className={`px-6 py-3 rounded-xl border-0 font-semibold capitalize transition-all duration-300 relative overflow-hidden ${
                        activeTab === tab
                          ? 'bg-gradient-to-r from-brand-button to-brand-button-hover text-white shadow-lg shadow-brand-button/30'
                          : 'text-white/70 hover:text-brand-button'
                      }`}
                      style={{ animationDelay: `${index * 100}ms` }}
                    >
                      <span className="relative z-10">
                        {tab === 'text' && '💬'} {tab === 'voice' && '🎤'} {tab === 'image' && '🖼️'} {tab}
                      </span>
                      {activeTab === tab && (
                        <div className="absolute inset-0 bg-gradient-to-r from-brand-button/20 to-brand-button-hover/10 animate-pulse"></div>
                      )}
                    </button>
                  ))}
                </div>

                {/* Chat Messages */}
                <div className="flex flex-col gap-4 mb-6">
                  <div className="self-end bg-gradient-to-r from-brand-button to-brand-button-hover text-white p-4 rounded-2xl rounded-br-sm max-w-[80%] shadow-lg shadow-brand-button/20 animate-fadeInUp animate-delay-400">
                    Create a task for tomorrow's team meeting
                  </div>
                  <div className="self-start bg-brand-card-bg/50 backdrop-blur-sm text-white p-4 rounded-2xl rounded-bl-sm max-w-[80%] shadow-sm border border-brand-card-border/30 animate-fadeInUp animate-delay-500">
                    ✅ I've created "Team Meeting" scheduled for tomorrow at 10 AM. Would you like to add any specific agenda items?
                  </div>
                  <div className="self-end bg-gradient-to-r from-brand-button to-brand-button-hover text-white p-4 rounded-2xl rounded-br-sm max-w-[80%] shadow-lg shadow-brand-button/20 animate-fadeInUp animate-delay-600">
                    Yes, add "Q1 planning review" to the agenda
                  </div>
                  <div className="self-start bg-brand-card-bg/50 backdrop-blur-sm text-white p-4 rounded-2xl rounded-bl-sm max-w-[80%] shadow-sm border border-brand-card-border/30 animate-fadeInUp animate-delay-700">
                    ✅ Done! I've added "Q1 planning review" to tomorrow's team meeting agenda.
                  </div>
                </div>

                {/* Input */}
                <div className="mt-6 flex gap-4 items-center">
                  <input
                    type="text"
                    placeholder="Type your message..."
                    className="flex-1 px-6 py-4 bg-brand-bg/50 backdrop-blur-sm border-2 border-brand-card-border rounded-xl text-white placeholder-white/40 focus:outline-none focus:border-brand-button transition-all duration-300 hover:shadow-lg hover:shadow-brand-button/10"
                  />
                  <button className="px-6 py-4 bg-gradient-to-r from-brand-button to-brand-button-hover text-white font-semibold border-0 rounded-xl transition-all duration-300 hover:from-brand-button-hover hover:to-brand-button shadow-lg shadow-brand-button/30 hover:shadow-xl hover:shadow-brand-button/40 hover:-translate-y-0.5 transform hover-lift">
                    Send
                  </button>
                </div>
              </div>

              {/* Right - Features */}
              <div className="animate-fadeInRight">
                <div className="mb-12">
                  <h3 className="text-2xl md:text-3xl font-bold mb-4 md:mb-6 text-white animate-fadeInRight animate-delay-400">
                    Intelligent Conversations
                  </h3>
                  <p className="text-base md:text-lg mb-6 md:mb-8 text-white/70 leading-relaxed animate-fadeInRight animate-delay-500">
                    Our AI chatbot understands natural language and context. Ask questions, create tasks, update priorities, and get insights - all through simple conversation.
                  </p>
                </div>

                <div className="flex flex-col gap-6">
                  {[
                    {
                      icon: '🧠',
                      title: 'Context Awareness',
                      description: 'Remembers previous conversations and understands your workflow'
                    },
                    {
                      icon: '⚡',
                      title: 'Instant Actions',
                      description: 'Create, update, or complete tasks with a single message'
                    },
                    {
                      icon: '🎨',
                      title: 'Visual Understanding',
                      description: 'Upload screenshots or images for visual task creation'
                    },
                    {
                      icon: '🔊',
                      title: 'Voice Commands',
                      description: 'Speak naturally to manage your tasks hands-free'
                    }
                  ].map((item, index) => (
                    <div
                      key={index}
                      className="flex gap-4 items-start animate-fadeInRight group"
                      style={{ animationDelay: `${(index + 6) * 100}ms` }}
                    >
                      <div className="w-12 h-12 rounded-xl bg-brand-button/20 flex items-center justify-center text-xl flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                        {item.icon}
                      </div>
                      <div>
                        <h4 className="text-base md:text-lg font-bold mb-2 text-white group-hover:text-brand-button transition-colors duration-300">
                          {item.title}
                        </h4>
                        <p className="text-sm md:text-base text-white/70 leading-relaxed group-hover:text-white/90 transition-colors duration-300">
                          {item.description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="px-4 py-16 md:py-24 lg:py-32 bg-gradient-to-br from-brand-bg to-brand-chat/20 text-white text-center relative overflow-hidden">
          {/* Background elements */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
            <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-brand-button/10 rounded-full blur-2xl animate-pulse animate-infinite"></div>
            <div className="absolute bottom-1/3 right-1/4 w-72 h-72 bg-brand-button/10 rounded-full blur-2xl animate-pulse animate-delay-1000 animate-infinite"></div>

            {/* Floating particles */}
            {[...Array(10)].map((_, i) => (
              <div
                key={i}
                className="absolute rounded-full bg-brand-button/10 animate-float"
                style={{
                  width: `${Math.random() * 12 + 4}px`,
                  height: `${Math.random() * 12 + 4}px`,
                  top: `${Math.random() * 100}%`,
                  left: `${Math.random() * 100}%`,
                  animationDuration: `${Math.random() * 10 + 10}s`,
                  animationDelay: `${Math.random() * 5}s`
                }}
              ></div>
            ))}
          </div>

          <div className="max-w-[800px] mx-auto animate-fadeInUp px-4 relative z-10">
            <div className="inline-block px-4 py-1.5 bg-brand-button/20 rounded-full mb-6 border border-brand-button/30 animate-fadeInUp animate-delay-100">
              <span className="text-sm font-medium text-brand-button">Ready to get started?</span>
            </div>

            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 md:mb-6 animate-fadeInUp animate-delay-200">
              Ready to Transform Your Workflow?
            </h2>
            <p className="text-lg md:text-xl mb-8 md:mb-10 text-white/95 max-w-2xl mx-auto animate-fadeInUp animate-delay-300">
              Join thousands of teams already using TaskFlow to boost productivity with AI
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-stretch max-w-md mx-auto animate-fadeInUp animate-delay-400">
              <Link href="/signup" className="w-full">
                <button className="w-full min-h-[48px] hover-lift px-8 py-4 bg-gradient-to-r from-brand-button to-brand-button-hover text-white text-lg font-semibold border-0 rounded-xl transition-all duration-300 hover:shadow-xl hover:shadow-brand-button/30 hover:-translate-y-0.5 transform backdrop-blur-sm relative overflow-hidden group">
                  <span className="relative z-10">Start Free Trial</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-brand-button/20 to-brand-button-hover/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <div className="absolute -left-4 top-1/2 w-4 h-4 bg-white/30 rounded-full animate-ping"></div>
                  <div className="absolute -right-4 top-1/2 w-4 h-4 bg-white/30 rounded-full animate-ping animate-delay-500"></div>
                </button>
              </Link>
              <button className="w-full min-h-[48px] hover-lift px-8 py-4 bg-transparent text-white text-lg font-semibold border-2 border-brand-button rounded-xl transition-all duration-300 hover:bg-brand-button/10 hover:-translate-y-0.5 transform backdrop-blur-sm relative overflow-hidden group">
                <span className="relative z-10">Watch Demo</span>
                <div className="absolute inset-0 bg-gradient-to-r from-brand-button/10 to-brand-button/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>
            </div>

            <div className="mt-8 flex flex-wrap justify-center gap-6 text-sm text-white/60 animate-fadeInUp animate-delay-500">
              <div className="flex items-center group">
                <svg className="w-5 h-5 text-green-400 mr-2 group-hover:animate-bounce" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                No credit card required
              </div>
              <div className="flex items-center group">
                <svg className="w-5 h-5 text-green-400 mr-2 group-hover:animate-bounce animate-delay-200" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Free 14-day trial
              </div>
              <div className="flex items-center group">
                <svg className="w-5 h-5 text-green-400 mr-2 group-hover:animate-bounce animate-delay-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Cancel anytime
              </div>
            </div>

            {/* Social proof */}
            <div className="mt-12 grid grid-cols-3 gap-8 max-w-md mx-auto animate-fadeInUp animate-delay-600">
              <div className="text-center">
                <div className="text-2xl font-bold text-brand-button">99.9%</div>
                <div className="text-xs text-white/70">Uptime</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-brand-button">24/7</div>
                <div className="text-xs text-white/70">Support</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-brand-button">10K+</div>
                <div className="text-xs text-white/70">Users</div>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="px-4 py-12 md:py-16 lg:px-12 bg-brand-bg text-white relative overflow-hidden">
          {/* Background elements */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
            <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-brand-button/5 rounded-full blur-2xl animate-pulse animate-infinite"></div>
            <div className="absolute bottom-1/3 right-1/4 w-72 h-72 bg-brand-button/5 rounded-full blur-2xl animate-pulse animate-delay-1000 animate-infinite"></div>

            {/* Floating particles */}
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className="absolute rounded-full bg-brand-button/10 animate-float"
                style={{
                  width: `${Math.random() * 10 + 5}px`,
                  height: `${Math.random() * 10 + 5}px`,
                  top: `${Math.random() * 100}%`,
                  left: `${Math.random() * 100}%`,
                  animationDuration: `${Math.random() * 10 + 10}s`,
                  animationDelay: `${Math.random() * 5}s`
                }}
              ></div>
            ))}
          </div>

          <div className="max-w-[1400px] mx-auto relative z-10">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 md:gap-12 mb-12">
              <div className="animate-fadeInUp animate-delay-100">
                <div className="text-xl md:text-2xl font-bold mb-4 flex items-center group">
                  <div className="w-8 h-8 bg-gradient-to-br from-brand-button to-brand-button-hover rounded-lg flex items-center justify-center mr-3 group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                      <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  TaskFlow
                </div>
                <p className="text-sm md:text-base text-white/70 leading-relaxed group-hover:text-white/90 transition-colors duration-300">
                  The only project management platform designed for the Agent Era.
                </p>

                <div className="flex space-x-4 mt-6">
                  <a href="#" className="text-white/60 hover:text-brand-button transition-colors duration-300 group">
                    <svg className="w-5 h-5 group-hover:scale-125 transition-transform duration-300" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.283 3.949 4.725-.445.12-.927.184-1.425.184-.29 0-.585-.027-.87-.08a6.585 6.585 0 0 1-1.085-.24 6.747 6.747 0 0 1-1.02-.41c.17 1.04.52 2.01 1.02 2.86 1.12 2.62 3.49 4.42 6.07 4.46-.43.11-.88.17-1.35.17-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16.0 21 20.32 14.78 20.32 9.64c0-.44-.01-.88-.03-1.32.87-.63 1.62-1.43 2.19-2.34z"/>
                    </svg>
                  </a>
                  <a href="#" className="text-white/60 hover:text-brand-button transition-colors duration-300 group">
                    <svg className="w-5 h-5 group-hover:scale-125 transition-transform duration-300" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16.04 21 20.32 14.78 20.32 9.64c0-.44-.01-.88-.03-1.32.87-.63 1.62-1.43 2.19-2.34z"/>
                    </svg>
                  </a>
                  <a href="#" className="text-white/60 hover:text-brand-button transition-colors duration-300 group">
                    <svg className="w-5 h-5 group-hover:scale-125 transition-transform duration-300" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                  </a>
                </div>
              </div>

              <div className="animate-fadeInUp animate-delay-200">
                <h4 className="text-base md:text-lg font-bold mb-4 group">Product</h4>
                <div className="flex flex-col gap-3">
                  <a href="#features" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">Features</a>
                  <a href="#how-it-works" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">How it works</a>
                  <a href="#chatbot" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">AI Chatbot</a>
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">Pricing</a>
                </div>
              </div>

              <div className="animate-fadeInUp animate-delay-300">
                <h4 className="text-base md:text-lg font-bold mb-4 group">Company</h4>
                <div className="flex flex-col gap-3">
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">About Us</a>
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">Careers</a>
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">Blog</a>
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">Contact</a>
                </div>
              </div>

              <div className="animate-fadeInUp animate-delay-400">
                <h4 className="text-base md:text-lg font-bold mb-4 group">Legal</h4>
                <div className="flex flex-col gap-3">
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">Privacy Policy</a>
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">Terms of Service</a>
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">Security</a>
                  <a href="#" className="text-white/70 hover:text-brand-button transition-colors duration-300 group-hover:translate-x-2">GDPR</a>
                </div>
              </div>
            </div>

            <div className="border-t border-brand-card-border pt-8 md:pt-12 text-center animate-fadeInUp animate-delay-500">
              <p className="text-sm md:text-base text-white/70">
                © 2025 TaskFlow Intelligence Platform. All rights reserved.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}

export default Home

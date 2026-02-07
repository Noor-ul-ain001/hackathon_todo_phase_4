import Head from 'next/head'
import { useState } from 'react'

export default function Help() {
  const [activeTab, setActiveTab] = useState('faq')
  const [expandedArticle, setExpandedArticle] = useState(null)

  const faqs = [
    {
      id: 1,
      question: "How do I create a new task?",
      answer: "You can create a new task by clicking the 'Add Task' button in the dashboard or by using the AI chat assistant. Simply type a command like 'Add task: Review documentation' and the AI will create the task for you."
    },
    {
      id: 2,
      question: "Can I set due dates for tasks?",
      answer: "Yes, you can set due dates when creating or editing tasks. The AI assistant can also parse natural language to set due dates, for example: 'Add task: Submit report due tomorrow'."
    },
    {
      id: 3,
      question: "How do I mark a task as complete?",
      answer: "You can mark a task as complete by clicking the checkbox next to the task in the dashboard, or by using the AI chat assistant with commands like 'Complete task #3' or 'Mark task Review documentation as done'."
    },
    {
      id: 4,
      question: "Can I collaborate with others on tasks?",
      answer: "Yes, TaskFlow supports team collaboration. You can assign tasks to team members, add comments, and track progress together. Create a project to start collaborating with your team."
    },
    {
      id: 5,
      question: "How do I change my notification settings?",
      answer: "You can change your notification settings in the Settings page. Navigate to Settings > Notifications to customize email, push, and SMS notifications."
    }
  ]

  const articles = [
    {
      id: 1,
      title: "Getting Started with TaskFlow",
      category: "Beginner",
      readTime: "5 min read",
      content: "Welcome to TaskFlow! This guide will help you get started with our AI-powered task management platform. First, create your account and set up your profile. Then, start by creating your first project and adding tasks using natural language commands through our AI assistant."
    },
    {
      id: 2,
      title: "Using the AI Assistant",
      category: "Advanced",
      readTime: "8 min read",
      content: "Our AI assistant understands natural language commands to manage your tasks. You can say things like 'Add task: Review code by Friday', 'Show me all pending tasks', or 'Mark task 5 as complete'. The assistant will interpret your commands and execute the appropriate actions."
    },
    {
      id: 3,
      title: "Project Management Best Practices",
      category: "Intermediate",
      readTime: "10 min read",
      content: "Effective project management starts with clear goals and well-defined tasks. Break down large projects into smaller, actionable tasks. Set realistic deadlines and prioritize tasks based on importance and urgency. Use our analytics dashboard to track your progress and productivity."
    },
    {
      id: 4,
      title: "Collaborating with Your Team",
      category: "Intermediate",
      readTime: "7 min read",
      content: "TaskFlow makes team collaboration easy. Create shared projects, assign tasks to team members, and track progress together. Use the comment feature to communicate about specific tasks. Set up notifications to stay updated on project changes."
    }
  ]

  const handleArticleToggle = (id) => {
    setExpandedArticle(expandedArticle === id ? null : id)
  }

  return (
    <>
      <Head>
        <title>Help Center - TaskFlow</title>
        <meta name="description" content="TaskFlow Help Center" />
      </Head>

      {/* Header */}
      <div className="bg-brand-card-bg/80 backdrop-blur-sm border-b border-brand-card-border px-4 py-3 md:px-8 md:py-6 animate-fadeInDown">
        <h1 className="text-3xl font-bold text-white mb-1">
          <span className="bg-gradient-to-r from-brand-button to-brand-button-hover bg-clip-text text-transparent">Help Center</span>
        </h1>
        <p className="text-white/70 text-sm">Find answers to your questions</p>
      </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-4 py-3 md:px-8 md:py-6">
          <div className="max-w-4xl mx-auto">
            {/* Help Tabs */}
            <div className="flex space-x-8 mb-8 border-b border-brand-card-border/50">
              {['faq', 'articles', 'contact'].map((tab, index) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`pb-4 px-1 capitalize font-semibold transition-all animate-fadeInDown ${
                    activeTab === tab
                      ? 'text-brand-button border-b-2 border-brand-button'
                      : 'text-white/70 hover:text-brand-button'
                  }`}
                  style={{animationDelay: `${index * 0.1}s`}}
                >
                  {tab === 'faq' ? 'FAQ' : tab === 'articles' ? 'Knowledge Base' : 'Contact Support'}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all animate-fadeInUp">
              {activeTab === 'faq' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Frequently Asked Questions</h2>
                  <div className="space-y-4">
                    {faqs.map((faq, index) => (
                      <div key={faq.id} className="border-b border-brand-card-border/30 pb-4 last:border-0 animate-fadeInLeft" style={{animationDelay: `${index * 0.1}s`}}>
                        <h3 className="text-lg font-semibold text-white mb-2">{faq.question}</h3>
                        <p className="text-white/70">{faq.answer}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'articles' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Knowledge Base Articles</h2>
                  <div className="space-y-6">
                    {articles.map((article, index) => (
                      <div key={article.id} className="border-b border-brand-card-border/30 pb-6 last:border-0 animate-fadeInLeft" style={{animationDelay: `${index * 0.1}s`}}>
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="text-lg font-semibold text-white mb-2">{article.title}</h3>
                            <div className="flex items-center space-x-4 text-sm text-white/60">
                              <span>{article.category}</span>
                              <span>•</span>
                              <span>{article.readTime}</span>
                            </div>
                          </div>
                          <button
                            onClick={() => handleArticleToggle(article.id)}
                            className="text-brand-button hover:text-brand-button-hover text-sm font-semibold transition-colors"
                          >
                            {expandedArticle === article.id ? 'Show Less' : 'Read More'}
                          </button>
                        </div>
                        {expandedArticle === article.id && (
                          <div className="mt-4 pt-4 border-t border-brand-card-border/30">
                            <p className="text-white/70">{article.content}</p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'contact' && (
                <div>
                  <h2 className="text-xl font-bold text-white mb-6">Contact Support</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/50 rounded-xl p-6 hover-lift transition-all animate-fadeInUp">
                      <div className="w-12 h-12 bg-brand-button/20 rounded-lg flex items-center justify-center mb-4 shadow-md">
                        <svg className="w-6 h-6 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <h3 className="text-lg font-semibold text-white mb-2">Email Support</h3>
                      <p className="text-white/70 mb-4">Send us an email and we'll respond within 24 hours.</p>
                      <a href="mailto:support@taskflow.example.com" className="text-brand-button hover:text-brand-button-hover font-semibold transition-colors">
                        support@taskflow.example.com
                      </a>
                    </div>

                    <div className="bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/50 rounded-xl p-6 hover-lift transition-all animate-fadeInUp animate-delay-100">
                      <div className="w-12 h-12 bg-brand-button/20 rounded-lg flex items-center justify-center mb-4 shadow-md">
                        <svg className="w-6 h-6 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                        </svg>
                      </div>
                      <h3 className="text-lg font-semibold text-white mb-2">Chat with Us</h3>
                      <p className="text-white/70 mb-4">Chat with our support team in real-time during business hours.</p>
                      <button className="text-brand-button hover:text-brand-button-hover font-semibold transition-colors">
                        Start Chat
                      </button>
                    </div>

                    <div className="bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/50 rounded-xl p-6 hover-lift transition-all animate-fadeInUp animate-delay-200">
                      <div className="w-12 h-12 bg-brand-button/20 rounded-lg flex items-center justify-center mb-4 shadow-md">
                        <svg className="w-6 h-6 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <h3 className="text-lg font-semibold text-white mb-2">Documentation</h3>
                      <p className="text-white/70 mb-4">Browse our comprehensive documentation for detailed guides.</p>
                      <a href="#" className="text-brand-button hover:text-brand-button-hover font-semibold transition-colors">
                        View Documentation
                      </a>
                    </div>

                    <div className="bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/50 rounded-xl p-6 hover-lift transition-all animate-fadeInUp animate-delay-300">
                      <div className="w-12 h-12 bg-brand-button/20 rounded-lg flex items-center justify-center mb-4 shadow-md">
                        <svg className="w-6 h-6 text-brand-button" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      </div>
                      <h3 className="text-lg font-semibold text-white mb-2">Community Forum</h3>
                      <p className="text-white/70 mb-4">Connect with other users and find solutions in our community forum.</p>
                      <a href="#" className="text-brand-button hover:text-brand-button-hover font-semibold transition-colors">
                        Visit Forum
                      </a>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
    </>
  )
}
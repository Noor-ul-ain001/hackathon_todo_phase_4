# TaskFlow UI - Updated Design

## Overview
The UI has been completely updated to match the TaskFlow Intelligence Platform design with full integration of the app's AI-powered task management features.

## Color Scheme
- **Primary Background**: Navy 900 (#0f172a)
- **Secondary Background**: Navy 800/950 (#1e293b)
- **Accent Color**: Cyan 400 (#22d3ee)
- **CTA Buttons**: Cream 100 (#fef3c7)
- **Text**: White with navy variants for hierarchy

## Pages

### 1. Landing Page (`/` or `/landing`)
**Features:**
- Hero section with TaskFlow branding
- Feature cards (Organization, Projects, Recursive Tasks)
- Tenant preview mockup
- Call-to-action buttons
- Navigation to dashboard

**Design Elements:**
- Dark navy gradient background
- Cyan accent highlights
- Glassmorphism effects
- Responsive grid layout

### 2. Dashboard Page (`/dashboard`)
**Features:**
- **Header**: Welcome message with dynamic task counts
- **Statistics Cards**:
  - Total Tasks
  - Active Tasks (pending + in_progress)
  - Pending Tasks
  - Completed Tasks
- **Task List**:
  - Filterable by status (all, pending, in_progress, completed)
  - Shows task title, description, status, priority, due date
  - Hover effects for editing
  - Empty state with CTA
- **System Logs**: Live event stream showing recent task activity
- **AI Chat Modal**: Natural language task management interface

**Functional Components:**
- Real-time task statistics
- Task filtering
- AI chat integration
- Image upload support
- Conversation history
- Auto-refresh on task changes

## Key Features

### AI Chat Assistant
- **Trigger**: Click "AI Assistant" button or chat icon in sidebar
- **Capabilities**:
  - Create tasks: "Add task: Review PR"
  - List tasks: "Show pending tasks"
  - Update tasks: "Update task #1"
  - Complete tasks: "Complete task #5"
  - Image analysis: Upload images for context
- **Features**:
  - Natural language processing
  - Multi-modal support (text, image)
  - Conversation history
  - Quick command suggestions
  - Tasks affected tracking

### Navigation
- **Left Sidebar**:
  - Home (Dashboard)
  - Analytics
  - Tasks
  - Team
  - AI Chat (with message counter)
  - Settings
- **Logo**: Links back to landing page

### Task Management
- **View**: List with status badges and priority indicators
- **Filter**: By status (all/pending/in_progress/completed)
- **Create**: Via AI chat or "Add Task" button
- **Update**: Click edit icon on task card
- **Stats**: Auto-calculated from task list

### System Logs
- Real-time activity feed
- Color-coded by status:
  - Green: Completed
  - Cyan: In Progress
  - Gray: Pending
- Shows last 6 tasks

## Backend Integration

### API Endpoints Used
- `POST /api/{user_id}/chat`: Main chat endpoint
  - Handles all task operations through natural language
  - Supports text and image modalities
  - Returns conversation_id and tasks_affected

### Data Flow
1. User sends command via chat
2. Backend processes through AI agents
3. Returns response with affected task IDs
4. Frontend refreshes task list if tasks were modified
5. Updates statistics automatically

## Running the App

1. **Start Backend**:
   ```bash
   cd backend
   python -m uvicorn backend.src.main:app --reload
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access**:
   - Landing: http://localhost:3001
   - Dashboard: http://localhost:3001/dashboard

## Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Design System

### Typography
- **Headings**: Bold, white
- **Subheadings**: Semi-bold, cyan-400
- **Body**: Regular, navy-300/400
- **Labels**: Uppercase, tracking-wider, navy-400

### Components
- **Cards**: Rounded-2xl, border navy-700, bg navy-800/50
- **Buttons**:
  - Primary: bg-cyan-400, text-navy-900
  - Secondary: border-cyan-400, text-cyan-400
  - Ghost: text-navy-400, hover:text-white
- **Inputs**: Rounded-xl, border-navy-600, bg-navy-900
- **Badges**: Rounded-full, color-500/20 background

### Responsive Design
- Mobile-first approach
- Grid layouts adapt to screen size
- Sidebar collapses on mobile (future enhancement)
- Modal is fullscreen on small devices

## Future Enhancements
1. Add real-time WebSocket updates for system logs
2. Implement drag-and-drop task reordering
3. Add task due date picker in UI
4. Voice input support
5. Dark/Light theme toggle
6. Mobile-optimized sidebar
7. Task search functionality
8. Batch task operations
9. Task categories/projects view
10. Analytics dashboard with charts

## Tech Stack
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **State**: React Hooks
- **API**: Fetch API
- **Icons**: Heroicons (via inline SVG)

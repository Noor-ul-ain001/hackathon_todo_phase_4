# 📋 How to Use Dashboard UI - TaskFlow

## 🌐 Access Dashboard
Visit: **http://localhost:3004/dashboard**

---

## ✨ Dashboard Features

### **1. View Tasks**
- See all your tasks at a glance
- Color-coded status badges:
  - 🟢 **Green** = Completed
  - 🔵 **Teal** = In Progress
  - ⚪ **Gray** = Pending
- Priority indicators:
  - 🔴 **Red** = High Priority
  - 🟡 **Yellow** = Medium Priority
  - 🔵 **Blue** = Low Priority

### **2. Filter Tasks**
Use the dropdown menu to filter by status:
- **All Tasks** - Show everything
- **Pending** - Only pending tasks
- **In Progress** - Tasks currently being worked on
- **Completed** - Finished tasks

### **3. Statistics Overview**
Top cards show real-time metrics:
- **Total Tasks** - All tasks count
- **Active** - Pending + In Progress
- **Pending** - Tasks not started
- **Completed** - Finished tasks

---

## 🤖 AI Assistant - Task Management

Click the **"AI Assistant"** button to open the chat modal.

### **Create Tasks**
```
✓ "Add task: Review PR"
✓ "Create task: Buy groceries"
✓ "New task: Meeting at 3pm"
```

### **List Tasks**
```
✓ "Show my tasks"
✓ "List all tasks"
✓ "Get my tasks"
```

### **Update Tasks**

#### Change Priority:
```
✓ "Update task 8 to high priority"
✓ "Change task 5 to low priority"
✓ "Make task 3 urgent"
```

#### Change Status:
```
✓ "Change task 6 status to in progress"
✓ "Mark task 2 as in progress"
✓ "Update task 4 status to pending"
```

#### Update Multiple Properties:
```
✓ "Update task 7 to high priority and mark as in progress"
```

### **Complete Tasks**
```
✓ "Complete task 5"
✓ "Mark task 10 as done"
✓ "Finish task 3"
```

### **Delete Tasks**
```
✓ "Delete task 8"
✓ "Remove task #12"
✓ "Delete 5"
```

---

## 🖱️ Quick Actions

### **Edit Button (Hover)**
- Hover over any task card
- Click the **pencil icon** that appears
- Opens AI Assistant with pre-filled update command
- Modify the command and send

### **Add Task Button**
- Click **"+ ADD TASK"** in the tasks section
- Opens AI Assistant
- Type your task and send

### **New Project Button**
- Click **"New Project"** at the top
- Opens AI Assistant with "Create a new project" pre-filled
- Customize and send

---

## 📊 System Logs
Right side panel shows:
- Recent task activities
- Real-time status updates
- Color-coded events

---

## 💡 Pro Tips

### **Natural Language**
The AI understands natural language, so you can say:
- "Set task 5 to urgent"
- "I'm working on task 3"
- "Task 8 is done"

### **Task IDs**
- Every task has an ID number
- Use "Show my tasks" to see IDs
- Reference tasks by ID for updates/completion/deletion

### **Status Values**
- `pending` - Not started
- `in_progress` - Currently working
- `completed` - Finished

### **Priority Values**
- `low` - Low priority
- `medium` - Medium priority
- `high` - High/Urgent priority

---

## 🔄 Task Workflow Example

```bash
# 1. Create a task
User: "Add task: Write documentation"
AI: ✓ Task created successfully: 'Write documentation' (ID: 15)

# 2. Start working on it
User: "Change task 15 status to in progress"
AI: ✓ Task updated: 'Write documentation' (ID: 15)

# 3. Make it high priority
User: "Update task 15 to high priority"
AI: ✓ Task updated: 'Write documentation' (ID: 15)

# 4. Complete it
User: "Complete task 15"
AI: ✓ Task completed: 'Write documentation' (ID: 15)

# 5. Review all tasks
User: "Show my tasks"
AI: Here are your tasks: [list of tasks with IDs and statuses]
```

---

## 🎨 UI Features

### **Responsive Design**
- Works on desktop and tablet
- Smooth animations
- Hover effects on cards

### **Real-time Updates**
- Tasks refresh after each operation
- Statistics update automatically
- System logs update in real-time

### **Color-coded Interface**
- Teal/Cyan theme for active elements
- Status-based coloring
- Priority-based badges

---

## 🚀 Quick Start Guide

1. **Open Dashboard**: http://localhost:3004/dashboard
2. **Click "AI Assistant"** button
3. **Type**: "Add task: My first task"
4. **Press Send**
5. **View** your new task in the list
6. **Update** by clicking the edit icon or using AI commands

---

## 📝 Examples

### Complete Workflow:
```
1. "Add task: Review code"          → Creates task (e.g., ID: 20)
2. "Show my tasks"                   → Lists all tasks with IDs
3. "Update task 20 to high priority" → Sets priority to high
4. "Change task 20 to in progress"   → Updates status
5. "Complete task 20"                → Marks as completed
```

### Multiple Tasks:
```
"Add task: Morning meeting"
"Add task: Respond to emails"
"Add task: Code review"
"Show my tasks"
"Update task 21 to high priority"
"Complete task 22"
```

---

## ❓ Need Help?

Type in AI Assistant:
- "help" - Get general guidance
- Any unclear command - AI will provide examples

---

**🎉 You're ready to manage tasks efficiently with TaskFlow!**

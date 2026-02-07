import React, { useState } from 'react';
import TodoDetail from './TodoDetail';

const TodoSummary = ({ tasks, isLoading = false, onRefresh }) => {
  const [selectedTask, setSelectedTask] = useState(null);

  if (isLoading) {
    return (
      <div className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-2xl shadow-lg shadow-black/20 p-4 mb-3 animate-pulse">
        <div className="flex justify-between items-center mb-3">
          <h4 className="font-bold text-white">Task Summary</h4>
          <div className="w-20 h-4 bg-gray-700/60 rounded"></div>
        </div>
        <div className="space-y-2">
          <div className="h-3 bg-gray-700/60 rounded"></div>
          <div className="h-3 bg-gray-700/60 rounded w-5/6"></div>
          <div className="h-3 bg-gray-700/60 rounded w-4/6"></div>
        </div>
      </div>
    );
  }

  if (!tasks || tasks.length === 0) {
    return (
      <div className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-2xl shadow-lg shadow-black/20 p-4 mb-3">
        <div className="flex justify-between items-center mb-2">
          <h4 className="font-bold text-white">Task Summary</h4>
          {onRefresh && (
            <button
              onClick={onRefresh}
              className="text-xs bg-gray-700/50 hover:bg-gray-600/50 text-gray-300 px-2 py-1 rounded transition-colors"
            >
              Refresh
            </button>
          )}
        </div>
        <p className="text-gray-400 text-sm">No tasks found. Create your first task to get started!</p>
      </div>
    );
  }

  // Calculate task statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.status === 'completed').length;
  const pendingTasks = tasks.filter(task => task.status === 'pending').length;
  const inProgressTasks = tasks.filter(task => task.status === 'in_progress').length;
  const highPriorityTasks = tasks.filter(task => task.priority === 'high').length;

  // Sort tasks by updated_at in descending order to show most recent first
  const sortedTasks = [...tasks].sort((a, b) =>
    new Date(b.updated_at) - new Date(a.updated_at)
  );

  // Get the most recent tasks
  const recentTasks = sortedTasks.slice(0, 5);

  return (
    <div className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-2xl shadow-lg shadow-black/20 p-4 mb-3">
      <div className="flex justify-between items-center mb-3">
        <h4 className="font-bold text-white">Task Summary</h4>
        {onRefresh && (
          <button
            onClick={onRefresh}
            className="text-xs bg-gray-700/50 hover:bg-gray-600/50 text-gray-300 px-2 py-1 rounded transition-colors"
          >
            Refresh
          </button>
        )}
      </div>

      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="bg-gray-700/50 rounded-lg p-2">
          <p className="text-xs text-gray-400">Total</p>
          <p className="text-lg font-bold text-white">{totalTasks}</p>
        </div>
        <div className="bg-gray-700/50 rounded-lg p-2">
          <p className="text-xs text-gray-400">Completed</p>
          <p className="text-lg font-bold text-green-400">{completedTasks}</p>
        </div>
        <div className="bg-gray-700/50 rounded-lg p-2">
          <p className="text-xs text-gray-400">Pending</p>
          <p className="text-lg font-bold text-amber-400">{pendingTasks}</p>
        </div>
        <div className="bg-gray-700/50 rounded-lg p-2">
          <p className="text-xs text-gray-400">High Priority</p>
          <p className="text-lg font-bold text-red-400">{highPriorityTasks}</p>
        </div>
      </div>

      {pendingTasks > 0 && (
        <div className="mt-3">
          <h5 className="font-semibold text-gray-300 text-sm mb-2">Pending Tasks:</h5>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {tasks
              .filter(task => task.status === 'pending')
              .slice(0, 5) // Show only first 5 pending tasks
              .map(task => (
                <div
                  key={task.id}
                  className="flex justify-between text-sm cursor-pointer hover:bg-gray-700/30 rounded p-1 transition-colors"
                  onClick={() => setSelectedTask(task)}
                >
                  <span className="text-gray-300 truncate max-w-[70%]">{task.title}</span>
                  {task.priority === 'high' && (
                    <span className="text-red-400 font-semibold">HIGH</span>
                  )}
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Recent Activity Section */}
      {recentTasks.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-700/50">
          <h5 className="font-semibold text-gray-300 text-sm mb-2">Recent Activity</h5>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {recentTasks.map(task => {
              const statusDisplay = task.status === 'completed' ? 'completed' :
                                  task.status === 'in_progress' ? 'in progress' : 'pending';

              return (
                <div
                  key={`recent-${task.id}`}
                  className="text-xs cursor-pointer hover:bg-gray-700/30 rounded p-1 transition-colors"
                  onClick={() => setSelectedTask(task)}
                >
                  <div className="flex justify-between">
                    <span className="text-gray-300 truncate max-w-[70%]">{task.title}</span>
                    <span className={`font-medium ${
                      task.status === 'completed' ? 'text-green-400' :
                      task.status === 'in_progress' ? 'text-amber-400' :
                      'text-blue-400'
                    }`}>
                      {statusDisplay}
                    </span>
                  </div>
                  <div className="text-gray-500 mt-1">
                    Updated: {new Date(task.updated_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Task Detail Modal */}
      {selectedTask && (
        <TodoDetail
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
        />
      )}
    </div>
  );
};

export default TodoSummary;
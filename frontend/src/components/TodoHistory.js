import React from 'react';

const TodoHistory = ({ tasks, maxItems = 5 }) => {
  // Sort tasks by updated_at in descending order to show most recent first
  const sortedTasks = [...tasks].sort((a, b) => 
    new Date(b.updated_at) - new Date(a.updated_at)
  );

  // Get the most recent tasks
  const recentTasks = sortedTasks.slice(0, maxItems);

  if (recentTasks.length === 0) {
    return (
      <div className="bg-brand-bg/30 backdrop-blur-md border border-brand-button/5 rounded-xl p-3 mb-3">
        <h4 className="font-semibold text-white/80 text-sm mb-2">Recent Activity</h4>
        <p className="text-xs text-white/60">No recent task activity</p>
      </div>
    );
  }

  return (
    <div className="bg-brand-bg/30 backdrop-blur-md border border-brand-button/5 rounded-xl p-3 mb-3">
      <h4 className="font-semibold text-white/80 text-sm mb-2">Recent Activity</h4>
      <div className="space-y-2">
        {recentTasks.map(task => {
          const statusDisplay = task.status === 'completed' ? 'completed' : 
                              task.status === 'in_progress' ? 'in progress' : 'pending';
          
          return (
            <div key={task.id} className="text-xs">
              <div className="flex justify-between">
                <span className="text-white/90 truncate max-w-[70%]">{task.title}</span>
                <span className={`font-medium ${
                  task.status === 'completed' ? 'text-green-400' : 
                  task.status === 'in_progress' ? 'text-amber-400' : 
                  'text-blue-400'
                }`}>
                  {statusDisplay}
                </span>
              </div>
              <div className="text-white/50 mt-1">
                Updated: {new Date(task.updated_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TodoHistory;
import React from 'react';

const TodoDetail = ({ task, onClose }) => {
  if (!task) return null;

  const statusColors = {
    pending: 'bg-gray-700/50 text-gray-300',
    in_progress: 'bg-gray-600/50 text-amber-400',
    completed: 'bg-green-900/30 text-green-400'
  };

  const priorityColors = {
    low: 'bg-blue-900/30 text-blue-400',
    medium: 'bg-yellow-900/30 text-yellow-400',
    high: 'bg-red-900/30 text-red-400'
  };

  return (
    <div className="fixed inset-0 bg-gray-900/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeIn">
      <div className="bg-gray-800 border-2 border-gray-700 rounded-2xl w-full max-w-md flex flex-col shadow-2xl shadow-gray-900/50 animate-scaleIn">
        {/* Modal Header */}
        <div className="flex items-center justify-between p-4 md:p-6 border-b border-gray-700">
          <h2 className="text-xl font-bold text-white">Task Details</h2>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-gray-700/50 backdrop-blur-sm border border-gray-600 hover:bg-gray-600/50 flex items-center justify-center transition-all duration-300 hover:scale-110"
          >
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Task Content */}
        <div className="p-6 space-y-4">
          <div>
            <h3 className="text-lg font-bold text-white mb-1">{task.title}</h3>
            {task.description && (
              <p className="text-gray-300">{task.description}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wider">Status</p>
              <span className={`text-xs px-2 py-1 rounded-full font-medium mt-1 inline-block ${statusColors[task.status]}`}>
                {task.status.replace('_', ' ')}
              </span>
            </div>

            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wider">Priority</p>
              {task.priority && (
                <span className={`text-xs px-2 py-1 rounded-full font-medium mt-1 inline-block ${priorityColors[task.priority]}`}>
                  {task.priority}
                </span>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wider">Created</p>
              <p className="text-sm text-gray-300">
                {new Date(task.created_at).toLocaleDateString()}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wider">Updated</p>
              <p className="text-sm text-gray-300">
                {new Date(task.updated_at).toLocaleDateString()}
              </p>
            </div>
          </div>

          {task.due_date && (
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wider">Due Date</p>
              <p className="text-sm text-gray-300">
                {new Date(task.due_date).toLocaleDateString()}
              </p>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-gray-700 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors duration-300"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default TodoDetail;
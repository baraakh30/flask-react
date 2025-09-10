const React = require('react');

function UserList(props) {
  // Get props from Flask app
  const { users = [], current_user = {}, can_edit = false, page_title = "User List" } = props;
  
  // Inline CSS styles with Tailwind-like classes
  const styles = `
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
      
      .min-h-screen { min-height: 100vh; }          React.createElement('div', { className: 'flex justify-between items-start' },
            React.createElement('div', null,
              React.createElement('h1', { className: 'text-4xl font-bold mb-2 flex items-center' }, 
                React.createElement('span', { className: 'mr-3' }, '👥'),
                page_title
              ),
              React.createElement('p', { className: 'text-blue-100 text-lg' }, 
                'User management system built with Flask-React - Server-Side Rendering'
              )
            ),
            current_user.name && React.createElement('div', { className: 'text-right' },
              React.createElement('p', { className: 'text-blue-100' }, 'Logged in as:'),
              React.createElement('p', { className: 'text-white font-semibold' }, current_user.name || 'Unknown'),
              React.createElement('span', { 
                className: 'inline-block px-2 py-1 text-xs rounded-full mt-1 ' + (
                  current_user.role === 'admin' ? 'bg-purple-200 text-purple-900' : 'bg-blue-200 text-blue-900'
                )
              }, (current_user.role || 'user').charAt(0).toUpperCase() + (current_user.role || 'user').slice(1))
            )
          ) .bg-gray-50 { background-color: #f9fafb; }
      .bg-white { background-color: white; }
      .bg-gradient-to-r { background-image: linear-gradient(to right, var(--tw-gradient-stops)); }
      .from-blue-600 { --tw-gradient-from: #2563eb; --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(37, 99, 235, 0)); }
      .to-purple-700 { --tw-gradient-to: #7c3aed; }
      .from-indigo-50 { --tw-gradient-from: #eef2ff; }
      .via-white { --tw-gradient-stops: var(--tw-gradient-from), white, var(--tw-gradient-to, rgba(255, 255, 255, 0)); }
      .to-cyan-50 { --tw-gradient-to: #ecfeff; }
      .from-green-50 { --tw-gradient-from: #f0fdf4; }
      .to-emerald-50 { --tw-gradient-to: #ecfdf5; }
      .from-white { --tw-gradient-from: white; }
      .to-blue-50 { --tw-gradient-to: #eff6ff; }
      
      .text-white { color: white; }
      .text-gray-800 { color: #1f2937; }
      .text-gray-600 { color: #4b5563; }
      .text-gray-500 { color: #6b7280; }
      .text-blue-100 { color: #dbeafe; }
      .text-red-800 { color: #991b1b; }
      .text-yellow-800 { color: #92400e; }
      .text-green-800 { color: #166534; }
      .text-blue-600 { color: #2563eb; }
      .text-green-600 { color: #16a34a; }
      .text-orange-600 { color: #ea580c; }
      .text-purple-600 { color: #9333ea; }
      
      .p-6 { padding: 1.5rem; }
      .p-4 { padding: 1rem; }
      .p-5 { padding: 1.25rem; }
      .px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
      .py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
      .px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
      .px-4 { padding-left: 1rem; padding-right: 1rem; }
      .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
      
      .mb-2 { margin-bottom: 0.5rem; }
      .mb-3 { margin-bottom: 0.75rem; }
      .mb-4 { margin-bottom: 1rem; }
      .mb-6 { margin-bottom: 1.5rem; }
      .mb-8 { margin-bottom: 2rem; }
      .mt-1 { margin-top: 0.25rem; }
      .mt-2 { margin-top: 0.5rem; }
      .mt-12 { margin-top: 3rem; }
      .mr-1 { margin-right: 0.25rem; }
      .mr-2 { margin-right: 0.5rem; }
      .mr-3 { margin-right: 0.75rem; }
      
      .flex { display: flex; }
      .items-center { align-items: center; }
      .items-start { align-items: flex-start; }
      .justify-between { justify-content: space-between; }
      .justify-center { justify-content: center; }
      .space-x-1 > * + * { margin-left: 0.25rem; }
      .space-x-2 > * + * { margin-left: 0.5rem; }
      .space-x-3 > * + * { margin-left: 0.75rem; }
      .space-x-4 > * + * { margin-left: 1rem; }
      .space-y-3 > * + * { margin-top: 0.75rem; }
      .space-y-4 > * + * { margin-top: 1rem; }
      .flex-1 { flex: 1 1 0%; }
      
      .grid { display: grid; }
      .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
      .grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .gap-4 { gap: 1rem; }
      .gap-6 { gap: 1.5rem; }
      .gap-8 { gap: 2rem; }
      
      @media (min-width: 768px) {
        .md\\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
        .md\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      }
      
      @media (min-width: 1024px) {
        .lg\\:col-span-2 { grid-column: span 2 / span 2; }
        .lg\\:col-span-1 { grid-column: span 1 / span 1; }
        .lg\\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      }
      
      .max-w-7xl { max-width: 80rem; }
      .mx-auto { margin-left: auto; margin-right: auto; }
      
      .text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
      .text-2xl { font-size: 1.5rem; line-height: 2rem; }
      .text-xl { font-size: 1.25rem; line-height: 1.75rem; }
      .text-lg { font-size: 1.125rem; line-height: 1.75rem; }
      .text-sm { font-size: 0.875rem; line-height: 1.25rem; }
      .text-xs { font-size: 0.75rem; line-height: 1rem; }
      
      .font-bold { font-weight: 700; }
      .font-semibold { font-weight: 600; }
      .font-medium { font-weight: 500; }
      
      .rounded-xl { border-radius: 0.75rem; }
      .rounded-2xl { border-radius: 1rem; }
      .rounded-lg { border-radius: 0.5rem; }
      .rounded-full { border-radius: 9999px; }
      
      .border { border-width: 1px; }
      .border-2 { border-width: 2px; }
      .border-l-4 { border-left-width: 4px; }
      .border-gray-200 { border-color: #e5e7eb; }
      .border-blue-200 { border-color: #bfdbfe; }
      .border-green-200 { border-color: #bbf7d0; }
      .border-red-200 { border-color: #fecaca; }
      .border-yellow-200 { border-color: #fde68a; }
      .border-indigo-200 { border-color: #c7d2fe; }
      .border-blue-500 { border-color: #3b82f6; }
      .border-green-500 { border-color: #22c55e; }
      .border-orange-500 { border-color: #f97316; }
      .border-purple-500 { border-color: #a855f7; }
      
      .shadow-md { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
      .shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
      .shadow-xl { box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); }
      .shadow-green-100 { box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15); }
      .shadow-blue-100 { box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15); }
      
      .bg-red-100 { background-color: #fee2e2; }
      .bg-yellow-100 { background-color: #fef3c7; }
      .bg-green-100 { background-color: #dcfce7; }
      .bg-gray-100 { background-color: #f3f4f6; }
      .bg-blue-100 { background-color: #dbeafe; }
      .bg-purple-100 { background-color: #ede9fe; }
      .bg-pink-100 { background-color: #fce7f3; }
      .bg-orange-100 { background-color: #fed7aa; }
      .bg-blue-500 { background-color: #3b82f6; }
      .bg-green-500 { background-color: #22c55e; }
      .bg-red-500 { background-color: #ef4444; }
      .bg-gray-500 { background-color: #6b7280; }
      .bg-gray-400 { background-color: #9ca3af; }
      .bg-green-400 { background-color: #4ade80; }
      .bg-purple-500 { background-color: #a855f7; }
      .bg-orange-500 { background-color: #f97316; }
      .bg-gray-800 { background-color: #1f2937; }
      .bg-gray-300 { background-color: #d1d5db; }
      
      .text-purple-800 { color: #6b21a8; }
      .text-blue-800 { color: #1e40af; }
      .text-pink-800 { color: #be185d; }
      .text-orange-800 { color: #9a3412; }
      .text-green-600 { color: #16a34a; }
      
      .w-3 { width: 0.75rem; }
      .h-3 { height: 0.75rem; }
      .w-5 { width: 1.25rem; }
      .h-5 { height: 1.25rem; }
      .w-8 { width: 2rem; }
      .h-8 { height: 2rem; }
      .w-12 { width: 3rem; }
      .h-12 { height: 3rem; }
      
      .relative { position: relative; }
      .absolute { position: absolute; }
      .top-3 { top: 0.75rem; }
      .right-3 { right: 0.75rem; }
      .bottom-3 { bottom: 0.75rem; }
      .left-5 { left: 1.25rem; }
      
      .transition-all { transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
      .transition-colors { transition-property: color, background-color, border-color, text-decoration-color, fill, stroke; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
      .duration-300 { transition-duration: 300ms; }
      
      .hover\\:bg-blue-600:hover { background-color: #2563eb; }
      .hover\\:bg-red-600:hover { background-color: #dc2626; }
      .hover\\:bg-gray-600:hover { background-color: #4b5563; }
      .hover\\:bg-green-600:hover { background-color: #16a34a; }
      .hover\\:bg-purple-600:hover { background-color: #9333ea; }
      .hover\\:bg-orange-600:hover { background-color: #ea580c; }
      .hover\\:shadow-lg:hover { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
      .hover\\:scale-102:hover { transform: scale(1.02); }
      
      .line-through { text-decoration-line: line-through; }
      .inline-block { display: inline-block; }
      .text-center { text-align: center; }
      
      button { cursor: pointer; border: none; outline: none; }
      input[type="checkbox"] { accent-color: #3b82f6; }
    </style>
  `;









  // User Card Component
  const UserCard = function UserCard(props) {
    const { user } = props;
    
    // Generate avatar from name (first letters)
    const getAvatar = (name) => {
      return name.split(' ').map(n => n[0]).join('').toUpperCase();
    };
    
    // Assume users are active by default since the app.py data doesn't include active status
    const isActive = true;
    const tasksAssigned = Math.floor(Math.random() * 5) + 1; // Random number for demo
    
    return React.createElement('div', {
      className: `p-4 bg-white rounded-xl border-2 ${isActive ? 'border-green-200' : 'border-gray-200'} shadow-md hover:shadow-lg transition-all duration-300`,
    },
      React.createElement('div', { className: 'flex items-center space-x-3 mb-3' },
        React.createElement('div', {
          className: `w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg ${
            isActive ? 'bg-green-500' : 'bg-gray-400'
          }`
        }, getAvatar(user.name)),
        React.createElement('div', { className: 'flex-1' },
          React.createElement('h3', { className: 'font-semibold text-gray-800' }, user.name),
          React.createElement('p', { className: 'text-sm text-gray-600' }, user.email),
          React.createElement('span', { 
            className: `inline-block px-2 py-1 text-xs rounded-full mt-1 ${
              user.role === 'admin' ? 'bg-purple-100 text-purple-800' :
              user.role === 'user' ? 'bg-blue-100 text-blue-800' :
              'bg-orange-100 text-orange-800'
            }`
          }, user.role.charAt(0).toUpperCase() + user.role.slice(1))
        ),
        React.createElement('div', {
          className: `w-3 h-3 rounded-full ${isActive ? 'bg-green-400' : 'bg-gray-400'}`
        })
      ),
      React.createElement('div', { className: 'flex justify-between items-center text-sm' },
        React.createElement('span', { className: 'text-gray-600' }, `${tasksAssigned} tasks assigned`),
        React.createElement('span', { 
          className: `px-2 py-1 rounded-full ${isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}` 
        }, isActive ? 'Active' : 'Inactive')
      )
    );
  };

  // User Statistics Component
  const UserStats = function UserStats(props) {
    const { users } = props;
    const total = users.length;
    const adminUsers = users.filter(u => u.role === 'admin').length;
    const regularUsers = users.filter(u => u.role === 'user').length;
    
    const roleCounts = users.reduce((acc, user) => {
      acc[user.role] = (acc[user.role] || 0) + 1;
      return acc;
    }, {});

    return React.createElement('div', { className: 'bg-gradient-to-br from-indigo-50 via-white to-cyan-50 p-6 rounded-2xl mb-8 border border-indigo-200 shadow-xl' },
      React.createElement('div', { className: 'flex items-center justify-between mb-6' },
        React.createElement('h3', { className: 'text-2xl font-bold text-gray-800 flex items-center' }, 
          React.createElement('span', { className: 'mr-2' }, '📊'),
          'User Statistics'
        ),
        React.createElement('div', { className: 'text-sm text-gray-500' },
          'Last updated: ', new Date().toLocaleTimeString()
        )
      ),
      
      // Main stats grid
      React.createElement('div', { className: 'grid grid-cols-2 md:grid-cols-3 gap-6 mb-6' },
        React.createElement('div', { className: 'text-center p-4 bg-white rounded-xl shadow-md border-l-4 border-blue-500' },
          React.createElement('div', { className: 'text-4xl font-bold text-blue-600 mb-2' }, total),
          React.createElement('div', { className: 'text-sm font-medium text-gray-600' }, 'Total Users'),
          React.createElement('div', { className: 'text-xs text-gray-500 mt-1' }, 'All registered')
        ),
        React.createElement('div', { className: 'text-center p-4 bg-white rounded-xl shadow-md border-l-4 border-purple-500' },
          React.createElement('div', { className: 'text-4xl font-bold text-purple-600 mb-2' }, adminUsers),
          React.createElement('div', { className: 'text-sm font-medium text-gray-600' }, 'Administrators'),
          React.createElement('div', { className: 'text-xs text-gray-500 mt-1' }, 'System admins')
        ),
        React.createElement('div', { className: 'text-center p-4 bg-white rounded-xl shadow-md border-l-4 border-green-500' },
          React.createElement('div', { className: 'text-4xl font-bold text-green-600 mb-2' }, regularUsers),
          React.createElement('div', { className: 'text-sm font-medium text-gray-600' }, 'Regular Users'),
          React.createElement('div', { className: 'text-xs text-gray-500 mt-1' }, 'Standard access')
        )
      ),
      
      // Role breakdown
      total > 0 && React.createElement('div', { className: 'bg-white p-5 rounded-xl shadow-md' },
        React.createElement('h4', { className: 'font-semibold mb-4 text-gray-700 flex items-center' }, 
          React.createElement('span', { className: 'mr-2' }, '👤'),
          'Role Distribution'
        ),
        React.createElement('div', { className: 'space-y-3' },
          Object.entries(roleCounts).map(([role, count]) =>
            React.createElement('div', { 
              key: role,
              className: 'flex justify-between items-center'
            },
              React.createElement('span', { 
                className: `px-3 py-1 text-sm font-medium rounded-full ${
                  role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
                }`
              }, role.charAt(0).toUpperCase() + role.slice(1)),
              React.createElement('span', { className: 'font-bold text-lg' }, count)
            )
          )
        )
      )
    );
  };

  // Main Dashboard Component
  const Dashboard = function Dashboard() {
    const activeUsers = users; // All users are considered active since app.py doesn't have active status
    
    return React.createElement('div', { className: 'min-h-screen bg-gray-50' },
      // Include styles
      React.createElement('div', { dangerouslySetInnerHTML: { __html: styles } }),
      // Header
      React.createElement('header', { className: 'bg-gradient-to-r from-blue-600 to-purple-700 text-white p-6 shadow-lg' },
        React.createElement('div', { className: 'max-w-7xl mx-auto' },
          React.createElement('h1', { className: 'text-4xl font-bold mb-2 flex items-center' }, 
            React.createElement('span', { className: 'mr-3' }, '�'),
            page_title
          ),
          React.createElement('p', { className: 'text-blue-100 text-lg' }, 
            'User management system built with Flask-React - Server-Side Rendering'
          )
        )
      ),
      
      // Main content
      React.createElement('div', { className: 'max-w-7xl mx-auto p-6' },
        // Statistics
        React.createElement(UserStats, { users }),
        
        // Quick actions
        can_edit && React.createElement('div', { className: 'mb-8 p-6 bg-white rounded-2xl shadow-lg border border-gray-200' },
          React.createElement('h2', { className: 'text-xl font-bold mb-4 flex items-center text-gray-800' },
            React.createElement('span', { className: 'mr-2' }, '⚡'),
            'Quick Actions'
          ),
          React.createElement('div', { className: 'grid grid-cols-2 md:grid-cols-4 gap-4' },
            React.createElement('button', { 
              className: 'p-4 bg-green-500 text-white rounded-xl hover:bg-green-600 transition-colors font-medium' 
            }, '👤 Add User'),
            React.createElement('button', { 
              className: 'p-4 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors font-medium' 
            }, '✏️ Edit User'),
            React.createElement('button', { 
              className: 'p-4 bg-purple-500 text-white rounded-xl hover:bg-purple-600 transition-colors font-medium' 
            }, '📊 Export Users'),
            React.createElement('button', { 
              className: 'p-4 bg-orange-500 text-white rounded-xl hover:bg-orange-600 transition-colors font-medium' 
            }, '⚙️ Settings')
          )
        ),
        
        // Users content
        React.createElement('div', { className: 'max-w-7xl mx-auto' },
          React.createElement('div', { className: 'mb-8' },
            React.createElement('div', { className: 'flex justify-between items-center mb-6' },
              React.createElement('h2', { className: 'text-2xl font-bold text-gray-800 flex items-center' },
                React.createElement('span', { className: 'mr-2' }, '�'),
                `Users (${users.length})`
              ),
              React.createElement('div', { className: 'text-sm text-gray-600' },
                current_user.role === 'admin' ? 'Admin View' : 'Standard View'
              )
            ),
            
            React.createElement('div', { className: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' },
              users.map(user =>
                React.createElement(UserCard, {
                  key: user.id,
                  user: user
                })
              )
            )
          )
        )
      ),
      
      // Footer
      React.createElement('footer', { className: 'bg-gray-800 text-white p-6 mt-12' },
        React.createElement('div', { className: 'max-w-7xl mx-auto text-center' },
          React.createElement('p', { className: 'text-gray-300' }, 
            'Complex React Application • Built with React.createElement • Server-Side Rendering Ready'
          ),
          React.createElement('p', { className: 'text-sm text-gray-400 mt-2' }, 
            'Demonstrates: Component composition, conditional rendering, data mapping, event handling, and styling'
          )
        )
      )
    );
  };

  return React.createElement(Dashboard);
}

module.exports = UserList;
// API Configuration for Task Pilot Frontend
const API_BASE_URL = 'https://task-pilot-8wx0.onrender.com';

// API Endpoints
const API_ENDPOINTS = {
    // Authentication
    LOGIN: `${API_BASE_URL}/login`,
    REGISTER: `${API_BASE_URL}/register`,
    LOGOUT: `${API_BASE_URL}/logout`,

    // Tasks
    HOME: `${API_BASE_URL}/`,  // GET for tasks list, POST to add new task
    COMPLETE_TASK: (id) => `${API_BASE_URL}/complete/${id}`,
    DELETE_TASK: (id) => `${API_BASE_URL}/delete/${id}`,
    EDIT_TASK: (id) => `${API_BASE_URL}/edit/${id}`  // GET for form, POST to update
};

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        credentials: 'include', // Include cookies for session management
    };

    const response = await fetch(endpoint, { ...defaultOptions, ...options });

    if (response.ok) {
        return await response.text(); // Flask returns HTML, not JSON
    } else {
        throw new Error(`API call failed: ${response.status}`);
    }
}

// Example usage functions
async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    return await apiCall(API_ENDPOINTS.LOGIN, {
        method: 'POST',
        body: formData
    });
}

async function register(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    return await apiCall(API_ENDPOINTS.REGISTER, {
        method: 'POST',
        body: formData
    });
}

async function getTasks() {
    return await apiCall(API_ENDPOINTS.HOME, {
        method: 'GET'
    });
}

async function addTask(task, progress, dueDate) {
    const formData = new URLSearchParams();
    formData.append('task', task);
    formData.append('progress', progress || 0);
    formData.append('due_date', dueDate || '');

    return await apiCall(API_ENDPOINTS.HOME, {
        method: 'POST',
        body: formData
    });
}

async function completeTask(id) {
    return await apiCall(API_ENDPOINTS.COMPLETE_TASK(id), {
        method: 'GET'
    });
}

async function deleteTask(id) {
    return await apiCall(API_ENDPOINTS.DELETE_TASK(id), {
        method: 'GET'
    });
}

async function updateTask(id, task, progress, dueDate) {
    const formData = new URLSearchParams();
    formData.append('task', task);
    formData.append('progress', progress || 0);
    formData.append('due_date', dueDate || '');

    return await apiCall(API_ENDPOINTS.EDIT_TASK(id), {
        method: 'POST',
        body: formData
    });
}

async function logout() {
    return await apiCall(API_ENDPOINTS.LOGOUT, {
        method: 'GET'
    });
}

// Export for use in your frontend
export {
    API_BASE_URL,
    API_ENDPOINTS,
    apiCall,
    login,
    register,
    getTasks,
    addTask,
    completeTask,
    deleteTask,
    updateTask,
    logout
};
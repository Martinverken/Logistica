import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://logistica-backend-3nzk.onrender.com';

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para errores
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// =====================================================
// ORDERS API
// =====================================================
export const ordersAPI = {
  getAll: (limit = 100, offset = 0) => 
    api.get(`/orders?limit=${limit}&offset=${offset}`),
  
  getById: (id) => 
    api.get(`/orders/${id}`),
  
  getToday: () => 
    api.get('/orders/today'),
  
  getDelayed: () => 
    api.get('/orders/delayed'),
  
  getAtRisk: () => 
    api.get('/orders/at-risk')
};

// =====================================================
// COMMENTS API
// =====================================================
export const commentsAPI = {
  getByOrder: (orderId) => 
    api.get(`/comments/order/${orderId}`),
  
  create: (commentData) => 
    api.post('/comments', commentData)
};

// =====================================================
// TICKETS API
// =====================================================
export const ticketsAPI = {
  getAll: () => 
    api.get('/tickets'),
  
  getByOrder: (orderId) => 
    api.get(`/tickets/order/${orderId}`),
  
  create: (ticketData) => 
    api.post('/tickets', ticketData),
  
  update: (ticketId, updateData) => 
    api.patch(`/tickets/${ticketId}`, updateData)
};

// =====================================================
// DASHBOARD API
// =====================================================
export const dashboardAPI = {
  getStats: () => 
    api.get('/dashboard/stats')
};

// =====================================================
// SYNC API
// =====================================================
export const syncAPI = {
  syncAll: () => 
    api.post('/sync/all'),
  
  syncFalabella: () => 
    api.post('/sync/falabella'),
  
  syncMercadoLibre: () => 
    api.post('/sync/mercadolibre')
};

export default api;
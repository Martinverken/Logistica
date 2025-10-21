import api from './api';

export const orderService = {
  // Obtener todas las órdenes
  getAll: () => api.get('/orders'),
  
  // Órdenes del día
  getToday: () => api.get('/orders/today'),
  
  // Órdenes atrasadas
  getDelayed: () => api.get('/orders/delayed'),
  
  // Órdenes en riesgo
  getAtRisk: () => api.get('/orders/at-risk'),
  
  // Una orden específica
  getById: (id) => api.get(`/orders/${id}`),
  
  // Estadísticas del dashboard
  getStats: () => api.get('/dashboard/stats'),
};

export default orderService;
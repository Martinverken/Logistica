import { useState, useEffect } from 'react';
import orderService from '../services/orderService';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await orderService.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Cargando...</div>;
  }

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Órdenes del día */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Órdenes Hoy</h3>
          <p className="text-4xl font-bold text-blue-600 mt-2">
            {stats?.orders_today || 0}
          </p>
        </div>

        {/* Órdenes atrasadas */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Atrasadas</h3>
          <p className="text-4xl font-bold text-red-600 mt-2">
            {stats?.orders_delayed || 0}
          </p>
        </div>

        {/* Listas para despachar */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Listo Despachar</h3>
          <p className="text-4xl font-bold text-green-600 mt-2">
            {stats?.orders_ready_to_ship || 0}
          </p>
        </div>
      </div>
    </div>
  );
}
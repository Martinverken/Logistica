import { useState, useEffect } from 'react';
import orderService from '../services/orderService';
import OrderDetailModal from '../components/OrderDetailModal';

export default function OrdersToday() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const response = await orderService.getToday();
      setOrders(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-8">Cargando...</div>;

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Órdenes del Día</h2>
      
      {orders.length === 0 ? (
        <p className="text-gray-500">No hay órdenes para hoy</p>
      ) : (
        <div className="grid gap-4">
          {orders.map((order) => (
            <div 
              key={order.id} 
              className="bg-white p-4 rounded-lg shadow cursor-pointer hover:shadow-lg transition"
              onClick={() => setSelectedOrder(order)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-bold text-lg">Orden #{order.order_number}</p>
                  <p className="text-gray-600">{order.customer_name}</p>
                  <p className="text-sm text-gray-500 capitalize">{order.platform}</p>
                </div>
                <div className="text-right">
                  <span className="inline-block px-3 py-1 rounded-full text-sm font-semibold bg-blue-100 text-blue-800">
                    {order.shipping_type}
                  </span>
                  <p className="text-sm text-gray-600 mt-2">
                    ${order.total_amount?.toLocaleString()}
                  </p>
                </div>
              </div>
              <div className="mt-3 text-sm text-gray-600">
                <p>📍 {order.shipping_city}</p>
                <p>⏰ Límite: {new Date(order.limite_despacho).toLocaleString()}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedOrder && (
        <OrderDetailModal
          order={selectedOrder}
          onClose={() => setSelectedOrder(null)}
        />
      )}
    </div>
  );
}
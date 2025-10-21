import { X, Package, Truck, Calendar, Clock, AlertCircle } from 'lucide-react';
import { useState, useEffect, useCallback } from 'react';
import { commentsAPI, ticketsAPI } from '../services/api';
import { formatDate, formatCurrency } from '../utils/formatters';

export default function OrderDetailModal({ order, onClose }) {
  const [comments, setComments] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(false);

  const loadCommentsAndTickets = useCallback(async () => {
    try {
      const [commentsRes, ticketsRes] = await Promise.all([
        commentsAPI.getByOrder(order.id),
        ticketsAPI.getByOrder(order.id)
      ]);
      setComments(commentsRes.data);
      setTickets(ticketsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  }, [order.id]);

  useEffect(() => {
    loadCommentsAndTickets();
  }, [loadCommentsAndTickets]);

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    
    setLoading(true);
    try {
      await commentsAPI.create({
        order_id: order.id,
        comment: newComment,
        user_name: 'Usuario'
      });
      setNewComment('');
      loadCommentsAndTickets();
    } catch (error) {
      console.error('Error adding comment:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      listo_despachar: 'bg-blue-100 text-blue-800',
      etiqueta_impresa: 'bg-purple-100 text-purple-800',
      enviado: 'bg-yellow-100 text-yellow-800',
      entregado: 'bg-green-100 text-green-800',
      cancelado: 'bg-red-100 text-red-800'
    };
    return badges[status] || 'bg-gray-100 text-gray-800';
  };

  const getPlatformBadge = (platform) => {
    const badges = {
      falabella: 'bg-green-100 text-green-800',
      mercadolibre: 'bg-yellow-100 text-yellow-800'
    };
    return badges[platform] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Orden #{order.order_number}
            </h2>
            <div className="flex gap-2 mt-2">
              <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getPlatformBadge(order.platform)}`}>
                {order.platform === 'falabella' ? 'Falabella' : 'MercadoLibre'}
              </span>
              <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusBadge(order.current_status)}`}>
                {order.current_status?.replace(/_/g, ' ').toUpperCase()}
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          
          {/* Info Principal */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Cliente */}
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <Package size={20} className="text-blue-600" />
                Información del Cliente
              </h3>
              <div className="space-y-2 text-sm">
                <p><strong>Nombre:</strong> {order.customer_name || 'N/A'}</p>
                <p><strong>Teléfono:</strong> {order.customer_phone || 'N/A'}</p>
                <p><strong>Email:</strong> {order.customer_email || 'N/A'}</p>
              </div>
            </div>

            {/* Envío */}
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <Truck size={20} className="text-green-600" />
                Información de Envío
              </h3>
              <div className="space-y-2 text-sm">
                <p><strong>Tipo:</strong> {order.shipping_type?.replace(/_/g, ' ')}</p>
                <p><strong>Ciudad:</strong> {order.shipping_city || 'N/A'}</p>
                <p><strong>Dirección:</strong> {order.shipping_address || 'N/A'}</p>
              </div>
            </div>

            {/* Fechas */}
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <Calendar size={20} className="text-purple-600" />
                Fechas Importantes
              </h3>
              <div className="space-y-2 text-sm">
                <p><strong>Creada:</strong> {formatDate(order.created_at)}</p>
                <p>
                  <strong>Límite despacho:</strong>{' '}
                  <span className={order.is_delayed ? 'text-red-600 font-semibold' : ''}>
                    {formatDate(order.limite_despacho)}
                  </span>
                </p>
                {order.promised_delivery && (
                  <p><strong>Entrega prometida:</strong> {formatDate(order.promised_delivery)}</p>
                )}
              </div>
            </div>

            {/* Detalles Adicionales */}
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <Clock size={20} className="text-orange-600" />
                Detalles
              </h3>
              <div className="space-y-2 text-sm">
                <p><strong>Monto:</strong> {formatCurrency(order.total_amount)}</p>
                <p><strong>Items:</strong> {order.items_count}</p>
                {order.is_delayed && (
                  <p className="text-red-600 font-semibold flex items-center gap-1">
                    <AlertCircle size={16} />
                    Atrasada por {order.hours_delayed}h
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Tickets */}
          {tickets.length > 0 && (
            <div className="border-t pt-6">
              <h3 className="font-semibold text-gray-900 mb-3">Tickets Asociados</h3>
              <div className="space-y-2">
                {tickets.map((ticket) => (
                  <div key={ticket.id} className="bg-red-50 p-3 rounded border border-red-200">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold text-red-900">{ticket.title}</p>
                        <p className="text-sm text-red-700 mt-1">{ticket.description}</p>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        ticket.status === 'open' ? 'bg-red-100 text-red-800' :
                        ticket.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {ticket.status.toUpperCase()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Comentarios */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-bold mb-3">Comentarios ({comments.length})</h3>
            
            {/* Formulario nuevo comentario */}
            <form onSubmit={handleAddComment} className="mb-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Agregar comentario..."
                  className="flex-1 px-3 py-2 border rounded"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                />
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                  disabled={loading}
                >
                  {loading ? 'Enviando...' : 'Enviar'}
                </button>
              </div>
            </form>

            {/* Lista de comentarios */}
            {comments.length === 0 ? (
              <p className="text-gray-500 text-sm">No hay comentarios</p>
            ) : (
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {comments.map((comment) => (
                  <div key={comment.id} className="bg-gray-50 p-3 rounded">
                    <div className="flex justify-between items-start mb-1">
                      <span className="font-semibold text-sm">{comment.user_name}</span>
                      <span className="text-xs text-gray-500">
                        {new Date(comment.created_at).toLocaleString()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700">{comment.comment}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import OrdersToday from './pages/OrdersToday';
import DelayedOrders from './pages/DelayedOrders';
import AtRiskOrders from './pages/AtRiskOrders';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/today" element={<OrdersToday />} />
          <Route path="/delayed" element={<DelayedOrders />} />
          <Route path="/at-risk" element={<AtRiskOrders />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
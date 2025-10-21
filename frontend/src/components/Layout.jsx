import { Link } from 'react-router-dom';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">
              Sistema Logística
            </h1>
            <nav className="flex gap-4">
              <Link to="/" className="text-blue-600 hover:text-blue-800">
                Dashboard
              </Link>
              <Link to="/today" className="text-blue-600 hover:text-blue-800">
                Hoy
              </Link>
              <Link to="/delayed" className="text-red-600 hover:text-red-800">
                Atrasadas
              </Link>
              <Link to="/at-risk" className="text-yellow-600 hover:text-yellow-800">
                En Riesgo
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
}
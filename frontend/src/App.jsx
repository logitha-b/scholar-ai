import { Routes, Route, Navigate } from 'react-router-dom'
import { useStore } from './store/useStore'
import Header from './components/shared/Header'
import { LoginPage, RegisterPage } from './components/auth/AuthPages'
import HomePage from './pages/HomePage'
import LearningPage from './pages/LearningPage'
import ResourcesPage from './pages/ResourcesPage'
import PlacementPage from './pages/PlacementPage'
import AptitudePage from './pages/AptitudePage'
import CommunicationPage from './pages/CommunicationPage'
import DashboardPage from './pages/DashboardPage'
import AdminPage from './pages/AdminPage'

function ProtectedRoute({ children, adminOnly = false }) {
  const { user } = useStore()
  if (!user) return <Navigate to="/login" replace />
  if (adminOnly && user.role !== 'admin') return <Navigate to="/" replace />
  if (!adminOnly && user.role === 'admin') return <Navigate to="/admin" replace />
  return children
}

function GuestRoute({ children }) {
  const { user } = useStore()
  if (user) return <Navigate to={user.role === 'admin' ? '/admin' : '/'} replace />
  return children
}

export default function App() {
  const { user } = useStore()
  const showHeader = !!user

  return (
    <div className="min-h-screen bg-slate-50">
      {showHeader && <Header />}
      <Routes>
        {/* Guest routes */}
        <Route path="/login"    element={<GuestRoute><LoginPage /></GuestRoute>} />
        <Route path="/register" element={<GuestRoute><RegisterPage /></GuestRoute>} />

        {/* Student routes */}
        <Route path="/"             element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
        <Route path="/learning"     element={<ProtectedRoute><LearningPage /></ProtectedRoute>} />
        <Route path="/resources"    element={<ProtectedRoute><ResourcesPage /></ProtectedRoute>} />
        <Route path="/placement"    element={<ProtectedRoute><PlacementPage /></ProtectedRoute>} />
        <Route path="/aptitude"     element={<ProtectedRoute><AptitudePage /></ProtectedRoute>} />
        <Route path="/communication"element={<ProtectedRoute><CommunicationPage /></ProtectedRoute>} />
        <Route path="/dashboard"    element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />

        {/* Admin routes */}
        <Route path="/admin" element={<ProtectedRoute adminOnly><AdminPage /></ProtectedRoute>} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to={user ? (user.role === 'admin' ? '/admin' : '/') : '/login'} replace />} />
      </Routes>
    </div>
  )
}

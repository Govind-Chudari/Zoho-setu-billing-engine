import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Login     from "./pages/Login";
import Register  from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Files     from "./pages/Files";
import Usage     from "./pages/Usage";      
import Billing   from "./pages/Billing";    
import "./App.css";

function PrivateRoute({ children }) {
  const { isLoggedIn, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center
                      bg-gradient-to-br from-brand-800 to-brand-600">
        <div className="text-center text-white">
          <div className="w-8 h-8 border-2 border-white/30 border-t-white
                          rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm font-medium">Loading...</p>
        </div>
      </div>
    );
  }
  return isLoggedIn ? children : <Navigate to="/login" replace />;
}

function PublicRoute({ children }) {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? <Navigate to="/dashboard" replace /> : children;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/"          element={<Navigate to="/login" replace />} />
      <Route path="/login"     element={<PublicRoute><Login /></PublicRoute>} />
      <Route path="/register"  element={<PublicRoute><Register /></PublicRoute>} />
      <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
      <Route path="/files"     element={<PrivateRoute><Files /></PrivateRoute>} />
      <Route path="/usage"     element={<PrivateRoute><Usage /></PrivateRoute>} />     
      <Route path="/billing"   element={<PrivateRoute><Billing /></PrivateRoute>} />   
      <Route path="*"          element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { ComposeProvider } from './context/ComposeContext';
import AppLayout from './components/layout/AppLayout';

import DashboardPage from './pages/DashboardPage';
import PipelinePage from './pages/PipelinePage';
import ProfessorsPage from './pages/ProfessorsPage';
import ProfessorDetailPage from './pages/ProfessorDetailPage';
import EmailCenterPage from './pages/EmailCenterPage';
import TemplatesPage from './pages/TemplatesPage';
import SettingsPage from './pages/SettingsPage';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <ComposeProvider>
          <BrowserRouter>
            <Toaster position="top-right" toastOptions={{ duration: 3500 }} />
            <AppLayout>
              <Routes>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/pipeline" element={<PipelinePage />} />
                <Route path="/professors" element={<ProfessorsPage />} />
                <Route path="/professors/:id" element={<ProfessorDetailPage />} />
                <Route path="/emails" element={<EmailCenterPage />} />
                <Route path="/templates" element={<TemplatesPage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </AppLayout>
          </BrowserRouter>
        </ComposeProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;

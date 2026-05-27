// import React from 'react'
// import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
// import { Toaster } from 'react-hot-toast'

// function App() {
//   return (
//     <Router>
//       <Toaster position="top-right" />
//       <div className="min-h-screen bg-gray-50">
//         <Routes>
//           <Route path="/" element={<Navigate to="/dashboard" />} />
//           <Route path="/dashboard" element={<div>Dashboard Page</div>} />
//         </Routes>
//       </div>
//     </Router>
//   )
// }

// export default App

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import CategoryTrends from './pages/CategoryTrends';
import ConsumerInsights from './pages/ConsumerInsights';
import CompetitorMapping from './pages/CompetitorMapping';
import VendorSourcing from './pages/VendorSourcing';
import CampaignImpact from './pages/CampaignImpact';
import Reports from './pages/Reports';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/category-trends" element={<CategoryTrends />} />
              <Route path="/consumer-insights" element={<ConsumerInsights />} />
              <Route path="/competitor-mapping" element={<CompetitorMapping />} />
              <Route path="/vendor-sourcing" element={<VendorSourcing />} />
              <Route path="/campaign-impact" element={<CampaignImpact />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </Layout>
        </Router>
      </LocalizationProvider>
    </ThemeProvider>
  );
}

export default App;

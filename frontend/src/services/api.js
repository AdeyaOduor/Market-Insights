import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
          refresh: refreshToken,
        });
        localStorage.setItem('access_token', response.data.access);
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Redirect to login
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const dashboardService = {
  getUnifiedDashboard: (params) => api.get('/dashboard/unified_dashboard/', { params }),
  getCategoryTrends: (params) => api.get('/dashboard/category_trends/', { params }),
  getPricingIntelligence: (params) => api.get('/dashboard/pricing_intelligence/', { params }),
  getConsumerInsights: (params) => api.get('/dashboard/consumer_insights/', { params }),
  getMarketOpportunities: (params) => api.get('/dashboard/market_opportunities/', { params }),
  getVendorSourcing: (params) => api.get('/dashboard/vendor_sourcing/', { params }),
  measureCampaignImpact: (data) => api.post('/dashboard/measure_campaign_impact/', data),
};
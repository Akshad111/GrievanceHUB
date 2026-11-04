import apiClient from './apiClient.js';

export const analyticsApi = {
  // 1. Executive Analytics Overview
  getOverview: async (params = {}) => {
    const response = await apiClient.get('/analytics/overview/', { params });
    return response.data?.data || response.data;
  },

  // 2. Grievance Volume Trends
  getTrends: async (params = {}) => {
    const response = await apiClient.get('/analytics/trends/', { params });
    return response.data?.data || response.data;
  },

  // 3. Category Distribution & Performance
  getCategories: async (params = {}) => {
    const response = await apiClient.get('/analytics/categories/', { params });
    return response.data?.data || response.data;
  },

  // 4. Status Distribution
  getStatusDistribution: async (params = {}) => {
    const response = await apiClient.get('/analytics/status-distribution/', { params });
    return response.data?.data || response.data;
  },

  // 5. Department Analytics
  getDepartments: async (params = {}) => {
    const response = await apiClient.get('/analytics/departments/', { params });
    return response.data?.data || response.data;
  },

  // 6. Resolution Time Analytics
  getResolutionTimes: async (params = {}) => {
    const response = await apiClient.get('/analytics/resolution-times/', { params });
    return response.data?.data || response.data;
  },

  // 7. Officer Workload & Capacity Utilization
  getOfficerWorkload: async (params = {}) => {
    const response = await apiClient.get('/analytics/officer-workload/', { params });
    return response.data?.data || response.data;
  },

  // 8. Reopen Analytics
  getReopens: async (params = {}) => {
    const response = await apiClient.get('/analytics/reopens/', { params });
    return response.data?.data || response.data;
  },

  // 9. Routing and Assignment Analytics
  getRouting: async (params = {}) => {
    const response = await apiClient.get('/analytics/routing/', { params });
    return response.data?.data || response.data;
  },

  // 10. Geographic & Ward Analytics
  getLocations: async (params = {}) => {
    const response = await apiClient.get('/analytics/locations/', { params });
    return response.data?.data || response.data;
  },

  // 11. ML Model Monitoring Foundation (Offline + Live Feedback)
  getMLOverview: async () => {
    const response = await apiClient.get('/analytics/ml/overview/');
    return response.data?.data || response.data;
  },

  // 12. ML Confusion Matrix
  getMLConfusionMatrix: async () => {
    const response = await apiClient.get('/analytics/ml/confusion-matrix/');
    return response.data?.data || response.data;
  },

  // 13. ML Confidence Breakdown
  getMLConfidence: async () => {
    const response = await apiClient.get('/analytics/ml/confidence/');
    return response.data?.data || response.data;
  },

  // 14. Data Quality & Health Audit
  getDataQuality: async () => {
    const response = await apiClient.get('/analytics/data-quality/');
    return response.data?.data || response.data;
  },

  // 15. Export CSV
  exportCSV: async (params = {}) => {
    const response = await apiClient.get('/analytics/export/', {
      params,
      responseType: 'blob'
    });
    return response.data;
  },

  // 16. Municipal Reports Generation
  generateReport: async (params = {}) => {
    const response = await apiClient.get('/analytics/reports/generate/', { params });
    return response.data?.data || response.data;
  }
};

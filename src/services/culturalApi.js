import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const culturalClient = axios.create({
  baseURL: `${API_BASE_URL}/api/cultural`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const culturalApi = {
  /**
   * Get weather & activity-adapted attire recommendations.
   * @param {Object} payload { destination, temperature_celsius, weather_condition, planned_poi_categories }
   */
  getAttireRecommendations: async (payload) => {
    const response = await culturalClient.post('/attire-recommendations', payload);
    return response.data;
  },

  /**
   * Fetch comprehensive destination cultural guide.
   * @param {string} destination
   */
  getCulturalGuide: async (destination) => {
    const response = await culturalClient.get(`/guide/${encodeURIComponent(destination)}`);
    return response.data;
  },

  /**
   * Get sacred site entry dress codes.
   */
  getDressCodes: async () => {
    const response = await culturalClient.get('/dress-codes');
    return response.data;
  },
};

export default culturalApi;

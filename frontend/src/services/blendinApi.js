import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const blendinClient = axios.create({
  baseURL: `${API_BASE_URL}/api/blendin`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const blendinApi = {
  /**
   * Evaluate Blend-In Score for an itinerary.
   * @param {Object} payload { destination, poi_list, restaurant_list, user_preferences, selected_attire_count, etiquette_acknowledgement }
   */
  evaluateItinerary: async (payload) => {
    const response = await blendinClient.post('/evaluate', payload);
    return response.data;
  },

  /**
   * Optimize & fine-tune itinerary when target blend-in score changes.
   * @param {Object} payload { destination, current_score, target_score, candidate_pois, candidate_restaurants, current_selected_poi_ids, user_preferences }
   */
  optimizeForTarget: async (payload) => {
    const response = await blendinClient.post('/optimize-target', payload);
    return response.data;
  },

  /**
   * Get metadata and definitions for all Blend-In persona tiers.
   */
  getTiers: async () => {
    const response = await blendinClient.get('/tiers');
    return response.data;
  },

  /**
   * Fetch destination-specific blend-in recommendations and etiquette tips.
   * @param {string} destination
   */
  getDestinationTips: async (destination) => {
    const response = await blendinClient.get(`/tips/${encodeURIComponent(destination)}`);
    return response.data;
  },
};

export default blendinApi;

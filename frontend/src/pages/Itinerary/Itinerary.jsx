import React, { useState, useEffect } from 'react';
import BlendinSlider from '../../components/BlendinSlider';
import blendinApi from '../../services/blendinApi';

export const Itinerary = () => {
  const [destination, setDestination] = useState('Jaipur');
  const [currentScore, setCurrentScore] = useState(68);
  const [targetScore, setTargetScore] = useState(68);
  const [isLoading, setIsLoading] = useState(false);
  const [breakdown, setBreakdown] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [suggestedSwaps, setSuggestedSwaps] = useState([]);
  const [localComparison, setLocalComparison] = useState(76);

  // Sample schedule items with Traffic-Light POI indicators
  const [schedule, setSchedule] = useState([
    {
      time: '08:00 AM - 10:00 AM',
      type: 'poi',
      name: 'Amber Palace & Fort',
      category: 'Historic Fortress',
      trafficLight: 'GREEN',
      matchReason: 'Wheelchair ramps available, highly matches interest in Rajput architecture.',
      authenticity: '85%',
      attire: 'Modest cotton attire & comfortable walking shoes',
      isLocalGem: false,
    },
    {
      time: '10:30 AM - 11:30 AM',
      type: 'food',
      name: 'Gulab Ji Chai Wale',
      category: 'Heritage Tea & Snacks',
      trafficLight: 'GREEN',
      matchReason: 'Pure vegetarian, famous bun maska and spiced masala chai with locals.',
      authenticity: '95%',
      isLocalGem: true,
    },
    {
      time: '12:00 PM - 02:00 PM',
      type: 'poi',
      name: 'Anokhi Museum of Hand Printing',
      category: 'Artisan Workshop',
      trafficLight: 'GREEN',
      matchReason: 'Interactive live block-printing demonstration, elder-friendly seating.',
      authenticity: '92%',
      attire: 'Casual breathable linen',
      isLocalGem: true,
    },
    {
      time: '02:30 PM - 03:45 PM',
      type: 'food',
      name: 'Laxmi Mishtan Bhandar (LMB)',
      category: 'Traditional Rajasthani Thali',
      trafficLight: 'GREEN',
      matchReason: 'Strict vegetarian & Jain friendly, authentic Dal Baati Churma.',
      authenticity: '90%',
      isLocalGem: true,
    },
    {
      time: '04:30 PM - 06:30 PM',
      type: 'poi',
      name: 'Bapu Bazaar Heritage Walk',
      category: 'Local Bazaar & Spice Market',
      trafficLight: 'YELLOW',
      matchReason: 'Vibrant local immersion, moderate walking crowds.',
      authenticity: '88%',
      isLocalGem: true,
    }
  ]);

  // Initial evaluation fetch
  useEffect(() => {
    loadBlendInEvaluation(currentScore);
  }, []);

  const loadBlendInEvaluation = async (score) => {
    try {
      setIsLoading(true);
      const evalPayload = {
        destination: destination,
        poi_list: schedule.filter(s => s.type === 'poi').map(p => ({
          name: p.name,
          category: p.category,
          authenticity_index: parseFloat(p.authenticity) / 100,
          tourist_density: 0.5,
          cultural_depth: 0.85,
          duration_minutes: 90,
          is_wheelchair_accessible: true
        })),
        restaurant_list: schedule.filter(s => s.type === 'food').map(f => ({
          name: f.name,
          cuisine: f.category,
          is_local_authentic: true,
          authentic_score: parseFloat(f.authenticity) / 100,
          dietary_options: ['Vegetarian']
        })),
        user_preferences: {
          food_preferences: ['Vegetarian'],
          handicap_accommodations: ['wheelchair_accessible'],
          elders_count: 1,
          habits: { pacing: 'moderate', walking_tolerance_km: 5 }
        },
        selected_attire_count: 2,
        etiquette_acknowledgement: true
      };

      const res = await blendinApi.evaluateItinerary(evalPayload);
      setCurrentScore(res.overall_score);
      setBreakdown(res.breakdown);
      setRecommendations(res.recommendations);
      setLocalComparison(res.local_comparison_percentile);
    } catch (err) {
      console.error('Error fetching blend-in evaluation:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTargetScoreChange = async (newTarget) => {
    setTargetScore(newTarget);
    setIsLoading(true);

    try {
      const optPayload = {
        destination: destination,
        current_score: currentScore,
        target_score: newTarget,
        candidate_pois: [
          { id: '1', name: 'Amber Palace & Fort', authenticity_index: 0.85, is_wheelchair_accessible: true },
          { id: '2', name: 'Anokhi Museum of Hand Printing', authenticity_index: 0.92, is_wheelchair_accessible: true },
          { id: '3', name: 'Bapu Bazaar Heritage Walk', authenticity_index: 0.88, is_wheelchair_accessible: false },
          { id: '4', name: 'Nahargarh Stepwell Sunset Point', authenticity_index: 0.95, is_wheelchair_accessible: true },
          { id: '5', name: 'Celebrity Wax Museum', authenticity_index: 0.15, is_wheelchair_accessible: true }
        ],
        current_selected_poi_ids: ['1', '2', '3'],
        user_preferences: {
          food_preferences: ['Vegetarian'],
          handicap_accommodations: ['wheelchair_accessible']
        }
      };

      const optResult = await blendinApi.optimizeForTarget(optPayload);
      setSuggestedSwaps(optResult.suggested_swaps || []);
      setCurrentScore(optResult.projected_score);

      // Re-evaluate breakdown for projected score
      await loadBlendInEvaluation(optResult.projected_score);
    } catch (err) {
      console.error('Error optimizing for target blend-in score:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Page Title & Controls */}
        <div className="flex flex-wrap items-center justify-between gap-4 bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
          <div>
            <h1 className="text-3xl font-extrabold text-gray-900">
              Trip Itinerary: {destination}
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              AI optimized for traffic constraints, weather safety, dietary comfort & cultural blend-in.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
              🟢 Highly Personalized
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800">
              🟡 Moderate Fit
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-100 text-rose-800">
              🔴 Constraint Alert
            </span>
          </div>
        </div>

        {/* Blend-In Score and Target Optimizer Widget */}
        <BlendinSlider
          currentScore={currentScore}
          targetScore={targetScore}
          breakdown={breakdown}
          recommendations={recommendations}
          suggestedSwaps={suggestedSwaps}
          localComparison={localComparison}
          isLoading={isLoading}
          onTargetChange={handleTargetScoreChange}
          destination={destination}
        />

        {/* Chronological Timeline */}
        <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-sm border border-gray-200">
          <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            📅 Day 1: Heritage & Cultural Discovery
          </h3>

          <div className="relative border-l-2 border-indigo-200 ml-4 space-y-8">
            {schedule.map((item, idx) => (
              <div key={idx} className="relative pl-6">
                {/* Timeline node marker */}
                <div
                  className={`absolute -left-[9px] top-1.5 w-4 h-4 rounded-full border-2 border-white ${
                    item.trafficLight === 'GREEN'
                      ? 'bg-emerald-500'
                      : item.trafficLight === 'YELLOW'
                      ? 'bg-amber-500'
                      : 'bg-rose-500'
                  }`}
                ></div>

                {/* Card Container */}
                <div className="bg-gray-50 hover:bg-slate-50 transition-colors p-5 rounded-xl border border-gray-200">
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                    <span className="text-xs font-bold text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-md">
                      ⏰ {item.time}
                    </span>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-gray-500">
                        Immersion: <strong className="text-gray-800">{item.authenticity}</strong>
                      </span>
                      {item.trafficLight === 'GREEN' && (
                        <span className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                          🟢 Best Match
                        </span>
                      )}
                      {item.trafficLight === 'YELLOW' && (
                        <span className="text-xs font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800">
                          🟡 Moderate
                        </span>
                      )}
                    </div>
                  </div>

                  <h4 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                    {item.type === 'food' ? '🍛' : '🏛️'} {item.name}
                    {item.isLocalGem && (
                      <span className="text-[10px] font-extrabold uppercase bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">
                        Local Gem
                      </span>
                    )}
                  </h4>

                  <p className="text-sm text-gray-600 mt-1">
                    {item.matchReason}
                  </p>

                  {item.attire && (
                    <div className="mt-3 text-xs text-indigo-800 bg-indigo-50/70 p-2.5 rounded-lg border border-indigo-100 flex items-center gap-1.5">
                      <span>👘</span>
                      <span><strong>Attire Advisory:</strong> {item.attire}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Itinerary;

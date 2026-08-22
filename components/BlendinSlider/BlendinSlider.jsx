import React, { useState, useEffect, useCallback } from 'react';
import './BlendinSlider.css';

/**
 * BlendinSlider Component
 * 
 * An interactive UX control and dashboard widget that:
 * 1. Displays current Blend-In Score (%) & Persona Tier.
 * 2. Provides an interactive slider for setting a Target Blend-in Score (0-100%).
 * 3. Shows dimensional breakdowns (Authenticity, Food, Pacing, Accessibility, Attire).
 * 4. Displays actionable recommendations and suggested POI swaps to achieve the target.
 * 5. Re-triggers the planning optimizer when the target is adjusted.
 */
export const BlendinSlider = ({
  currentScore = 65,
  targetScore = 65,
  breakdown = null,
  recommendations = [],
  suggestedSwaps = [],
  localComparison = 72,
  isLoading = false,
  onTargetChange = () => {},
  destination = 'Destination',
}) => {
  const [sliderValue, setSliderValue] = useState(targetScore);
  const [activeTab, setActiveTab] = useState('overview'); // 'overview' | 'breakdown' | 'tips' | 'swaps'

  useEffect(() => {
    setSliderValue(targetScore);
  }, [targetScore]);

  // Determine tier metadata from score
  const getTierInfo = (score) => {
    if (score >= 76) {
      return {
        tier: 'Local Insider',
        icon: '✨',
        color: '#8B5CF6',
        gradient: 'from-purple-500 to-indigo-600',
        bgLight: '#F5F3FF',
        tagline: 'Deeply integrated with native rhythms and hidden gems.',
      };
    } else if (score >= 51) {
      return {
        tier: 'Cultural Immersion',
        icon: '🕌',
        color: '#F59E0B',
        gradient: 'from-amber-500 to-orange-600',
        bgLight: '#FFFBEB',
        tagline: 'Rich heritage experiences, authentic dining, and cultural customs.',
      };
    } else if (score >= 26) {
      return {
        tier: 'Comfort Explorer',
        icon: '🧭',
        color: '#10B981',
        gradient: 'from-emerald-500 to-teal-600',
        bgLight: '#ECFDF5',
        tagline: 'Iconic landmarks combined with gentle local discoveries.',
      };
    } else {
      return {
        tier: 'Tourist Bubble',
        icon: '🏖️',
        color: '#3B82F6',
        gradient: 'from-blue-500 to-cyan-600',
        bgLight: '#EFF6FF',
        tagline: 'High-comfort standard sightseeing with zero cultural friction.',
      };
    }
  };

  const currentTier = getTierInfo(currentScore);
  const targetTier = getTierInfo(sliderValue);

  const handleSliderChange = (e) => {
    const newVal = Number(e.target.value);
    setSliderValue(newVal);
  };

  const handleSliderCommit = () => {
    if (onTargetChange) {
      onTargetChange(sliderValue);
    }
  };

  return (
    <div className="blendin-container bg-white rounded-2xl shadow-xl border border-gray-100 p-6 max-w-4xl mx-auto my-6 font-sans">
      {/* Header with Title and Persona Badge */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">{currentTier.icon}</span>
            <h2 className="text-2xl font-bold text-gray-900 tracking-tight">
              AI Blend-In Score
            </h2>
            <span className="bg-indigo-50 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full uppercase tracking-wider">
              AI Powered
            </span>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Quantifying cultural immersion, local authenticity & comfort in <span className="font-semibold text-gray-700">{destination}</span>
          </p>
        </div>

        {/* Current Score Badge */}
        <div className="flex items-center gap-3 bg-gray-50 px-4 py-2 rounded-xl border border-gray-200">
          <div className="text-right">
            <div className="text-xs text-gray-500 uppercase font-medium">Current Match</div>
            <div className="text-sm font-bold" style={{ color: currentTier.color }}>
              {currentTier.tier}
            </div>
          </div>
          <div
            className="w-12 h-12 rounded-full flex items-center justify-center text-white font-extrabold text-lg shadow-sm"
            style={{ backgroundColor: currentTier.color }}
          >
            {Math.round(currentScore)}%
          </div>
        </div>
      </div>

      {/* Target Blend-in Slider Card */}
      <div className="my-6 bg-gradient-to-r from-gray-50 to-slate-50 p-6 rounded-2xl border border-gray-200">
        <div className="flex flex-wrap justify-between items-center mb-3">
          <label className="text-base font-bold text-gray-800 flex items-center gap-2">
            🎯 Target Immersion Level:
            <span className="text-lg font-extrabold" style={{ color: targetTier.color }}>
              {sliderValue}% ({targetTier.tier})
            </span>
          </label>
          {sliderValue !== currentScore && (
            <span className="text-xs font-semibold px-2 py-1 rounded bg-amber-100 text-amber-800">
              {sliderValue > currentScore ? `+${sliderValue - currentScore}% Deeper Immersion` : `${sliderValue - currentScore}% More Comfort`}
            </span>
          )}
        </div>

        {/* Range Slider */}
        <div className="relative my-4">
          <input
            type="range"
            min="10"
            max="100"
            step="1"
            value={sliderValue}
            onChange={handleSliderChange}
            onMouseUp={handleSliderCommit}
            onTouchEnd={handleSliderCommit}
            className="blendin-range-slider w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600 transition-all"
          />
          {/* Ticks and Marker Labels */}
          <div className="flex justify-between text-xs text-gray-500 mt-2 font-medium">
            <span className="cursor-pointer" onClick={() => { setSliderValue(20); onTargetChange(20); }}>🏖️ Tourist (20%)</span>
            <span className="cursor-pointer" onClick={() => { setSliderValue(40); onTargetChange(40); }}>🧭 Explorer (40%)</span>
            <span className="cursor-pointer" onClick={() => { setSliderValue(65); onTargetChange(65); }}>🕌 Immersion (65%)</span>
            <span className="cursor-pointer" onClick={() => { setSliderValue(90); onTargetChange(90); }}>✨ Local Insider (90%)</span>
          </div>
        </div>

        {/* Action button if adjusted */}
        <div className="flex flex-wrap items-center justify-between gap-3 mt-4 pt-3 border-t border-gray-200">
          <p className="text-xs text-gray-600">
            {targetTier.tagline}
          </p>
          <button
            onClick={handleSliderCommit}
            disabled={isLoading}
            className={`px-5 py-2 rounded-xl text-white font-semibold text-sm shadow-md transition-all flex items-center gap-2 ${
              isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-700 active:scale-95'
            }`}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                Fine-Tuning Itinerary...
              </>
            ) : (
              <>🔄 Re-generate with {sliderValue}% Target</>
            )}
          </button>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="flex gap-2 border-b border-gray-100 pb-2 mb-6">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
            activeTab === 'overview'
              ? 'bg-indigo-50 text-indigo-700'
              : 'text-gray-500 hover:text-gray-800'
          }`}
        >
          📊 Immersion Overview
        </button>
        <button
          onClick={() => setActiveTab('breakdown')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
            activeTab === 'breakdown'
              ? 'bg-indigo-50 text-indigo-700'
              : 'text-gray-500 hover:text-gray-800'
          }`}
        >
          🧩 Dimension Breakdown
        </button>
        <button
          onClick={() => setActiveTab('tips')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
            activeTab === 'tips'
              ? 'bg-indigo-50 text-indigo-700'
              : 'text-gray-500 hover:text-gray-800'
          }`}
        >
          💡 Blend-In Tips ({recommendations.length})
        </button>
        {suggestedSwaps.length > 0 && (
          <button
            onClick={() => setActiveTab('swaps')}
            className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
              activeTab === 'swaps'
                ? 'bg-indigo-50 text-indigo-700'
                : 'text-gray-500 hover:text-gray-800'
            }`}
          >
            🔄 Suggested Swaps ({suggestedSwaps.length})
          </button>
        )}
      </div>

      {/* Tab 1: Overview */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Key Metrics Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 bg-purple-50 rounded-xl border border-purple-100">
              <div className="text-xs text-purple-700 font-bold uppercase tracking-wider">Local Comparison</div>
              <div className="text-2xl font-extrabold text-purple-900 mt-1">{localComparison}%</div>
              <div className="text-xs text-purple-600 mt-1">Relative to native resident rhythm</div>
            </div>

            <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-100">
              <div className="text-xs text-emerald-700 font-bold uppercase tracking-wider">Authenticity Index</div>
              <div className="text-2xl font-extrabold text-emerald-900 mt-1">
                {breakdown ? `${Math.round(breakdown.authenticity_score)}%` : `${Math.round(currentScore * 0.95)}%`}
              </div>
              <div className="text-xs text-emerald-600 mt-1">Heritage craft, markets & hidden gems</div>
            </div>

            <div className="p-4 bg-blue-50 rounded-xl border border-blue-100">
              <div className="text-xs text-blue-700 font-bold uppercase tracking-wider">Comfort & Adaptation</div>
              <div className="text-2xl font-extrabold text-blue-900 mt-1">
                {breakdown ? `${Math.round(breakdown.familiarity_score)}%` : '85%'}
              </div>
              <div className="text-xs text-blue-600 mt-1">Dietary, pacing & accessibility safety</div>
            </div>
          </div>

          {/* Quick Insights List */}
          <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
            <h4 className="text-sm font-bold text-gray-800 mb-2">🎯 Immersion Highlights for this Route</h4>
            <ul className="text-sm text-gray-600 space-y-1.5 list-disc list-inside">
              <li>Balanced mix of prominent heritage monuments and neighborhood artisan quarters.</li>
              <li>Meal stops feature authentic regional dishes aligned with your dietary requirements.</li>
              <li>Activity timing matches local morning commerce and evening cultural rituals.</li>
            </ul>
          </div>
        </div>
      )}

      {/* Tab 2: Dimension Breakdown */}
      {activeTab === 'breakdown' && (
        <div className="space-y-4">
          {breakdown && breakdown.dimensions && breakdown.dimensions.length > 0 ? (
            breakdown.dimensions.map((dim, idx) => (
              <div key={idx} className="p-4 bg-gray-50 rounded-xl border border-gray-200">
                <div className="flex justify-between items-center mb-1.5">
                  <span className="text-sm font-bold text-gray-800">{dim.name}</span>
                  <span className="text-sm font-extrabold text-indigo-600">{Math.round(dim.score)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                  <div
                    className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(100, Math.max(5, dim.score))}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500">{dim.description}</p>
                {dim.strengths && dim.strengths.length > 0 && (
                  <div className="mt-2 text-xs text-emerald-700 flex items-center gap-1">
                    <span>✓</span> {dim.strengths[0]}
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-400 text-sm">
              Generate an itinerary to view granular dimensional breakdown.
            </div>
          )}
        </div>
      )}

      {/* Tab 3: Actionable Blend-In Tips */}
      {activeTab === 'tips' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.length > 0 ? (
            recommendations.map((rec, idx) => (
              <div key={idx} className="p-4 rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold uppercase px-2 py-0.5 rounded bg-indigo-50 text-indigo-700">
                    {rec.category}
                  </span>
                  {rec.impact_score_boost > 0 && (
                    <span className="text-xs font-bold text-emerald-600">
                      +{rec.impact_score_boost}% Boost
                    </span>
                  )}
                </div>
                <h5 className="text-sm font-bold text-gray-900 mb-1">{rec.title}</h5>
                <p className="text-xs text-gray-600 leading-relaxed mb-2">{rec.description}</p>
                {rec.cultural_context && (
                  <div className="text-xs text-gray-500 italic bg-gray-50 p-2 rounded border-l-2 border-indigo-400">
                    💡 {rec.cultural_context}
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="col-span-2 text-center py-8 text-gray-400 text-sm">
              No specific blend-in tips needed for the current configuration.
            </div>
          )}
        </div>
      )}

      {/* Tab 4: Suggested Swaps */}
      {activeTab === 'swaps' && (
        <div className="space-y-3">
          <p className="text-xs text-gray-600 mb-3">
            Suggested attraction adjustments to reach your target {sliderValue}% blend-in level:
          </p>
          {suggestedSwaps.map((swap, idx) => (
            <div key={idx} className="p-4 bg-slate-50 rounded-xl border border-gray-200 flex flex-wrap items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2 text-sm">
                  <span className="line-through text-gray-400">{swap.current_poi_name}</span>
                  <span className="text-indigo-600 font-bold">➔</span>
                  <span className="font-bold text-gray-900">{swap.suggested_poi_name}</span>
                </div>
                <p className="text-xs text-gray-500">{swap.reason}</p>
              </div>
              <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-3 py-1.5 rounded-full">
                +{swap.blendin_score_delta}% Immersion
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BlendinSlider;

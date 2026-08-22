import React, { useState, useEffect } from 'react';
import culturalApi from '../../services/culturalApi';

export const CulturalGuide = () => {
  const [destination, setDestination] = useState('Jaipur');
  const [guideData, setGuideData] = useState(null);
  const [attireData, setAttireData] = useState(null);
  const [activeTab, setActiveTab] = useState('attire'); // 'attire' | 'etiquette' | 'dress_codes' | 'phrases'
  const [selectedAttireIds, setSelectedAttireIds] = useState(['att_raj_1']);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchGuideAndAttire(destination);
  }, [destination]);

  const fetchGuideAndAttire = async (dest) => {
    try {
      setIsLoading(true);
      const [guideRes, attireRes] = await Promise.all([
        culturalApi.getCulturalGuide(dest),
        culturalApi.getAttireRecommendations({
          destination: dest,
          temperature_celsius: 32.0,
          weather_condition: 'Sunny',
          planned_poi_categories: ['historic_temple', 'bazaar', 'fort']
        })
      ]);
      setGuideData(guideRes);
      setAttireData(attireRes);
    } catch (err) {
      console.error('Error fetching cultural guide:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleAttireSelection = (id) => {
    setSelectedAttireIds(prev =>
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  return (
    <div className="min-h-screen bg-slate-100 py-8 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-900 via-purple-900 to-slate-900 rounded-3xl p-8 text-white shadow-xl">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <span className="bg-indigo-500/30 text-indigo-200 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider border border-indigo-400/30">
                Cultural & Attire Guide
              </span>
              <h1 className="text-3xl sm:text-4xl font-extrabold mt-3 tracking-tight">
                {destination} Cultural Intelligence
              </h1>
              <p className="text-indigo-200 text-sm mt-2 max-w-2xl leading-relaxed">
                {guideData?.cultural_overview || 'Discover regional dress codes, sacred temple etiquette, and conversational phrases to blend in seamlessly.'}
              </p>
            </div>

            {/* Quick Readiness Badge */}
            <div className="bg-white/10 backdrop-blur-md px-5 py-4 rounded-2xl border border-white/20 text-center">
              <div className="text-xs uppercase tracking-wider text-indigo-200">Selected Attire</div>
              <div className="text-2xl font-black text-amber-300 mt-0.5">
                {selectedAttireIds.length} Outfits
              </div>
              <div className="text-[11px] text-emerald-300 font-medium mt-1">
                +{selectedAttireIds.length * 7.5}% Blend-In Boost
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl shadow-sm border border-gray-200">
          <button
            onClick={() => setActiveTab('attire')}
            className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all flex items-center gap-2 ${
              activeTab === 'attire'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            👘 Regional Attire ({attireData?.recommended_outfits?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab('dress_codes')}
            className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all flex items-center gap-2 ${
              activeTab === 'dress_codes'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            ⛩️ Temple & Site Dress Codes
          </button>
          <button
            onClick={() => setActiveTab('etiquette')}
            className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all flex items-center gap-2 ${
              activeTab === 'etiquette'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            🙏 Customs & Etiquette
          </button>
          <button
            onClick={() => setActiveTab('phrases')}
            className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all flex items-center gap-2 ${
              activeTab === 'phrases'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            🗣️ Local Phrasebook
          </button>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="bg-white rounded-2xl p-12 text-center shadow-sm">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-600 border-t-transparent"></div>
            <p className="text-gray-500 text-sm mt-3">Loading cultural guide and attire recommendations...</p>
          </div>
        )}

        {/* Tab 1: Regional Attire */}
        {!isLoading && activeTab === 'attire' && (
          <div className="space-y-6">
            {/* Weather advisory banner */}
            {attireData?.weather_summary && (
              <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-center gap-3 text-amber-900 text-sm">
                <span className="text-2xl">☀️</span>
                <div>
                  <strong>Weather Advisory:</strong> {attireData.weather_summary}
                </div>
              </div>
            )}

            {/* Attire Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {attireData?.recommended_outfits?.map((outfit) => {
                const isSelected = selectedAttireIds.includes(outfit.id);
                return (
                  <div
                    key={outfit.id}
                    className={`bg-white rounded-2xl p-6 border-2 transition-all shadow-sm hover:shadow-md flex flex-col justify-between ${
                      isSelected ? 'border-indigo-600 ring-2 ring-indigo-100' : 'border-gray-200'
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-2">
                        <span className="text-xs font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-md">
                          {outfit.category}
                        </span>
                        <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                          Modesty: {outfit.modesty_level}
                        </span>
                      </div>

                      <h3 className="text-lg font-bold text-gray-900 mt-1">{outfit.name}</h3>
                      {outfit.local_name && (
                        <p className="text-xs text-indigo-600 font-semibold mb-2">Local name: {outfit.local_name}</p>
                      )}

                      <p className="text-sm text-gray-600 leading-relaxed mb-4">{outfit.description}</p>

                      <div className="space-y-2 bg-gray-50 p-3.5 rounded-xl text-xs text-gray-700 mb-4">
                        <div><strong>🧵 Recommended Fabric:</strong> {outfit.fabric_recommendation}</div>
                        <div><strong>💡 Cultural Context:</strong> {outfit.cultural_significance}</div>
                      </div>
                    </div>

                    <button
                      onClick={() => toggleAttireSelection(outfit.id)}
                      className={`w-full py-2.5 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
                        isSelected
                          ? 'bg-emerald-600 text-white shadow-sm hover:bg-emerald-700'
                          : 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100'
                      }`}
                    >
                      {isSelected ? '✓ Added to My Cultural Attire' : '+ Select for Immersion (+7.5% Boost)'}
                    </button>
                  </div>
                );
              })}
            </div>

            {/* Packing Checklist */}
            {attireData?.packing_checklist && (
              <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
                <h4 className="text-base font-bold text-gray-900 mb-3 flex items-center gap-2">
                  🧳 Cultural Packing Checklist for {destination}
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {attireData.packing_checklist.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-sm text-gray-700 bg-slate-50 p-2.5 rounded-xl border border-gray-100">
                      <span className="text-indigo-600 font-bold">✓</span> {item}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Site Dress Codes */}
        {!isLoading && activeTab === 'dress_codes' && (
          <div className="space-y-4">
            {guideData?.site_dress_codes?.map((code, idx) => (
              <div key={idx} className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-gray-100 pb-3">
                  <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                    🏛️ {code.site_name}
                  </h3>
                  <span
                    className={`text-xs font-extrabold uppercase px-3 py-1 rounded-full ${
                      code.requirement_level === 'strict'
                        ? 'bg-rose-100 text-rose-800'
                        : 'bg-amber-100 text-amber-800'
                    }`}
                  >
                    {code.requirement_level === 'strict' ? '⚠️ Strict Entry Rules' : 'Recommended Dress'}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <h5 className="font-bold text-gray-800 mb-2">📋 Mandatory Rules:</h5>
                    <ul className="space-y-1.5 list-disc list-inside text-gray-600">
                      {code.mandatory_rules.map((r, rIdx) => (
                        <li key={rIdx}>{r}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h5 className="font-bold text-gray-800 mb-2">👟 Footwear & Accessories Policy:</h5>
                    <p className="text-gray-600 text-xs leading-relaxed bg-gray-50 p-3 rounded-xl border border-gray-100">
                      {code.shoe_policy}
                    </p>
                    {code.prohibited_items.length > 0 && (
                      <div className="mt-2 text-xs text-rose-700 bg-rose-50 p-2.5 rounded-xl border border-rose-100">
                        <strong>🚫 Prohibited:</strong> {code.prohibited_items.join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab 3: Customs & Etiquette */}
        {!isLoading && activeTab === 'etiquette' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {guideData?.etiquette_rules?.map((rule, idx) => (
              <div key={idx} className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-3">
                <h4 className="text-base font-bold text-gray-900 flex items-center gap-2">
                  ✨ {rule.title}
                </h4>
                <p className="text-xs text-gray-600">{rule.description}</p>

                <div className="space-y-2 pt-2">
                  {rule.dos.map((d, dIdx) => (
                    <div key={dIdx} className="text-xs text-emerald-800 bg-emerald-50 p-2.5 rounded-xl flex items-start gap-2">
                      <span className="font-bold">✓ DO:</span> {d}
                    </div>
                  ))}
                  {rule.donts.map((d, dIdx) => (
                    <div key={dIdx} className="text-xs text-rose-800 bg-rose-50 p-2.5 rounded-xl flex items-start gap-2">
                      <span className="font-bold">✕ DON'T:</span> {d}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab 4: Phrasebook */}
        {!isLoading && activeTab === 'phrases' && (
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-4">
            <h3 className="text-lg font-bold text-gray-900 mb-2">
              🗣️ Essential Conversational Phrases ({guideData?.primary_languages?.join(', ')})
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {guideData?.essential_phrases?.map((phrase, idx) => (
                <div key={idx} className="p-4 rounded-xl border border-gray-200 bg-slate-50 hover:bg-indigo-50/50 transition-colors">
                  <div className="text-xs font-bold text-indigo-700 uppercase tracking-wider mb-1">
                    {phrase.phrase}
                  </div>
                  <div className="text-xl font-black text-gray-900 my-1">{phrase.native_script}</div>
                  <div className="text-sm font-semibold text-purple-700">Pronounce: "{phrase.phonetic_pronunciation}"</div>
                  <div className="text-[11px] text-gray-500 mt-2 italic">Context: {phrase.context}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CulturalGuide;

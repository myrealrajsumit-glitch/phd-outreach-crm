import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Sparkles, Search, GraduationCap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const Navbar = () => {
  const { user } = useAuth();
  const [health, setHealth] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await api.get('/health');
        setHealth(res.data);
      } catch (err) {
        console.error("Health check error:", err);
      }
    };
    checkHealth();
  }, []);

  const handleSearch = (e) => {
    if (e.key === 'Enter') {
      navigate(`/professors?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <header className="h-16 bg-[#F6F8FC] border-b border-slate-200 px-6 flex items-center justify-between gap-4 sticky top-0 z-30">
      {/* Brand & App Title */}
      <div className="flex items-center gap-3 shrink-0">
        <div className="w-10 h-10 rounded-2xl bg-blue-600 text-white flex items-center justify-center font-bold text-lg shadow-sm">
          <GraduationCap className="w-6 h-6" />
        </div>
        <div>
          <h1 className="font-bold text-slate-900 text-sm tracking-tight flex items-center gap-2">
            PhD Research Mail
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 border border-blue-200">
              Personal Workspace
            </span>
          </h1>
          <p className="text-[11px] text-slate-500">
            Evidence-Grounded Faculty Cold Outreach & Follow-Up Engine
          </p>
        </div>
      </div>

      {/* Gmail-Style Centered Search Bar */}
      <div className="flex-1 max-w-xl mx-4 hidden sm:block">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3.5 top-2.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search faculty, universities, papers, or outreach status... (Press Enter)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleSearch}
            className="w-full pl-10 pr-4 py-2 text-xs bg-[#EAF1FB] hover:bg-[#E2ECF9] focus:bg-white text-slate-800 placeholder:text-slate-500 rounded-full border border-transparent focus:border-blue-400 focus:outline-none focus:shadow-sm transition-all"
          />
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3 shrink-0">
        {/* Gemini Engine Status Pill */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold bg-white border border-slate-200 text-slate-700 shadow-2xs">
          <Sparkles className="w-3.5 h-3.5 text-blue-600 animate-pulse" />
          <span>Gemini 3.6 Flash</span>
          <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span className="text-[10px] text-slate-400">({health?.active_gemini_keys || 6} keys)</span>
        </div>

        {/* Candidate Profile Avatar */}
        {user && (
          <div 
            onClick={() => navigate('/settings')}
            className="flex items-center gap-2.5 pl-2 cursor-pointer hover:opacity-85 transition-opacity"
            title="Account & Outreach Settings"
          >
            <div className="text-right hidden md:block">
              <div className="text-xs font-bold text-slate-800">{user.full_name}</div>
              <div className="text-[10px] text-slate-500">{user.target_field || 'PhD Aspirant'}</div>
            </div>
            <div className="w-9 h-9 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs shadow-sm ring-2 ring-blue-100">
              {user.full_name ? user.full_name.charAt(0) : 'S'}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;

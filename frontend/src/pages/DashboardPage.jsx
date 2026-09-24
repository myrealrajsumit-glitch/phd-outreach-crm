import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCompose } from '../context/ComposeContext';
import { 
  Users, 
  Send, 
  Clock, 
  MessageSquareCheck, 
  TrendingUp, 
  Sparkles, 
  Plus, 
  Mail,
  RotateCw,
  Building,
  CheckCircle2
} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { openCompose } = useCompose();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/stats/dashboard');
        setStats(res.data);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const overview = stats?.overview || {};
  const funnel = stats?.funnel || {};
  const recent = stats?.recent_activity || [];

  const statCards = [
    { label: 'Target Faculty', val: overview.total_professors || 0, icon: Users, color: 'text-blue-700 bg-blue-50 border-blue-200' },
    { label: 'Emails Dispatched', val: overview.total_sent || 0, icon: Send, color: 'text-emerald-700 bg-emerald-50 border-emerald-200' },
    { label: 'Queued / Staggered', val: overview.total_scheduled || 0, icon: Clock, color: 'text-amber-800 bg-amber-50 border-amber-200' },
    { label: 'Replies Logged', val: overview.total_replied || 0, icon: MessageSquareCheck, color: 'text-indigo-800 bg-indigo-50 border-indigo-200' },
    { label: 'Response Rate', val: `${overview.reply_rate_percent || 0}%`, icon: TrendingUp, color: 'text-violet-800 bg-violet-50 border-violet-200' },
  ];

  return (
    <div className="space-y-6">
      {/* Top Welcome & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-slate-900">
            Outreach Dashboard
          </h2>
          <p className="text-xs text-slate-500">
            PhD Candidate Funnel & Evidence-Grounded Research Outreach
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => openCompose({ mode: 'new' })}
            className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-sm flex items-center gap-1.5 transition-all"
          >
            <Mail className="w-4 h-4" />
            <span>Compose Email</span>
          </button>
          <button
            onClick={() => navigate('/professors?new=true')}
            className="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-xs font-semibold shadow-2xs flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4 text-blue-600" />
            <span>Add Professor</span>
          </button>
        </div>
      </div>

      {/* Top 5 Stat Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
        {statCards.map((card, i) => {
          const Icon = card.icon;
          return (
            <div key={i} className="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs flex flex-col justify-between">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-slate-600">{card.label}</span>
                <div className={`p-1.5 rounded-lg border ${card.color}`}>
                  <Icon className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-2xl font-extrabold text-slate-900 tracking-tight">
                {card.val}
              </div>
            </div>
          );
        })}
      </div>

      {/* Recruitment Pipeline Funnel */}
      <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-2xs">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Application Pipeline Funnel</h3>
            <p className="text-xs text-slate-500">Stages from faculty discovery to advisor interview</p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700">
            Daily Cap: {overview.daily_velocity_limit || 25} emails/day
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5">
          {[
            { key: 'Identified', label: '1. Identified', count: funnel.Identified || 0, color: 'bg-slate-50 text-slate-800 border-slate-200' },
            { key: 'Reviewing', label: '2. Reviewing', count: funnel.Reviewing || 0, color: 'bg-sky-50 text-sky-900 border-sky-200' },
            { key: 'Draft_Ready', label: '3. Draft Ready', count: funnel.Draft_Ready || 0, color: 'bg-violet-50 text-violet-900 border-violet-200' },
            { key: 'Scheduled', label: '4. Queued', count: funnel.Scheduled || 0, color: 'bg-amber-50 text-amber-900 border-amber-200' },
            { key: 'Sent', label: '5. Sent', count: funnel.Sent || 0, color: 'bg-indigo-50 text-indigo-900 border-indigo-200' },
            { key: 'Replied', label: '6. Replied', count: funnel.Replied || 0, color: 'bg-emerald-50 text-emerald-900 border-emerald-200' },
            { key: 'Interview', label: '7. Interview', count: funnel.Interview || 0, color: 'bg-teal-50 text-teal-900 border-teal-200 font-bold' },
          ].map((col) => (
            <div
              key={col.key}
              onClick={() => navigate(`/pipeline`)}
              className={`p-3.5 rounded-xl cursor-pointer hover:shadow-xs transition-all flex flex-col justify-between border ${col.color}`}
            >
              <div className="text-[11px] font-bold">{col.label}</div>
              <div className="text-2xl font-extrabold mt-1">{col.count}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Professors & Co-Pilot Box */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Recent Professors Table */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-white border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900">Recent Faculty in Pipeline</h3>
            <button
              onClick={() => navigate('/professors')}
              className="text-xs text-blue-600 font-bold hover:underline"
            >
              View All ({overview.total_professors || 0})
            </button>
          </div>

          <div className="divide-y divide-slate-100">
            {recent.map((prof) => (
              <div
                key={prof.id}
                onClick={() => navigate(`/professors/${prof.id}`)}
                className="py-3 flex items-center justify-between hover:bg-slate-50/80 px-2 rounded-xl cursor-pointer transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center font-bold text-xs">
                    {prof.name.charAt(0)}
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-900">{prof.name}</div>
                    <div className="text-[11px] text-slate-500 flex items-center gap-1">
                      <Building className="w-3 h-3 text-slate-400" />
                      <span className="font-semibold text-blue-900">{prof.institution}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                  {prof.match_score > 0 && (
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200">
                      {prof.match_score}/10 Match
                    </span>
                  )}
                  <button
                    onClick={() => openCompose({
                      professorId: prof.id,
                      professorName: prof.name,
                      institution: prof.institution,
                      mode: 'new'
                    })}
                    className="px-2.5 py-1 rounded-lg bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 text-[11px] font-bold flex items-center gap-1"
                  >
                    <Mail className="w-3 h-3" />
                    <span>Email</span>
                  </button>
                  <button
                    onClick={() => openCompose({
                      professorId: prof.id,
                      professorName: prof.name,
                      institution: prof.institution,
                      mode: 'follow_up',
                      followUpStage: 1
                    })}
                    className="px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 hover:bg-amber-100 border border-amber-200 text-[11px] font-bold flex items-center gap-1"
                  >
                    <RotateCw className="w-3 h-3" />
                    <span>Follow-Up</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Co-Pilot Summary Card */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-blue-700 font-bold text-sm mb-2">
              <Sparkles className="w-4 h-4 text-blue-600" />
              <span>Grounded AI Outreach Assistant</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed mb-4">
              Compose initial inquiries or generate automated follow-ups with one click. Gemini uses your candidate profile and the faculty member's actual papers to write scholarly cold emails.
            </p>
            <div className="space-y-2 text-xs text-slate-700">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>One-click Gmail copy-paste support</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Automated 7-day & 14-day follow-up templates</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Zero hallucination: grounded in real publications</span>
              </div>
            </div>
          </div>

          <button
            onClick={() => openCompose({ mode: 'new' })}
            className="w-full mt-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-sm flex items-center justify-center gap-2 transition-all"
          >
            <Mail className="w-3.5 h-3.5" />
            <span>Open Email Composer</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { useCompose } from '../../context/ComposeContext';
import { 
  Plus, 
  PenSquare, 
  Users, 
  Inbox, 
  Send, 
  Clock, 
  MessageSquareCheck, 
  BellRing, 
  Kanban, 
  FileText, 
  Settings, 
  Sparkles,
  LayoutDashboard
} from 'lucide-react';
import api from '../../services/api';

const Sidebar = () => {
  const { openCompose } = useCompose();
  const [counts, setCounts] = useState({
    total: 0,
    reviewing: 0,
    drafts: 0,
    sent: 0,
    followUps: 0,
    replied: 0
  });

  useEffect(() => {
    const fetchCounts = async () => {
      try {
        const res = await api.get('/stats/dashboard');
        const overview = res.data?.overview || {};
        const funnel = res.data?.funnel || {};
        setCounts({
          total: overview.total_professors || 0,
          reviewing: funnel.Reviewing || 0,
          drafts: funnel.Draft_Ready || 0,
          sent: overview.total_sent || 0,
          followUps: funnel.Scheduled || 0,
          replied: overview.total_replied || 0
        });
      } catch (err) {
        // silent fallback
      }
    };
    fetchCounts();
  }, []);

  const navItems = [
    { to: '/', label: 'Overview', icon: LayoutDashboard },
    { to: '/professors', label: 'All Faculty', icon: Users, badge: counts.total, badgeColor: 'bg-slate-200 text-slate-800' },
    { to: '/pipeline', label: 'Pipeline Kanban', icon: Kanban },
    { to: '/emails?tab=Draft', label: 'Drafts', icon: PenSquare, badge: counts.drafts, badgeColor: 'bg-blue-100 text-blue-800' },
    { to: '/emails?tab=Sent', label: 'Sent Outreach', icon: Send, badge: counts.sent, badgeColor: 'bg-emerald-100 text-emerald-800' },
    { to: '/emails?tab=FollowUp', label: 'Follow-Ups Due', icon: BellRing, badge: counts.followUps || 0, badgeColor: 'bg-amber-100 text-amber-900 font-bold' },
    { to: '/templates', label: 'Email Templates', icon: FileText },
    { to: '/settings', label: 'Settings & SMTP', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#F6F8FC] border-r border-slate-200/80 flex flex-col justify-between shrink-0 min-h-[calc(100vh-4rem)] p-3">
      <div className="space-y-4">
        {/* Prominent Gmail-Style Compose Button */}
        <div className="px-2 pt-2">
          <button
            type="button"
            onClick={() => openCompose({ mode: 'new' })}
            className="w-full py-3.5 px-5 rounded-2xl bg-[#C2E7FF] hover:bg-[#B3DDF6] text-[#001D35] font-bold text-sm shadow-sm hover:shadow-md transition-all flex items-center gap-3 group border border-[#A4D5F8]"
          >
            <div className="p-1 rounded-lg bg-white/80 text-blue-700 group-hover:scale-110 transition-transform">
              <PenSquare className="w-4 h-4 text-blue-600" />
            </div>
            <span>Compose Email</span>
          </button>
        </div>

        {/* Navigation List */}
        <nav className="space-y-0.5 pt-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) =>
                  `flex items-center justify-between px-4 py-2.5 rounded-full text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-[#D3E3FD] text-[#041E49] font-bold'
                      : 'text-slate-700 hover:bg-slate-200/60 hover:text-slate-900'
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-4 h-4 shrink-0 text-slate-600" />
                  <span>{item.label}</span>
                </div>
                {item.badge !== undefined && item.badge > 0 && (
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${item.badgeColor || 'bg-slate-200 text-slate-700'}`}>
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* AI Assistant Mini Card */}
      <div className="p-3.5 m-1 rounded-2xl bg-white border border-slate-200 text-xs shadow-2xs">
        <div className="flex items-center gap-2 font-bold text-blue-700 text-xs mb-1">
          <Sparkles className="w-3.5 h-3.5 text-blue-600 animate-pulse" />
          <span>Gemini AI Assistant</span>
        </div>
        <p className="text-slate-600 text-[11px] leading-relaxed">
          Click <strong>Compose Email</strong> or any faculty member to draft an initial cold email or take an automated follow-up.
        </p>
      </div>
    </aside>
  );
};

export default Sidebar;

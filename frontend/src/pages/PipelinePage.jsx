import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Plus, 
  Sparkles, 
  Mail, 
  ExternalLink, 
  MoreVertical, 
  ChevronRight,
  ChevronLeft,
  Building,
  GraduationCap
} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

const STAGES = [
  { key: 'Identified', label: 'Identified', color: 'border-slate-300 dark:border-slate-700' },
  { key: 'Reviewing', label: 'Reviewing', color: 'border-sky-400 dark:border-sky-600' },
  { key: 'Draft_Ready', label: 'Draft Ready', color: 'border-violet-400 dark:border-violet-600' },
  { key: 'Scheduled', label: 'Queued', color: 'border-amber-400 dark:border-amber-600' },
  { key: 'Sent', label: 'Sent', color: 'border-indigo-400 dark:border-indigo-600' },
  { key: 'Replied', label: 'Replied', color: 'border-emerald-400 dark:border-emerald-600' },
  { key: 'Interview', label: 'Interview', color: 'border-teal-400 dark:border-teal-600' }
];

const PipelinePage = () => {
  const [professors, setProfessors] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchProfessors = async () => {
    try {
      const res = await api.get('/professors');
      setProfessors(res.data);
    } catch (err) {
      console.error("Error fetching pipeline:", err);
      toast.error("Failed to load pipeline.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfessors();
  }, []);

  const moveStage = async (profId, newStage, e) => {
    e.stopPropagation();
    try {
      await api.put(`/professors/${profId}`, { status: newStage });
      setProfessors(prev =>
        prev.map(p => (p.id === profId ? { ...p, status: newStage } : p))
      );
      toast.success(`Moved to ${newStage.replace('_', ' ')}`);
    } catch (err) {
      console.error(err);
      toast.error("Failed to update status.");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Outreach Pipeline Kanban
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Track and advance candidate outreach across 7 progressive recruitment stages
          </p>
        </div>
        <button
          onClick={() => navigate('/professors?new=true')}
          className="px-3.5 py-2 rounded-xl bg-primary-600 hover:bg-primary-700 text-white text-xs font-semibold shadow-sm flex items-center gap-1.5 transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>New Professor</span>
        </button>
      </div>

      {/* Kanban Horizontal Scroll Container */}
      <div className="flex gap-4 overflow-x-auto pb-6 pt-2">
        {STAGES.map((stage, colIdx) => {
          const items = professors.filter(p => p.status === stage.key);
          return (
            <div
              key={stage.key}
              className={`w-72 shrink-0 rounded-2xl bg-slate-100/70 dark:bg-slate-900/60 border-t-4 ${stage.color} p-3.5 flex flex-col max-h-[calc(100vh-14rem)]`}
            >
              {/* Column Header */}
              <div className="flex items-center justify-between mb-3 px-1">
                <span className="text-xs font-bold text-slate-800 dark:text-slate-200">
                  {stage.label}
                </span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-semibold shadow-2xs">
                  {items.length}
                </span>
              </div>

              {/* Cards List */}
              <div className="flex-1 overflow-y-auto space-y-3 pr-1">
                {items.length === 0 ? (
                  <div className="text-center py-8 text-[11px] text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-xl">
                    No faculty
                  </div>
                ) : (
                  items.map(prof => (
                    <div
                      key={prof.id}
                      onClick={() => navigate(`/professors/${prof.id}`)}
                      className="p-3.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 shadow-xs hover:shadow-md transition-all cursor-pointer group"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                          {prof.name}
                        </h4>
                        {prof.match_score > 0 && (
                          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300">
                            {prof.match_score}
                          </span>
                        )}
                      </div>

                      <div className="text-[11px] text-slate-500 dark:text-slate-400 flex items-center gap-1 mt-1">
                        <Building className="w-3 h-3 shrink-0" />
                        <span className="truncate">{prof.institution}</span>
                      </div>

                      {prof.research_topics && (
                        <div className="mt-2 text-[10px] text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-900/50 p-1.5 rounded-lg line-clamp-2">
                          {prof.research_topics}
                        </div>
                      )}

                      <div className="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-700/60 flex items-center justify-between text-[11px]">
                        <span className="text-slate-400 text-[10px]">
                          {prof.papers?.length || 0} papers
                        </span>

                        {/* Stage Progression Buttons */}
                        <div className="flex items-center gap-1">
                          {colIdx > 0 && (
                            <button
                              onClick={(e) => moveStage(prof.id, STAGES[colIdx - 1].key, e)}
                              className="p-1 rounded text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700"
                              title={`Back to ${STAGES[colIdx - 1].label}`}
                            >
                              <ChevronLeft className="w-3.5 h-3.5" />
                            </button>
                          )}
                          {colIdx < STAGES.length - 1 && (
                            <button
                              onClick={(e) => moveStage(prof.id, STAGES[colIdx + 1].key, e)}
                              className="p-1 rounded text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-950"
                              title={`Advance to ${STAGES[colIdx + 1].label}`}
                            >
                              <ChevronRight className="w-3.5 h-3.5" />
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default PipelinePage;

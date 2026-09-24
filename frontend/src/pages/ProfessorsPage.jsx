import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useCompose } from '../context/ComposeContext';
import { 
  Plus, 
  Search, 
  Filter, 
  ExternalLink, 
  Sparkles, 
  Building, 
  GraduationCap, 
  Mail, 
  RotateCw,
  Trash2, 
  ChevronRight,
  X
} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

const ProfessorsPage = () => {
  const [professors, setProfessors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [showAddModal, setShowAddModal] = useState(false);
  const [analyzingId, setAnalyzingId] = useState(null);

  const navigate = useNavigate();
  const location = useLocation();
  const { openCompose } = useCompose();

  // New professor form state
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    institution: '',
    department: 'Computer Science',
    title: 'Associate Professor',
    homepage_url: '',
    lab_url: '',
    country: 'USA',
    research_topics: '',
    accepting_students: 'Unknown',
    initial_paper_title: '',
    initial_paper_abstract: ''
  });

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.get('new') === 'true') {
      setShowAddModal(true);
    }
    if (params.get('search')) {
      setSearch(params.get('search'));
    }
  }, [location]);

  const fetchProfessors = async () => {
    try {
      const res = await api.get('/professors', {
        params: {
          search: search || undefined,
          status: statusFilter !== 'All' ? statusFilter : undefined
        }
      });
      setProfessors(res.data);
    } catch (err) {
      console.error(err);
      toast.error("Failed to load professors.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfessors();
  }, [search, statusFilter]);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        name: formData.name,
        email: formData.email,
        institution: formData.institution,
        department: formData.department,
        title: formData.title,
        homepage_url: formData.homepage_url,
        lab_url: formData.lab_url,
        country: formData.country,
        research_topics: formData.research_topics,
        accepting_students: formData.accepting_students,
        papers: formData.initial_paper_title ? [
          {
            title: formData.initial_paper_title,
            abstract: formData.initial_paper_abstract,
            year: 2024
          }
        ] : []
      };

      await api.post('/professors', payload);
      toast.success("Professor added to pipeline!");
      setShowAddModal(false);
      setFormData({
        name: '',
        email: '',
        institution: '',
        department: 'Computer Science',
        title: 'Associate Professor',
        homepage_url: '',
        lab_url: '',
        country: 'USA',
        research_topics: '',
        accepting_students: 'Unknown',
        initial_paper_title: '',
        initial_paper_abstract: ''
      });
      fetchProfessors();
    } catch (err) {
      console.error(err);
      toast.error(err.response?.data?.detail || "Failed to create professor.");
    }
  };

  const handleRunAiReview = async (profId, e) => {
    e.stopPropagation();
    setAnalyzingId(profId);
    try {
      const res = await api.post('/ai/review', { professor_id: profId });
      toast.success(`AI Review Complete! Match: ${res.data.match_score}/10`);
      fetchProfessors();
    } catch (err) {
      console.error(err);
      toast.error("AI synthesis failed.");
    } finally {
      setAnalyzingId(null);
    }
  };

  const handleOpenCompose = (prof, e) => {
    e.stopPropagation();
    openCompose({
      professorId: prof.id,
      professorName: prof.name,
      institution: prof.institution,
      recipientEmail: prof.email,
      mode: 'new'
    });
  };

  const handleOpenFollowUp = (prof, e) => {
    e.stopPropagation();
    openCompose({
      professorId: prof.id,
      professorName: prof.name,
      institution: prof.institution,
      recipientEmail: prof.email,
      mode: 'follow_up',
      followUpStage: 1
    });
  };

  const handleDelete = async (profId, e) => {
    e.stopPropagation();
    if (!window.confirm("Remove this professor from your pipeline?")) return;
    try {
      await api.delete(`/professors/${profId}`);
      toast.success("Professor removed.");
      setProfessors(prev => prev.filter(p => p.id !== profId));
    } catch (err) {
      toast.error("Failed to delete professor.");
    }
  };

  return (
    <div className="space-y-5">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
            Target Faculty Directory
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800">
              {professors.length} professors
            </span>
          </h2>
          <p className="text-xs text-slate-500">
            Select any professor to review publications, compose tailored emails, or take follow-ups
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
            onClick={() => setShowAddModal(true)}
            className="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-xs font-semibold shadow-2xs flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4 text-blue-600" />
            <span>Add Professor</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3.5 top-2.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search by faculty name, university, or research topic..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 text-xs bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 shadow-2xs placeholder:text-slate-400"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 text-xs bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-700 font-medium shadow-2xs"
          >
            <option value="All">All Stages</option>
            <option value="Identified">Identified</option>
            <option value="Reviewing">Reviewing</option>
            <option value="Draft_Ready">Draft Ready</option>
            <option value="Scheduled">Queued</option>
            <option value="Sent">Sent</option>
            <option value="Replied">Replied</option>
            <option value="Interview">Interview</option>
          </select>
        </div>
      </div>

      {/* Professors White Table */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center h-48">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : professors.length === 0 ? (
          <div className="text-center py-16 px-4">
            <GraduationCap className="w-10 h-10 mx-auto text-slate-300 mb-2" />
            <h3 className="text-sm font-semibold text-slate-700">No professors found</h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1">
              Add professors you are interested in applying to or adjust your search.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#F8FAFC] border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                <tr>
                  <th className="px-5 py-3.5">Professor & Institution</th>
                  <th className="px-4 py-3.5">Lab Focus / Topics</th>
                  <th className="px-4 py-3.5">Stage</th>
                  <th className="px-4 py-3.5">AI Match</th>
                  <th className="px-4 py-3.5">Papers</th>
                  <th className="px-5 py-3.5 text-right">Outreach Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {professors.map((prof) => (
                  <tr
                    key={prof.id}
                    onClick={() => navigate(`/professors/${prof.id}`)}
                    className="hover:bg-[#F2F6FC]/60 transition-colors cursor-pointer group"
                  >
                    <td className="px-5 py-3.5">
                      <div className="font-bold text-slate-900 text-sm group-hover:text-blue-600 transition-colors">
                        {prof.name}
                      </div>
                      <div className="text-[11px] text-slate-600 flex items-center gap-1.5 mt-0.5">
                        <Building className="w-3 h-3 text-slate-400" />
                        <span className="font-semibold text-blue-900">{prof.institution}</span>
                        {prof.department && <span className="text-slate-300">•</span>}
                        <span>{prof.department}</span>
                      </div>
                    </td>

                    <td className="px-4 py-3.5 max-w-xs">
                      <div className="text-slate-700 truncate font-mono text-[11px]">
                        {prof.research_topics || 'Not specified'}
                      </div>
                    </td>

                    <td className="px-4 py-3.5">
                      <span className={`px-2.5 py-1 rounded-full text-[11px] font-bold border ${
                        prof.status === 'Sent' ? 'bg-emerald-50 text-emerald-800 border-emerald-200' :
                        prof.status === 'Replied' ? 'bg-teal-50 text-teal-800 border-teal-200' :
                        prof.status === 'Draft_Ready' ? 'bg-violet-50 text-violet-800 border-violet-200' :
                        prof.status === 'Reviewing' ? 'bg-sky-50 text-sky-800 border-sky-200' :
                        'bg-slate-100 text-slate-700 border-slate-200'
                      }`}>
                        {prof.status}
                      </span>
                    </td>

                    <td className="px-4 py-3.5">
                      {prof.match_score > 0 ? (
                        <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                          {prof.match_score}/10
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px]">Not reviewed</span>
                      )}
                    </td>

                    <td className="px-4 py-3.5 text-slate-600 font-semibold">
                      {prof.papers?.length || 0}
                    </td>

                    <td className="px-5 py-3.5 text-right">
                      <div className="flex items-center justify-end gap-1.5" onClick={(e) => e.stopPropagation()}>
                        {/* Compose Email Button */}
                        <button
                          onClick={(e) => handleOpenCompose(prof, e)}
                          className="px-2.5 py-1 rounded-lg bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 text-[11px] font-bold flex items-center gap-1 transition-all"
                          title="Compose email to this professor"
                        >
                          <Mail className="w-3 h-3 text-blue-600" />
                          <span>Compose</span>
                        </button>

                        {/* Follow-Up Button */}
                        <button
                          onClick={(e) => handleOpenFollowUp(prof, e)}
                          className="px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 hover:bg-amber-100 border border-amber-200 text-[11px] font-bold flex items-center gap-1 transition-all"
                          title="Take follow-up with this professor"
                        >
                          <RotateCw className="w-3 h-3 text-amber-600" />
                          <span>Follow-Up</span>
                        </button>

                        {/* AI Review Button */}
                        <button
                          onClick={(e) => handleRunAiReview(prof.id, e)}
                          disabled={analyzingId === prof.id}
                          className="p-1.5 rounded-lg text-indigo-600 hover:bg-indigo-50 border border-transparent hover:border-indigo-200 transition-all"
                          title="Run Gemini AI paper review"
                        >
                          <Sparkles className="w-3.5 h-3.5" />
                        </button>

                        {/* Delete Button */}
                        <button
                          onClick={(e) => handleDelete(prof.id, e)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                          title="Delete Professor"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add Professor Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-xs p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 border border-slate-200 shadow-2xl my-8">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Plus className="w-4 h-4 text-blue-600" />
                <span>Add Target Professor</span>
              </h3>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    Professor Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white text-slate-800"
                    placeholder="e.g. Dr. Yann LeCun"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white text-slate-800"
                    placeholder="yann@cs.nyu.edu"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    University / Institution *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.institution}
                    onChange={(e) => setFormData({ ...formData, institution: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white text-slate-800"
                    placeholder="New York University"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    Department
                  </label>
                  <input
                    type="text"
                    value={formData.department}
                    onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white text-slate-800"
                    placeholder="Computer Science"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">
                  Research Topics / Keywords
                </label>
                <input
                  type="text"
                  value={formData.research_topics}
                  onChange={(e) => setFormData({ ...formData, research_topics: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white text-slate-800"
                  placeholder="e.g. Energy-Based Models, Self-Supervised Learning, Computer Vision"
                />
              </div>

              <div className="pt-2 border-t border-slate-100">
                <div className="text-[11px] font-bold text-slate-800 mb-1 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                  <span>Attach Recent Publication (For AI Grounding)</span>
                </div>
                <input
                  type="text"
                  value={formData.initial_paper_title}
                  onChange={(e) => setFormData({ ...formData, initial_paper_title: e.target.value })}
                  className="w-full px-3 py-2 mb-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white text-slate-800"
                  placeholder="Paper Title (e.g. A Path Towards Autonomous Machine Intelligence)"
                />
                <textarea
                  rows={3}
                  value={formData.initial_paper_abstract}
                  onChange={(e) => setFormData({ ...formData, initial_paper_abstract: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white text-slate-800"
                  placeholder="Paste Paper Abstract here so Gemini can extract methodology and research gaps..."
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 font-semibold hover:bg-slate-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold shadow-xs"
                >
                  Save Professor
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfessorsPage;

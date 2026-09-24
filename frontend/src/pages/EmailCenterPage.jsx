import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useCompose } from '../context/ComposeContext';
import { 
  Mail, 
  Send, 
  RotateCw, 
  CheckCircle, 
  CheckCircle2,
  Copy, 
  Trash2, 
  Clock, 
  Building,
  Check,
  Eye,
  Search,
  History,
  Sparkles,
  X,
  ExternalLink
} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

const EmailCenterPage = () => {
  const [emails, setEmails] = useState([]);
  const [professors, setProfessors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get('tab') || 'All';
  const { openCompose } = useCompose();

  const [searchQuery, setSearchQuery] = useState('');
  const [viewingEmail, setViewingEmail] = useState(null);
  const [copiedId, setCopiedId] = useState(null);

  const fetchEmails = async () => {
    try {
      const isFollowUpTab = activeTab === 'FollowUp';
      const params = {};
      if (activeTab !== 'All' && !isFollowUpTab) {
        params.status = activeTab;
      }
      const [emailRes, profRes] = await Promise.all([
        api.get('/emails', { params }),
        api.get('/professors')
      ]);
      let data = emailRes.data || [];
      if (isFollowUpTab) {
        data = data.filter(d => d.status === 'Sent' || d.status === 'Scheduled');
      }
      setEmails(data);
      setProfessors(profRes.data || []);
    } catch (err) {
      console.error(err);
      toast.error("Failed to load email drafts.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
  }, [activeTab]);

  const handleCopy = (draft) => {
    const text = `Subject: ${draft.subject}\n\n${draft.body}`;
    navigator.clipboard.writeText(text);
    setCopiedId(draft.id);
    toast.success("Email copied! Ready to paste into Gmail.", { icon: '📋' });
    setTimeout(() => setCopiedId(null), 3000);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this email draft?")) return;
    try {
      await api.delete(`/emails/${id}`);
      toast.success("Draft removed.");
      if (viewingEmail?.id === id) setViewingEmail(null);
      fetchEmails();
    } catch (err) {
      toast.error("Failed to delete draft.");
    }
  };

  const getProfessor = (profId) => {
    return professors.find(p => p.id === profId) || { name: 'Faculty Member', institution: 'University', email: '' };
  };

  const filteredEmails = emails.filter(d => {
    if (!searchQuery.trim()) return true;
    const prof = getProfessor(d.professor_id);
    const q = searchQuery.toLowerCase();
    return (
      d.subject.toLowerCase().includes(q) ||
      d.body.toLowerCase().includes(q) ||
      prof.name.toLowerCase().includes(q) ||
      prof.institution.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-slate-900">
            Outreach Email Center
          </h2>
          <p className="text-xs text-slate-500">
            Manage your initial inquiries, sent emails, and follow-up threads
          </p>
        </div>

        <button
          onClick={() => openCompose({ mode: 'new' })}
          className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-sm flex items-center gap-1.5 transition-all self-start sm:self-auto"
        >
          <Mail className="w-4 h-4" />
          <span>Compose Email</span>
        </button>
      </div>

      {/* Tabs and Search Filter Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        {/* Tabs */}
        <div className="flex items-center gap-1 p-1 rounded-xl bg-white border border-slate-200 w-fit text-xs font-semibold shadow-2xs">
          {['All', 'Draft', 'Sent', 'Scheduled', 'Replied'].map((tab) => (
            <button
              key={tab}
              onClick={() => setSearchParams({ tab })}
              className={`px-4 py-1.5 rounded-lg transition-all ${
                activeTab === tab
                  ? 'bg-blue-600 text-white shadow-2xs font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {tab === 'Sent' ? 'Sent Outreach' : tab}
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by faculty, university, subject..."
            className="w-full pl-9 pr-3 py-1.5 bg-white border border-slate-200 rounded-xl text-xs placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-500 shadow-2xs"
          />
        </div>
      </div>

      {/* Emails List */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center h-48">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : filteredEmails.length === 0 ? (
          <div className="text-center py-16 px-4">
            <Mail className="w-10 h-10 mx-auto text-slate-300 mb-2" />
            <h3 className="text-sm font-semibold text-slate-700">
              {searchQuery ? "No matching emails found" : activeTab === 'Sent' ? "No sent outreach emails yet" : "No emails found in this category"}
            </h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1 mb-4">
              {activeTab === 'Sent'
                ? "When you send an outreach via SMTP or click 'Open in Gmail (1-Click)' and mark as Sent, your dispatched emails will appear here."
                : "Click 'Compose Email' to draft personalized outreach or autofill from previous outreach."}
            </p>
            <button
              onClick={() => openCompose({ mode: 'new' })}
              className="px-4 py-2 rounded-xl bg-blue-600 text-white text-xs font-bold inline-flex items-center gap-1.5 shadow-sm hover:bg-blue-700"
            >
              <Mail className="w-4 h-4" />
              <span>Compose Email Now</span>
            </button>
          </div>
        ) : (
          <div className="divide-y divide-slate-100 text-xs">
            {filteredEmails.map((draft) => {
              const prof = getProfessor(draft.professor_id);
              return (
                <div
                  key={draft.id}
                  className="p-4 hover:bg-[#F2F6FC]/60 transition-colors flex flex-col lg:flex-row lg:items-center justify-between gap-4"
                >
                  <div className="flex items-start gap-3 flex-1 min-w-0">
                    <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                      {prof.name.charAt(0)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-bold text-slate-900 text-sm">
                          {prof.name}
                        </span>
                        <span className="text-[11px] text-blue-900 font-semibold flex items-center gap-1">
                          <Building className="w-3 h-3 text-slate-400" />
                          <span>{prof.institution}</span>
                        </span>
                        {prof.email && (
                          <span className="font-mono text-[10px] text-slate-400">
                            &lt;{prof.email}&gt;
                          </span>
                        )}
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                          draft.status === 'Sent' ? 'bg-emerald-50 text-emerald-800 border-emerald-300' :
                          draft.status === 'Replied' ? 'bg-teal-50 text-teal-800 border-teal-200' :
                          draft.status === 'Scheduled' ? 'bg-blue-50 text-blue-800 border-blue-200' :
                          'bg-slate-100 text-slate-700 border-slate-200'
                        }`}>
                          {draft.status === 'Sent' ? '✓ Sent Outreach' : draft.status}
                        </span>
                      </div>

                      <div className="font-semibold text-slate-800 mt-1 cursor-pointer hover:text-blue-600 transition-colors" onClick={() => setViewingEmail(draft)}>
                        {draft.subject}
                      </div>

                      <p className="text-slate-600 text-xs line-clamp-2 mt-0.5 leading-relaxed">
                        {draft.body}
                      </p>

                      <div className="text-[11px] text-slate-400 mt-1.5 flex items-center gap-4">
                        <span>Drafted: {new Date(draft.created_at).toLocaleDateString()}</span>
                        {draft.sent_at && (
                          <span className="text-emerald-700 font-medium flex items-center gap-1">
                            <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                            Dispatched: {new Date(draft.sent_at).toLocaleString()}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Quick Action Buttons */}
                  <div className="flex flex-wrap items-center gap-1.5 self-end lg:self-center shrink-0">
                    <button
                      onClick={() => setViewingEmail(draft)}
                      className="px-2.5 py-1.5 rounded-xl bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 font-semibold text-xs flex items-center gap-1 shadow-2xs transition-all"
                      title="Read full email content"
                    >
                      <Eye className="w-3.5 h-3.5 text-slate-500" />
                      <span>View Full</span>
                    </button>

                    <button
                      onClick={() => {
                        openCompose({
                          mode: 'new',
                          subject: draft.subject,
                          body: draft.body
                        });
                        toast.success("Loaded into compose email! Ready to customize.", { icon: '📝' });
                      }}
                      className="px-2.5 py-1.5 rounded-xl bg-blue-50 hover:bg-blue-100 border border-blue-200 text-blue-700 font-semibold text-xs flex items-center gap-1 shadow-2xs transition-all"
                      title="Autofill this email into a new outreach pitch"
                    >
                      <History className="w-3.5 h-3.5 text-blue-600" />
                      <span>Autofill New</span>
                    </button>

                    <button
                      onClick={() => handleCopy(draft)}
                      className={`px-2.5 py-1.5 rounded-xl border text-xs font-semibold flex items-center gap-1 transition-all ${
                        copiedId === draft.id
                          ? 'bg-emerald-50 border-emerald-300 text-emerald-700 font-bold'
                          : 'bg-white hover:bg-slate-100 border-slate-200 text-slate-700 shadow-2xs'
                      }`}
                      title="Copy to clipboard for Gmail"
                    >
                      {copiedId === draft.id ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-500" />}
                      <span>{copiedId === draft.id ? "Copied!" : "Copy"}</span>
                    </button>

                    <button
                      onClick={() => openCompose({
                        professorId: prof.id,
                        professorName: prof.name,
                        institution: prof.institution,
                        recipientEmail: prof.email,
                        previousSubject: draft.subject,
                        previousBody: draft.body,
                        mode: 'follow_up',
                        followUpStage: 1
                      })}
                      className="px-2.5 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100 border border-amber-200 text-amber-800 text-xs font-bold flex items-center gap-1 transition-all"
                      title="Generate AI Follow-Up"
                    >
                      <RotateCw className="w-3.5 h-3.5 text-amber-600" />
                      <span>Follow-Up</span>
                    </button>

                    <button
                      onClick={() => handleDelete(draft.id)}
                      className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                      title="Delete Entry"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Full Email View Modal */}
      {viewingEmail && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 rounded-3xl max-w-2xl w-full border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden flex flex-col max-h-[85vh] animate-in fade-in zoom-in-95 duration-150">
            {/* Header */}
            <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-800/50">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-2xl bg-blue-600 text-white flex items-center justify-center font-bold text-sm shadow-sm">
                  {getProfessor(viewingEmail.professor_id).name.charAt(0)}
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">
                    {getProfessor(viewingEmail.professor_id).name}
                  </h3>
                  <p className="text-xs text-slate-500 flex items-center gap-1.5">
                    <span>{getProfessor(viewingEmail.professor_id).institution}</span>
                    <span>•</span>
                    <span className="font-mono text-[11px] text-blue-600">{getProfessor(viewingEmail.professor_id).email}</span>
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                  viewingEmail.status === 'Sent' ? 'bg-emerald-50 text-emerald-800 border-emerald-300' :
                  'bg-slate-100 text-slate-700 border-slate-200'
                }`}>
                  {viewingEmail.status === 'Sent' ? '✓ Sent Outreach' : viewingEmail.status}
                </span>
                <button
                  onClick={() => setViewingEmail(null)}
                  className="p-1.5 rounded-xl hover:bg-slate-200/60 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-700 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Subject and Content */}
            <div className="p-6 overflow-y-auto space-y-4 text-xs">
              <div className="p-3.5 bg-slate-50 rounded-2xl border border-slate-100">
                <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block mb-1">Subject</span>
                <span className="text-sm font-bold text-slate-900">{viewingEmail.subject}</span>
              </div>

              {viewingEmail.sent_at && (
                <div className="text-[11px] text-emerald-700 font-medium flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Dispatched: <strong>{new Date(viewingEmail.sent_at).toLocaleString()}</strong></span>
                </div>
              )}

              <div>
                <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block mb-1.5">Message Content</span>
                <div className="p-4 bg-white rounded-2xl border border-slate-200 text-slate-800 whitespace-pre-wrap leading-relaxed font-sans text-xs max-h-[350px] overflow-y-auto shadow-2xs">
                  {viewingEmail.body}
                </div>
              </div>
            </div>

            {/* Modal Footer Actions */}
            <div className="p-4 bg-slate-50 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2">
              <button
                onClick={() => handleCopy(viewingEmail)}
                className="px-3 py-1.5 rounded-xl bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 font-semibold text-xs flex items-center gap-1.5 shadow-2xs"
              >
                <Copy className="w-3.5 h-3.5 text-slate-500" />
                <span>Copy Body</span>
              </button>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    openCompose({
                      mode: 'new',
                      subject: viewingEmail.subject,
                      body: viewingEmail.body
                    });
                    setViewingEmail(null);
                    toast.success("Loaded into compose email!", { icon: '📝' });
                  }}
                  className="px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm"
                >
                  <History className="w-3.5 h-3.5" />
                  <span>Autofill in Compose</span>
                </button>

                <button
                  onClick={() => {
                    const prof = getProfessor(viewingEmail.professor_id);
                    openCompose({
                      professorId: prof.id,
                      professorName: prof.name,
                      institution: prof.institution,
                      recipientEmail: prof.email,
                      previousSubject: viewingEmail.subject,
                      previousBody: viewingEmail.body,
                      mode: 'follow_up',
                      followUpStage: 1
                    });
                    setViewingEmail(null);
                  }}
                  className="px-3.5 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm"
                >
                  <RotateCw className="w-3.5 h-3.5" />
                  <span>Take Follow-Up</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmailCenterPage;

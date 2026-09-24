import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useCompose } from '../context/ComposeContext';
import { 
  Mail, 
  Send, 
  RotateCw, 
  CheckCircle, 
  Copy, 
  Trash2, 
  Clock, 
  Building,
  Check
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

  const [copiedId, setCopiedId] = useState(null);

  const fetchEmails = async () => {
    try {
      const [emailRes, profRes] = await Promise.all([
        api.get('/emails', {
          params: { status: activeTab !== 'All' ? activeTab : undefined }
        }),
        api.get('/professors')
      ]);
      setEmails(emailRes.data || []);
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
      fetchEmails();
    } catch (err) {
      toast.error("Failed to delete draft.");
    }
  };

  const getProfessor = (profId) => {
    return professors.find(p => p.id === profId) || { name: 'Faculty Member', institution: 'University' };
  };

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

      {/* Tabs */}
      <div className="flex items-center gap-1 p-1 rounded-xl bg-white border border-slate-200 w-fit text-xs font-semibold shadow-2xs">
        {['All', 'Draft', 'Scheduled', 'Sent', 'Replied'].map((tab) => (
          <button
            key={tab}
            onClick={() => setSearchParams({ tab })}
            className={`px-4 py-1.5 rounded-lg transition-all ${
              activeTab === tab
                ? 'bg-blue-600 text-white shadow-2xs font-bold'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Emails List */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center h-48">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : emails.length === 0 ? (
          <div className="text-center py-16 px-4">
            <Mail className="w-10 h-10 mx-auto text-slate-300 mb-2" />
            <h3 className="text-sm font-semibold text-slate-700">No emails found in this category</h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1 mb-4">
              Click "Compose Email" to craft a cold outreach email or take a follow-up.
            </p>
            <button
              onClick={() => openCompose({ mode: 'new' })}
              className="px-4 py-2 rounded-xl bg-blue-600 text-white text-xs font-bold inline-flex items-center gap-1.5"
            >
              <Mail className="w-4 h-4" />
              <span>Compose Email Now</span>
            </button>
          </div>
        ) : (
          <div className="divide-y divide-slate-100 text-xs">
            {emails.map((draft) => {
              const prof = getProfessor(draft.professor_id);
              return (
                <div
                  key={draft.id}
                  className="p-4 hover:bg-[#F2F6FC]/60 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                >
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                      {prof.name.charAt(0)}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-900 text-sm">
                          {prof.name}
                        </span>
                        <span className="text-[11px] text-blue-900 font-semibold flex items-center gap-1">
                          <Building className="w-3 h-3 text-slate-400" />
                          <span>{prof.institution}</span>
                        </span>
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                          draft.status === 'Sent' ? 'bg-emerald-50 text-emerald-800 border-emerald-200' :
                          draft.status === 'Replied' ? 'bg-teal-50 text-teal-800 border-teal-200' :
                          'bg-slate-100 text-slate-700 border-slate-200'
                        }`}>
                          {draft.status}
                        </span>
                      </div>

                      <div className="font-semibold text-slate-800 mt-1">
                        {draft.subject}
                      </div>

                      <p className="text-slate-600 text-xs line-clamp-2 mt-0.5 max-w-3xl leading-relaxed">
                        {draft.body}
                      </p>

                      <div className="text-[11px] text-slate-400 mt-1.5 flex items-center gap-3">
                        <span>Created: {new Date(draft.created_at).toLocaleDateString()}</span>
                        {draft.sent_at && <span>Sent: {new Date(draft.sent_at).toLocaleString()}</span>}
                      </div>
                    </div>
                  </div>

                  {/* Quick Action Buttons */}
                  <div className="flex items-center gap-2 self-end sm:self-center shrink-0">
                    <button
                      onClick={() => handleCopy(draft)}
                      className={`px-3 py-1.5 rounded-xl border text-xs font-semibold flex items-center gap-1 transition-all ${
                        copiedId === draft.id
                          ? 'bg-emerald-50 border-emerald-300 text-emerald-700 font-bold'
                          : 'bg-white hover:bg-slate-100 border-slate-200 text-slate-700 shadow-2xs'
                      }`}
                      title="Copy to clipboard for Gmail"
                    >
                      {copiedId === draft.id ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-500" />}
                      <span>{copiedId === draft.id ? "Copied!" : "Copy for Gmail"}</span>
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
                      className="px-3 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100 border border-amber-200 text-amber-800 text-xs font-bold flex items-center gap-1 transition-all"
                      title="Generate AI Follow-Up"
                    >
                      <RotateCw className="w-3.5 h-3.5 text-amber-600" />
                      <span>Take Follow-Up</span>
                    </button>

                    <button
                      onClick={() => handleDelete(draft.id)}
                      className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                      title="Delete Draft"
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
    </div>
  );
};

export default EmailCenterPage;

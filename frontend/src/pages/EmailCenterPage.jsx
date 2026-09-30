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
  ExternalLink,
  Zap,
  CheckSquare
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

  // Multi-select & Batch Actions State
  const [selectedIds, setSelectedIds] = useState([]);
  const [isBatchSending, setIsBatchSending] = useState(false);
  const [isBatchDeleting, setIsBatchDeleting] = useState(false);
  const [isBatchGenerating, setIsBatchGenerating] = useState(false);
  const [batchFollowUpStage, setBatchFollowUpStage] = useState(1);

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
      let data = Array.isArray(emailRes.data) ? emailRes.data : [];
      
      // Server data is authoritative
      const localDrafts = JSON.parse(localStorage.getItem('local_email_drafts') || '[]');
      const localSent = JSON.parse(localStorage.getItem('local_sent_emails') || '[]');
      const allLocal = [...localDrafts, ...localSent];
      
      const serverIds = new Set(data.map(d => String(d.id)));
      const offlineOnly = allLocal.filter(d => d.id && !serverIds.has(String(d.id)));
      if (offlineOnly.length > 0) {
        data = [...offlineOnly, ...data];
      }

      if (isFollowUpTab) {
        data = data.filter(d => d.status === 'Sent');
      } else if (activeTab !== 'All') {
        data = data.filter(d => d.status?.toLowerCase() === activeTab.toLowerCase());
      }
      setEmails(data);
      setProfessors(Array.isArray(profRes.data) ? profRes.data : []);
    } catch (err) {
      console.error(err);
      // Fallback to local storage on error
      const localDrafts = JSON.parse(localStorage.getItem('local_email_drafts') || '[]');
      const localSent = JSON.parse(localStorage.getItem('local_sent_emails') || '[]');
      let localData = [...localDrafts, ...localSent];
      if (activeTab !== 'All') {
        localData = localData.filter(d => d.status?.toLowerCase() === activeTab.toLowerCase());
      }
      setEmails(localData);
      if (localData.length === 0) {
        toast.error("Backend offline. Using local CRM storage.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
    setSelectedIds([]);
  }, [activeTab]);

  const handleCopy = (draft) => {
    const text = `Subject: ${draft.subject}\n\n${draft.body}`;
    navigator.clipboard.writeText(text);
    setCopiedId(draft.id);
    toast.success("Email copied to clipboard!", { icon: '📋' });
    setTimeout(() => setCopiedId(null), 3000);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this email draft?")) return;
    try {
      try {
        await api.delete(`/emails/${id}`);
      } catch (apiErr) {
        console.warn("API delete draft warning:", apiErr);
      }
      toast.success("Draft removed.", { icon: '🗑️' });
      if (viewingEmail?.id === id) setViewingEmail(null);
      // Remove from local storage as well
      const localDrafts = JSON.parse(localStorage.getItem('local_email_drafts') || '[]');
      localStorage.setItem('local_email_drafts', JSON.stringify(localDrafts.filter(d => String(d.id) !== String(id))));
      const localSent = JSON.parse(localStorage.getItem('local_sent_emails') || '[]');
      localStorage.setItem('local_sent_emails', JSON.stringify(localSent.filter(d => String(d.id) !== String(id))));
      // Immediately filter from state
      setEmails(prev => prev.filter(e => String(e.id) !== String(id)));
      setSelectedIds(prev => prev.filter(x => String(x) !== String(id)));
      window.dispatchEvent(new Event('crm-data-updated'));
      fetchEmails();
    } catch (err) {
      toast.error("Failed to delete draft.");
    }
  };

  // Bulk Delete Selected Drafts
  const handleDeleteSelected = async () => {
    if (selectedIds.length === 0) {
      toast.error("No drafts selected to delete.");
      return;
    }

    if (!window.confirm(`Permanently delete all ${selectedIds.length} selected email draft(s)?`)) {
      return;
    }

    setIsBatchDeleting(true);
    const toDeleteIds = [...selectedIds];

    try {
      try {
        await api.post('/emails/batch-delete', {
          draft_ids: toDeleteIds.map(Number)
        });
      } catch (apiErr) {
        console.warn("Backend batch delete fallback:", apiErr);
        for (const id of toDeleteIds) {
          try { await api.delete(`/emails/${id}`); } catch (_) {}
        }
      }

      // Purge from localStorage
      const localDrafts = JSON.parse(localStorage.getItem('local_email_drafts') || '[]');
      localStorage.setItem('local_email_drafts', JSON.stringify(localDrafts.filter(d => !toDeleteIds.some(delId => String(delId) === String(d.id)))));
      const localSent = JSON.parse(localStorage.getItem('local_sent_emails') || '[]');
      localStorage.setItem('local_sent_emails', JSON.stringify(localSent.filter(d => !toDeleteIds.some(delId => String(delId) === String(d.id)))));

      // Optimistically update in-memory state
      setEmails(prev => prev.filter(e => !toDeleteIds.some(delId => String(delId) === String(e.id))));
      setSelectedIds([]);
      toast.success(`Deleted ${toDeleteIds.length} email draft(s).`, { icon: '🗑️' });
      window.dispatchEvent(new Event('crm-data-updated'));
      fetchEmails();
    } catch (err) {
      console.error("Batch delete error:", err);
      toast.error("Failed to delete selected drafts.");
    } finally {
      setIsBatchDeleting(false);
    }
  };

  const getProfessor = (profId) => {
    return (Array.isArray(professors) ? professors : []).find(p => p.id === profId) || { name: 'Faculty Member', institution: 'University', email: '' };
  };

  const filteredEmails = (Array.isArray(emails) ? emails : []).filter(d => {
    if (!searchQuery.trim()) return true;
    const prof = getProfessor(d.professor_id);
    const q = searchQuery.toLowerCase();
    return (
      d.subject?.toLowerCase().includes(q) ||
      d.body?.toLowerCase().includes(q) ||
      prof.name?.toLowerCase().includes(q) ||
      prof.institution?.toLowerCase().includes(q)
    );
  });

  // Toggle selection for an individual email (robust string matching)
  const handleToggleSelect = (id) => {
    const idStr = String(id);
    setSelectedIds(prev => 
      prev.some(x => String(x) === idStr)
        ? prev.filter(x => String(x) !== idStr)
        : [...prev, id]
    );
  };

  const isAllSelected = filteredEmails.length > 0 && filteredEmails.every(e => selectedIds.some(s => String(s) === String(e.id)));

  // Toggle select all in current view
  const handleSelectAll = () => {
    if (isAllSelected) {
      setSelectedIds([]);
    } else {
      setSelectedIds(filteredEmails.map(e => e.id));
    }
  };

  // Select all drafts in current view
  const handleSelectAllDrafts = () => {
    const draftIds = filteredEmails.filter(e => e.status !== 'Sent').map(e => e.id);
    setSelectedIds(draftIds);
    if (draftIds.length > 0) {
      toast.success(`Selected ${draftIds.length} drafts!`, { icon: '☑️' });
    } else {
      toast('No drafts found in current view.', { icon: 'ℹ️' });
    }
  };

  // Delete all drafts currently in view
  const handleDeleteAllDrafts = async () => {
    const toDelete = filteredEmails.filter(e => e.status !== 'Sent');
    const toDeleteIds = toDelete.map(e => e.id);
    if (toDeleteIds.length === 0) {
      toast('No drafts found in this view to delete.', { icon: 'ℹ️' });
      return;
    }
    if (!window.confirm(`Permanently delete ALL ${toDeleteIds.length} draft(s) currently shown? This cannot be undone.`)) {
      return;
    }
    setIsBatchDeleting(true);
    try {
      try {
        await api.post('/emails/batch-delete', {
          draft_ids: toDeleteIds.map(Number)
        });
      } catch (apiErr) {
        console.warn("Backend batch delete fallback:", apiErr);
        for (const id of toDeleteIds) {
          try { await api.delete(`/emails/${id}`); } catch (_) {}
        }
      }

      // Purge from localStorage
      const localDrafts = JSON.parse(localStorage.getItem('local_email_drafts') || '[]');
      localStorage.setItem('local_email_drafts', JSON.stringify(localDrafts.filter(d => !toDeleteIds.some(delId => String(delId) === String(d.id)))));

      // Optimistically update in-memory state
      setEmails(prev => prev.filter(e => !toDeleteIds.some(delId => String(delId) === String(e.id))));
      setSelectedIds([]);
      toast.success(`Deleted all ${toDeleteIds.length} draft(s).`, { icon: '🗑️' });
      window.dispatchEvent(new Event('crm-data-updated'));
      fetchEmails();
    } catch (err) {
      console.error("Delete all drafts error:", err);
      toast.error("Failed to delete all drafts.");
    } finally {
      setIsBatchDeleting(false);
    }
  };

  // Send all selected drafts in one go
  const handleSendSelectedInOneGo = async () => {
    const toSend = filteredEmails.filter(e => selectedIds.some(s => String(s) === String(e.id)) && e.status !== 'Sent');
    if (toSend.length === 0) {
      toast.error("No drafts selected to send.");
      return;
    }

    if (!window.confirm(`Send all ${toSend.length} selected email drafts in one go?`)) {
      return;
    }

    setIsBatchSending(true);
    try {
      const draftIds = toSend.map(e => e.id);
      try {
        await api.post('/emails/batch-send', {
          draft_ids: draftIds,
          send_now: true
        });
      } catch (apiErr) {
        console.warn("Backend batch-send failed, using fallback:", apiErr);
      }

      // Update local storage
      const localDrafts = JSON.parse(localStorage.getItem('local_email_drafts') || '[]');
      const localSent = JSON.parse(localStorage.getItem('local_sent_emails') || '[]');
      const nowIso = new Date().toISOString();

      const remainingDrafts = localDrafts.filter(d => !draftIds.some(delId => String(delId) === String(d.id)));
      const sentDrafts = localDrafts
        .filter(d => draftIds.some(delId => String(delId) === String(d.id)))
        .map(d => ({ ...d, status: 'Sent', sent_at: nowIso }));

      localStorage.setItem('local_email_drafts', JSON.stringify(remainingDrafts));
      localStorage.setItem('local_sent_emails', JSON.stringify([...sentDrafts, ...localSent]));

      // Optimistically update in-memory state
      setEmails(prev => prev.map(e => draftIds.some(delId => String(delId) === String(e.id)) ? { ...e, status: 'Sent', sent_at: nowIso } : e));
      setSelectedIds([]);
      toast.success(`🚀 Successfully dispatched ${toSend.length} emails in one go!`, { icon: '⚡', duration: 5000 });
      window.dispatchEvent(new Event('crm-data-updated'));
      fetchEmails();
    } catch (err) {
      console.error("Batch send error:", err);
      toast.error("Failed to send selected emails.");
    } finally {
      setIsBatchSending(false);
    }
  };

  // Send single draft immediately in one click
  const handleSendSingleDraft = async (draft) => {
    try {
      try {
        await api.post('/emails/send', {
          draft_id: draft.id,
          send_now: true
        });
      } catch (apiErr) {
        console.warn("API send failed, falling back to local CRM dispatch:", apiErr);
      }

      const nowIso = new Date().toISOString();
      const localDrafts = JSON.parse(localStorage.getItem('local_email_drafts') || '[]');
      const localSent = JSON.parse(localStorage.getItem('local_sent_emails') || '[]');
      const remainingDrafts = localDrafts.filter(d => d.id !== draft.id);
      const sentItem = { ...draft, status: 'Sent', sent_at: nowIso };
      localStorage.setItem('local_email_drafts', JSON.stringify(remainingDrafts));
      localStorage.setItem('local_sent_emails', JSON.stringify([sentItem, ...localSent]));

      setEmails(prev => prev.map(e => e.id === draft.id ? { ...e, status: 'Sent', sent_at: nowIso } : e));
      toast.success(`⚡ Email sent to ${getProfessor(draft.professor_id)?.name || draft.recipient_email}!`, { icon: '⚡' });
      window.dispatchEvent(new Event('crm-data-updated'));
      fetchEmails();
    } catch (err) {
      toast.error("Failed to send draft.");
    }
  };

  // Select and generate follow up email to all selected
  const handleBatchGenerateFollowUp = async () => {
    const selectedEmails = filteredEmails.filter(e => selectedIds.includes(e.id));
    if (selectedEmails.length === 0) {
      toast.error("Please select at least one email to generate follow-up.");
      return;
    }

    setIsBatchGenerating(true);
    let successCount = 0;

    for (const item of selectedEmails) {
      const prof = getProfessor(item.professor_id);
      let fuSubject = `Re: ${item.subject || 'PhD Inquiries'}`;
      let fuBody = `Dear Professor ${prof?.name?.replace(/^Prof\.?\s+/i, '') || 'Faculty Member'},\n\nI hope you are having a productive week. I am following up on my previous note regarding prospective PhD research opportunities in your laboratory.\n\nI remain very enthusiastic about your group's publications and research directions. Given your busy schedule, I would welcome a brief 10-15 minute introductory video call at your convenience, or I can provide any additional materials regarding my research background.\n\nThank you for your time and guidance.\n\nSincerely,\nSumit Raj`;

      try {
        const res = await api.post('/ai/follow-up', {
          professor_id: prof?.id,
          previous_subject: item.subject,
          previous_body: item.body,
          follow_up_stage: batchFollowUpStage
        });
        if (res.data?.subject) fuSubject = res.data.subject;
        if (res.data?.body) fuBody = res.data.body;
      } catch (aiErr) {
        console.warn("AI follow-up endpoint failed, using grounded template:", aiErr);
      }

      const newDraftPayload = {
        professor_id: prof?.id,
        recipient_email: prof?.email || item.recipient_email,
        recipient_name: prof?.name,
        institution: prof?.institution,
        subject: fuSubject,
        body: fuBody,
        status: 'Draft'
      };

      try {
        await api.post('/emails', newDraftPayload);
      } catch (saveErr) {
        // Local offline fallback
        const fallbackDraft = {
          id: Date.now() + Math.floor(Math.random() * 1000),
          ...newDraftPayload,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        const localDrafts = JSON.parse(localStorage.getItem('local_email_drafts') || '[]');
        localDrafts.unshift(fallbackDraft);
        localStorage.setItem('local_email_drafts', JSON.stringify(localDrafts));
      }
      successCount++;
    }

    setIsBatchGenerating(false);
    setSelectedIds([]);
    window.dispatchEvent(new Event('crm-data-updated'));
    setSearchParams({ tab: 'Draft' });
    toast.success(`🔁 Generated ${successCount} follow-up drafts! Switched to Drafts tab.`, { icon: '✨', duration: 6000 });
    fetchEmails();
  };

  return (
    <div className="space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-slate-900">
            Outreach Email Center
          </h2>
          <p className="text-xs text-slate-500">
            Manage your initial inquiries, save drafts, bulk send outreach, and generate follow-ups
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
          {['All', 'Draft', 'Sent', 'Replied'].map((tab) => (
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

      {/* Multi-Select & Bulk Actions Bar */}
      <div className="bg-white border border-slate-200 rounded-2xl p-3 flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-2xs">
        <div className="flex flex-wrap items-center gap-2.5">
          <label className="flex items-center gap-2 cursor-pointer font-bold text-slate-800 select-none text-xs bg-slate-50 px-2.5 py-1.5 rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">
            <input
              type="checkbox"
              checked={isAllSelected}
              onChange={handleSelectAll}
              className="w-4 h-4 rounded text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer"
            />
            <span>Select All ({selectedIds.length}/{filteredEmails.length})</span>
          </label>

          <button
            onClick={handleSelectAllDrafts}
            className="px-2.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition-colors"
            title="Select all unsent drafts only"
          >
            Select All Drafts ({filteredEmails.filter(e => e.status !== 'Sent').length})
          </button>

          {selectedIds.length > 0 && (
            <button
              onClick={() => setSelectedIds([])}
              className="text-xs text-slate-500 hover:text-slate-700 underline font-medium px-1"
            >
              Clear Selection
            </button>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Bulk Send Selected in One Go */}
          <button
            onClick={handleSendSelectedInOneGo}
            disabled={selectedIds.length === 0 || isBatchSending}
            className="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
            title="Send all selected drafts immediately in one go"
          >
            <Zap className="w-3.5 h-3.5" />
            <span>{isBatchSending ? "Sending..." : `🚀 Send Selected (${selectedIds.length})`}</span>
          </button>

          {/* Bulk Delete Selected */}
          <button
            onClick={handleDeleteSelected}
            disabled={selectedIds.length === 0 || isBatchDeleting}
            className="px-3.5 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
            title="Delete all selected email drafts"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>{isBatchDeleting ? "Deleting..." : `🗑️ Delete Selected (${selectedIds.length})`}</span>
          </button>

          {/* Delete All Drafts Button */}
          {filteredEmails.some(e => e.status !== 'Sent') && (
            <button
              onClick={handleDeleteAllDrafts}
              disabled={isBatchDeleting}
              className="px-3 py-2 rounded-xl bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-700 font-bold text-xs flex items-center gap-1.5 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
              title="Delete all drafts in this view at once"
            >
              <Trash2 className="w-3.5 h-3.5 text-rose-500" />
              <span>Delete All Drafts</span>
            </button>
          )}

          {/* Batch Follow-Up Generator */}
          <div className="flex items-center gap-1.5 bg-slate-50 border border-slate-200 rounded-xl p-1 shadow-2xs">
            <select
              value={batchFollowUpStage}
              onChange={(e) => setBatchFollowUpStage(Number(e.target.value))}
              className="text-[11px] font-semibold text-slate-700 bg-transparent border-0 focus:outline-none px-2 cursor-pointer"
              title="Follow-Up Stage"
            >
              <option value={1}>Stage 1 Follow-Up</option>
              <option value={2}>Stage 2 Nudge</option>
              <option value={3}>Stage 3 Final Check</option>
            </select>
            <button
              onClick={handleBatchGenerateFollowUp}
              disabled={selectedIds.length === 0 || isBatchGenerating}
              className="px-3.5 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs flex items-center gap-1.5 transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-2xs"
              title="Generate AI follow-up drafts for all selected emails"
            >
              <RotateCw className={`w-3.5 h-3.5 ${isBatchGenerating ? 'animate-spin' : ''}`} />
              <span>{isBatchGenerating ? "Generating..." : `🔁 Follow-Up (${selectedIds.length})`}</span>
            </button>
          </div>
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
                ? "When you send outreach via 'Send Now' or 'Send in One Go', your dispatched emails will appear here."
                : "Save emails as draft in Compose, then select all drafts to send them in one go!"}
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
              const isSelected = selectedIds.some(x => String(x) === String(draft.id));
              return (
                <div
                  key={draft.id}
                  className={`p-4 transition-colors flex flex-col lg:flex-row lg:items-center justify-between gap-4 ${
                    isSelected ? 'bg-blue-50/70 border-l-4 border-l-blue-600' : 'hover:bg-[#F2F6FC]/60'
                  }`}
                >
                  <div className="flex items-start gap-3 flex-1 min-w-0">
                    {/* Row Select Checkbox & Avatar click to select */}
                    <div className="flex items-center gap-2.5 select-none shrink-0 mt-0.5">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => handleToggleSelect(draft.id)}
                        className="w-4 h-4 rounded text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer shrink-0"
                      />

                      <div
                        onClick={() => handleToggleSelect(draft.id)}
                        className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shrink-0 cursor-pointer transition-all ${
                          isSelected ? 'bg-blue-600 text-white shadow-sm' : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                        }`}
                        title="Click to toggle selection"
                      >
                        {isSelected ? '✓' : ((prof?.name || draft.recipient_email || 'P').charAt(0)).toUpperCase()}
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-bold text-slate-900 text-sm">
                          {prof?.name || draft.recipient_email || 'Faculty Member'}
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
                          'bg-slate-100 text-slate-700 border-slate-200'
                        }`}>
                          {draft.status === 'Sent' ? '✓ Sent Outreach' : draft.status || 'Draft'}
                        </span>
                      </div>

                      <div className="font-semibold text-slate-800 mt-1 cursor-pointer hover:text-blue-600 transition-colors" onClick={() => setViewingEmail(draft)}>
                        {draft.subject}
                      </div>

                      <p className="text-slate-600 text-xs line-clamp-2 mt-0.5 leading-relaxed">
                        {draft.body}
                      </p>

                      <div className="text-[11px] text-slate-400 mt-1.5 flex items-center gap-4">
                        <span>Drafted: {new Date(draft.created_at || Date.now()).toLocaleDateString()}</span>
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
                    {/* 1-Click Send Now for any unsent draft */}
                    {draft.status !== 'Sent' && (
                      <button
                        onClick={() => handleSendSingleDraft(draft)}
                        className="px-2.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-1 shadow-sm transition-all"
                        title="Send this email right now"
                      >
                        <Zap className="w-3.5 h-3.5" />
                        <span>Send Now</span>
                      </button>
                    )}

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
                      <span>Autofill</span>
                    </button>

                    <button
                      onClick={() => handleCopy(draft)}
                      className={`px-2.5 py-1.5 rounded-xl border text-xs font-semibold flex items-center gap-1 transition-all ${
                        copiedId === draft.id
                          ? 'bg-emerald-50 border-emerald-300 text-emerald-700 font-bold'
                          : 'bg-white hover:bg-slate-100 border-slate-200 text-slate-700 shadow-2xs'
                      }`}
                      title="Copy email to clipboard"
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
                  {((getProfessor(viewingEmail.professor_id)?.name || viewingEmail.recipient_email || 'P').charAt(0)).toUpperCase()}
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">
                    {getProfessor(viewingEmail.professor_id)?.name || viewingEmail.recipient_email || 'Faculty Member'}
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
                  {viewingEmail.status === 'Sent' ? '✓ Sent Outreach' : viewingEmail.status || 'Draft'}
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
                {viewingEmail.status !== 'Sent' && (
                  <button
                    onClick={() => {
                      handleSendSingleDraft(viewingEmail);
                      setViewingEmail(null);
                    }}
                    className="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm"
                  >
                    <Zap className="w-3.5 h-3.5" />
                    <span>Send Now</span>
                  </button>
                )}

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

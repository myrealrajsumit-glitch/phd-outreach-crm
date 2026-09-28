import React, { useState, useEffect, useRef } from 'react';
import { useCompose } from '../../context/ComposeContext';
import { 
  X, 
  Minus, 
  Maximize2, 
  Minimize2, 
  Send, 
  Sparkles, 
  Copy, 
  Save, 
  Trash2, 
  RotateCw, 
  FileText,
  Check,
  ChevronDown,
  Clock,
  Globe,
  ShieldCheck,
  AlertTriangle,
  Zap,
  Calendar,
  CheckCircle2,
  Info
} from 'lucide-react';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { formatErrorMessage } from '../../utils/errorUtils';

const GmailCompose = () => {
  const { 
    isOpen, 
    isMinimized, 
    isMaximized, 
    composeData, 
    closeCompose, 
    toggleMinimize, 
    toggleMaximize,
    setComposeData
  } = useCompose();

  const [to, setTo] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [professors, setProfessors] = useState([]);
  const [selectedProfId, setSelectedProfId] = useState(null);
  const [tone, setTone] = useState('Formal Academic');
  const [wordCount, setWordCount] = useState(250);
  const [followUpStage, setFollowUpStage] = useState(1);
  const [customHook, setCustomHook] = useState('');
  const [templates, setTemplates] = useState([]);
  const [sentEmails, setSentEmails] = useState([]);
  
  // Smart Scheduler & Anti-Spam state
  const [scheduleData, setScheduleData] = useState(null);
  const [isAnalyzingSchedule, setIsAnalyzingSchedule] = useState(false);
  const [spamData, setSpamData] = useState(null);
  const [isCheckingSpam, setIsCheckingSpam] = useState(false);
  const [showSpamDetails, setShowSpamDetails] = useState(false);

  const [isAiGenerating, setIsAiGenerating] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [isScheduling, setIsScheduling] = useState(false);
  const [copied, setCopied] = useState(false);

  // Load professors, templates, and sent outreach
  useEffect(() => {
    const loadMetadata = async () => {
      try {
        const [profRes, tplRes, sentRes] = await Promise.all([
          api.get('/professors'),
          api.get('/emails/templates'),
          api.get('/emails', { params: { status: 'Sent' } })
        ]);
        setProfessors(Array.isArray(profRes.data) ? profRes.data : []);
        setTemplates(Array.isArray(tplRes.data) ? tplRes.data : []);
        setSentEmails(Array.isArray(sentRes.data) ? sentRes.data : []);
      } catch (err) {
        console.error("Error loading compose metadata:", err);
      }
    };
    if (isOpen) {
      loadMetadata();
    }
  }, [isOpen]);

  // Sync state when composeData changes
  useEffect(() => {
    if (isOpen) {
      setTo(composeData.recipientEmail || '');
      setSubject(composeData.subject || '');
      setBody(composeData.body || '');
      setSelectedProfId(composeData.professorId || null);
      setFollowUpStage(composeData.followUpStage || 1);
      setCopied(false);
    }
  }, [isOpen, composeData]);

  // Matched professor derived from current email or selected ID
  const matchedProf = Array.isArray(professors)
    ? professors.find(p => 
        (to && p.email?.toLowerCase() === to.trim().toLowerCase()) ||
        (selectedProfId && p.id === parseInt(selectedProfId))
      )
    : null;

  // Debounced Timezone & Country Intelligence analysis when `to` changes
  useEffect(() => {
    if (!isOpen || !to || !to.includes('@')) {
      setScheduleData(null);
      return;
    }

    const timer = setTimeout(async () => {
      setIsAnalyzingSchedule(true);
      try {
        const targetProf = Array.isArray(professors) 
          ? professors.find(p => p.email?.toLowerCase() === to.trim().toLowerCase()) 
          : null;
        const res = await api.post('/emails/analyze-schedule', {
          email: to.trim(),
          institution: targetProf?.institution || null
        });
        setScheduleData(res.data);
      } catch (err) {
        console.error("Timezone analysis error:", err);
      } finally {
        setIsAnalyzingSchedule(false);
      }
    }, 350);

    return () => clearTimeout(timer);
  }, [to, isOpen, professors]);

  // Debounced Anti-Spam analysis when `subject` or `body` changes
  useEffect(() => {
    if (!isOpen || (!subject && !body)) {
      setSpamData(null);
      return;
    }

    const timer = setTimeout(async () => {
      setIsCheckingSpam(true);
      try {
        const targetProf = Array.isArray(professors) 
          ? professors.find(p => p.email?.toLowerCase() === to.trim().toLowerCase()) 
          : null;
        const res = await api.post('/emails/check-spam', {
          subject: subject,
          body: body,
          recipient_name: targetProf?.name || null,
          recipient_email: to || null
        });
        setSpamData(res.data);
      } catch (err) {
        console.error("Spam check error:", err);
      } finally {
        setIsCheckingSpam(false);
      }
    }, 450);

    return () => clearTimeout(timer);
  }, [subject, body, to, isOpen, professors]);

  if (!isOpen) return null;

  const handleGenerateInitialDraft = async () => {
    if (!to || !to.includes('@')) {
      toast.error("Please enter a valid recipient email address.");
      return;
    }
    setIsAiGenerating(true);
    try {
      let prof = matchedProf;
      if (!prof && to) {
        prof = {
          name: to.split('@')[0].replace('.', ' ').replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
          email: to.trim(),
          institution: to.split('@')[1] || "Academic Institution",
          research_topics: "Computer Science, AI, Systems"
        };
      }

      const res = await api.post('/ai/draft-email', {
        professor_id: prof?.id || undefined,
        professor_name: prof?.name,
        institution: prof?.institution,
        research_topic: prof?.research_topics,
        tone: tone,
        word_count: wordCount,
        custom_hook: customHook || undefined
      });

      if (res.data?.subject) setSubject(res.data.subject);
      if (res.data?.body) setBody(res.data.body);
      toast.success("Academic inquiry generated!", { icon: '✨' });
    } catch (err) {
      console.error("AI Generation failed:", err);
      toast.error(formatErrorMessage(err, "Failed to generate AI email draft."));
    } finally {
      setIsAiGenerating(false);
    }
  };

  const handleGenerateFollowUp = async () => {
    if (!to || !to.includes('@')) {
      toast.error("Please enter a recipient email address.");
      return;
    }
    setIsAiGenerating(true);
    try {
      const prof = matchedProf || {
        name: to.split('@')[0].replace('.', ' ').replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
        email: to.trim()
      };

      const res = await api.post('/ai/follow-up-email', {
        professor_id: prof?.id || undefined,
        professor_name: prof?.name,
        original_subject: subject || "PhD Inquiry",
        follow_up_stage: followUpStage,
        tone: tone
      });

      if (res.data?.subject) setSubject(res.data.subject);
      if (res.data?.body) setBody(res.data.body);
      toast.success(`Follow-up Stage ${followUpStage} generated!`, { icon: '🔁' });
    } catch (err) {
      console.error("AI Follow-up failed:", err);
      toast.error(formatErrorMessage(err, "Failed to generate follow-up draft."));
    } finally {
      setIsAiGenerating(false);
    }
  };

  const handleSaveDraft = async ({ silent = false } = {}) => {
    let targetProf = matchedProf;

    const payload = {
      subject: subject || 'PhD Outreach Email',
      body: body || '',
      status: 'Draft'
    };

    if (targetProf?.id) {
      payload.professor_id = targetProf.id;
    } else if (to && to.trim()) {
      payload.recipient_email = to.trim();
    } else if (professors[0]?.id) {
      payload.professor_id = professors[0].id;
    } else {
      if (!silent) toast.error("Please specify a recipient professor or email address.");
      return null;
    }

    try {
      const res = await api.post('/emails', payload);
      if (!silent) toast.success("Draft saved to CRM outbox!", { icon: '💾' });
      return res.data;
    } catch (err) {
      console.error("Save draft error:", err);
      if (!silent) toast.error(formatErrorMessage(err, "Failed to save draft."));
      return null;
    }
  };

  const handleCopyToClipboard = () => {
    const fullText = `Subject: ${subject}\n\n${body}`;
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    toast.success("Email copied to clipboard!", { icon: '📋' });
    setTimeout(() => setCopied(false), 2500);
  };

  const handleMarkAsSent = async () => {
    let targetProf = matchedProf;

    const payload = {
      subject: subject || 'PhD Outreach Email',
      body: body || '',
      status: 'Sent'
    };

    if (targetProf?.id) {
      payload.professor_id = targetProf.id;
    } else if (to && to.trim()) {
      payload.recipient_email = to.trim();
    } else {
      toast.error("Please specify a recipient email.");
      return;
    }

    try {
      await api.post('/emails', payload);
      toast.success("Outreach marked as Sent in CRM!", { icon: '✅' });
      const sentRes = await api.get('/emails', { params: { status: 'Sent' } });
      setSentEmails(sentRes.data || []);
      closeCompose();
    } catch (err) {
      console.error("Mark as sent error:", err);
      toast.error(formatErrorMessage(err, "Failed to record sent outreach."));
    }
  };

  // Option 1: Send Instant Email (Dispatches immediately via SMTP)
  const handleSendInstantEmail = async () => {
    if (!to || !to.includes('@') || !body) {
      toast.error("Please specify recipient and message body.");
      return;
    }

    if (spamData && !spamData.is_safe_to_send) {
      const proceed = window.confirm(
        `⚠️ High Spam Risk Detected (Score: ${spamData.deliverability_score}%).\n\nIssues:\n• ${spamData.flags.join('\n• ')}\n\nAre you sure you want to dispatch without fixing these?`
      );
      if (!proceed) return;
    }

    setIsSending(true);
    try {
      const draft = await handleSaveDraft({ silent: true });
      if (!draft?.id) {
        throw new Error("Could not initialize email draft in CRM.");
      }

      const sendRes = await api.post('/emails/send', {
        draft_id: draft.id,
        send_now: true
      });
      toast.success(sendRes.data.message || `Instant email dispatched to ${to}!`, { icon: '⚡', duration: 5000 });
      closeCompose();
    } catch (err) {
      console.error("Instant send error:", err);
      const errMsg = formatErrorMessage(err, "SMTP instant dispatch failed.");
      toast.error(errMsg, { duration: 6000 });
    } finally {
      setIsSending(false);
    }
  };

  // Option 2: Smart Schedule Email (Schedules at optimal academic local time, strictly avoiding Friday)
  const handleSmartScheduleEmail = async () => {
    if (!to || !to.includes('@') || !body) {
      toast.error("Please specify recipient and message body.");
      return;
    }

    setIsScheduling(true);
    try {
      // 1. Ensure schedule analysis is loaded
      let sched = scheduleData;
      if (!sched) {
        const targetProf = matchedProf;
        const res = await api.post('/emails/analyze-schedule', {
          email: to.trim(),
          institution: targetProf?.institution || null
        });
        sched = res.data;
        setScheduleData(sched);
      }

      if (!sched?.scheduled_iso) {
        throw new Error("Could not compute optimal delivery time window.");
      }

      // 2. Save draft
      const draft = await handleSaveDraft({ silent: true });
      if (!draft?.id) {
        throw new Error("Could not initialize email draft in CRM.");
      }

      // 3. Queue for scheduled delivery
      await api.post('/emails/send', {
        draft_id: draft.id,
        send_now: false,
        scheduled_for: sched.scheduled_iso
      });

      toast.success(
        `Scheduled for ${sched.optimal_slot_local} (Local) / ${sched.optimal_slot_ist} (IST)!`,
        { icon: '📅', duration: 7000 }
      );
      closeCompose();
    } catch (err) {
      console.error("Smart schedule error:", err);
      toast.error(formatErrorMessage(err, "Failed to schedule email."));
    } finally {
      setIsScheduling(false);
    }
  };

  return (
    <div 
      className={`fixed z-50 bg-white border border-slate-300 rounded-t-2xl shadow-2xl transition-all duration-200 flex flex-col ${
        isMaximized 
          ? 'inset-6 w-auto h-auto rounded-2xl' 
          : isMinimized 
            ? 'bottom-0 right-10 w-80 h-12' 
            : 'bottom-0 right-8 w-[720px] max-w-[95vw] h-[720px] max-h-[92vh]'
      }`}
    >
      {/* Window Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-900 text-white rounded-t-2xl select-none">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse" />
          <span className="font-semibold text-xs tracking-wide">
            PhD Outreach Composer & Intelligence
          </span>
          {scheduleData && (
            <span className="text-[10px] bg-blue-950 text-blue-300 px-2 py-0.5 rounded-full border border-blue-800/60 font-mono">
              {scheduleData.country} ({scheduleData.timezone.split('/')[1] || scheduleData.timezone})
            </span>
          )}
        </div>
        
        <div className="flex items-center gap-1.5 text-slate-400">
          <button 
            type="button"
            onClick={toggleMinimize} 
            className="p-1 hover:text-white hover:bg-slate-800 rounded transition-colors"
            title={isMinimized ? "Restore" : "Minimize"}
          >
            <Minus className="w-3.5 h-3.5" />
          </button>
          <button 
            type="button"
            onClick={toggleMaximize} 
            className="p-1 hover:text-white hover:bg-slate-800 rounded transition-colors"
            title={isMaximized ? "Exit Fullscreen" : "Maximize"}
          >
            {isMaximized ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
          </button>
          <button 
            type="button"
            onClick={closeCompose} 
            className="p-1 hover:text-rose-400 hover:bg-slate-800 rounded transition-colors"
            title="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {!isMinimized && (
        <div className="flex-1 flex flex-col overflow-hidden bg-white text-xs">
          
          {/* Recipient Selector / Input */}
          <div className="px-4 py-2 border-b border-slate-100 flex items-center gap-2">
            <span className="text-slate-400 font-semibold w-14 shrink-0">To:</span>
            <div className="flex-1 flex items-center gap-2">
              <input 
                type="email"
                value={to}
                onChange={(e) => {
                  setTo(e.target.value);
                  setSelectedProfId(null);
                }}
                placeholder="Enter professor email (e.g. prof@stanford.edu or prof@auckland.ac.nz)"
                className="flex-1 text-slate-800 font-medium focus:outline-none placeholder:text-slate-400 text-xs"
              />
              
              {matchedProf && (
                <div className="flex items-center gap-1.5 bg-blue-50 border border-blue-200/80 text-blue-700 px-2.5 py-0.5 rounded-lg text-[11px] font-semibold shrink-0">
                  <span>🎓 {matchedProf.name}</span>
                  <span className="text-blue-400 font-normal">({matchedProf.institution})</span>
                </div>
              )}
            </div>
          </div>

          {/* Smart Country & Timezone Thinking Card */}
          {scheduleData && (
            <div className="bg-gradient-to-r from-blue-50/70 via-indigo-50/50 to-slate-50 px-4 py-2.5 border-b border-blue-100 flex flex-col gap-1.5 transition-all text-[11px]">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Globe className="w-3.5 h-3.5 text-blue-600" />
                  <span className="font-bold text-slate-800">
                    {scheduleData.country} ({scheduleData.city})
                  </span>
                  <span className="text-slate-500 font-medium">
                    • {scheduleData.diff_hours_str}
                  </span>
                  <span className="bg-blue-100/80 text-blue-800 px-2 py-0.5 rounded text-[10px] font-semibold">
                    {scheduleData.activity_state}
                  </span>
                </div>
                <div className="flex items-center gap-1.5 text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 text-[10px]">
                  <span>🛡️ Friday Protected</span>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between text-slate-600 gap-y-1">
                <div>
                  <span className="text-slate-400">Prof Local: </span>
                  <span className="font-semibold text-slate-700">{scheduleData.current_local_time}</span>
                  <span className="mx-1 text-slate-300">|</span>
                  <span className="text-slate-400">India: </span>
                  <span className="font-semibold text-slate-700">{scheduleData.current_ist_time}</span>
                </div>
                <div className="text-blue-900 font-medium flex items-center gap-1">
                  <Clock className="w-3 h-3 text-blue-600 inline" />
                  <span>Optimal Delivery: </span>
                  <span className="font-bold text-blue-700">{scheduleData.optimal_slot_local}</span>
                  <span className="text-[10px] text-slate-500">({scheduleData.optimal_slot_ist})</span>
                </div>
              </div>
            </div>
          )}

          {/* Subject Line Input */}
          <div className="px-4 py-2 border-b border-slate-100 flex items-center gap-2">
            <span className="text-slate-400 font-semibold w-14 shrink-0">Subject:</span>
            <input 
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="e.g. Prospective PhD Inquiry - Distributed Systems - Sumit Raj"
              className="flex-1 text-slate-800 font-medium focus:outline-none placeholder:text-slate-400"
            />
          </div>

          {/* Anti-Spam Deliverability Meter */}
          {spamData && (
            <div className={`px-4 py-1.5 border-b flex items-center justify-between text-[11px] ${
              spamData.rating === 'EXCELLENT' ? 'bg-emerald-50/60 border-emerald-200' :
              spamData.rating === 'GOOD' ? 'bg-blue-50/60 border-blue-200' :
              spamData.rating === 'MODERATE_RISK' ? 'bg-amber-50/60 border-amber-200' :
              'bg-rose-50/60 border-rose-200'
            }`}>
              <div className="flex items-center gap-2">
                <ShieldCheck className={`w-3.5 h-3.5 ${
                  spamData.rating === 'EXCELLENT' ? 'text-emerald-600' :
                  spamData.rating === 'GOOD' ? 'text-blue-600' :
                  spamData.rating === 'MODERATE_RISK' ? 'text-amber-600' : 'text-rose-600'
                }`} />
                <span className="font-bold text-slate-800">
                  Deliverability Score: {spamData.deliverability_score}%
                </span>
                <span className="text-slate-500">
                  ({spamData.rating.replace('_', ' ')}) • {spamData.word_count} words
                </span>
                {spamData.flags.length > 0 && (
                  <span className="text-amber-700 font-semibold bg-amber-100/70 px-1.5 py-0.5 rounded text-[10px]">
                    {spamData.flags.length} spam {spamData.flags.length === 1 ? 'flag' : 'flags'}
                  </span>
                )}
              </div>

              <button
                type="button"
                onClick={() => setShowSpamDetails(!showSpamDetails)}
                className="text-blue-700 hover:text-blue-900 font-medium underline text-[10px]"
              >
                {showSpamDetails ? "Hide Checks" : "View Anti-Spam Checks"}
              </button>
            </div>
          )}

          {/* Expandable Spam Guidelines & Flags */}
          {showSpamDetails && spamData && (
            <div className="bg-slate-50 px-4 py-2 border-b border-slate-200 text-[11px] flex flex-col gap-1.5 max-h-36 overflow-y-auto">
              {spamData.flags.length > 0 && (
                <div>
                  <span className="font-bold text-rose-700 block mb-0.5">⚠️ Spam Warnings Detected:</span>
                  <ul className="list-disc list-inside text-rose-800 space-y-0.5">
                    {spamData.flags.map((f, i) => (
                      <li key={i}>{f}</li>
                    ))}
                  </ul>
                </div>
              )}
              {spamData.suggestions.length > 0 && (
                <div>
                  <span className="font-bold text-blue-700 block mb-0.5">💡 Deliverability Suggestions:</span>
                  <ul className="list-disc list-inside text-slate-700 space-y-0.5">
                    {spamData.suggestions.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              )}
              {spamData.positive_signals.length > 0 && (
                <div>
                  <span className="font-bold text-emerald-700 block mb-0.5">✓ Positive Signals:</span>
                  <ul className="list-disc list-inside text-emerald-800 space-y-0.5">
                    {spamData.positive_signals.map((p, i) => (
                      <li key={i}>{p}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* AI Controls Toolbar */}
          <div className="px-4 py-2 bg-slate-50/60 border-b border-slate-100 flex flex-wrap items-center justify-between gap-2 text-[11px]">
            <div className="flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={handleGenerateInitialDraft}
                disabled={isAiGenerating}
                className="px-3 py-1.5 bg-blue-50 hover:bg-blue-100 border border-blue-200 text-blue-700 rounded-lg font-bold flex items-center gap-1.5 transition-all disabled:opacity-50"
                title="Generate grounded initial inquiry citing professor papers"
              >
                <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                <span>{isAiGenerating ? "Generating..." : "✨ AI Initial Draft"}</span>
              </button>

              <button
                type="button"
                onClick={handleGenerateFollowUp}
                disabled={isAiGenerating}
                className="px-3 py-1.5 bg-amber-50 hover:bg-amber-100 border border-amber-200 text-amber-800 rounded-lg font-bold flex items-center gap-1.5 transition-all disabled:opacity-50"
                title="Generate polite academic follow-up inquiry"
              >
                <RotateCw className="w-3.5 h-3.5 text-amber-600" />
                <span>🔁 Follow-Up {followUpStage}</span>
              </button>

              {/* Template Selector */}
              {Array.isArray(templates) && templates.length > 0 && (
                <div className="relative">
                  <select 
                    onChange={(e) => {
                      const t = Array.isArray(templates) ? templates.find(x => x.id === parseInt(e.target.value)) : null;
                      if (t) {
                        setSubject(t.subject_template);
                        setBody(t.body_template);
                      }
                    }}
                    defaultValue=""
                    className="bg-white border border-slate-200 text-slate-700 rounded-lg px-2 py-1 text-[11px] font-medium focus:outline-none"
                  >
                    <option value="" disabled>Load Template...</option>
                    {templates.map(t => (
                      <option key={t.id} value={t.id}>{t.name}</option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2 text-slate-500">
              <span>Tone:</span>
              <select 
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="bg-transparent border-0 text-slate-700 font-semibold focus:outline-none cursor-pointer"
              >
                <option value="Formal Academic">Formal Academic</option>
                <option value="Direct & Concise">Direct & Concise</option>
                <option value="Technical Deep-Dive">Technical Deep-Dive</option>
              </select>
            </div>
          </div>

          {/* Email Body Editor */}
          <div className="flex-1 p-4 overflow-y-auto">
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder="Write your email to the professor or click '✨ AI Initial Draft' / '🔁 Follow-Up' above to generate grounded outreach..."
              className="w-full h-full resize-none focus:outline-none text-slate-800 font-sans text-xs leading-relaxed placeholder:text-slate-400"
            />
          </div>

          {/* Bottom Action Bar */}
          <div className="px-4 py-3 bg-slate-50 border-t border-slate-200 flex flex-wrap items-center justify-between gap-2">
            
            {/* Primary Action Buttons: Instant Send vs Smart Schedule */}
            <div className="flex flex-wrap items-center gap-2">
              
              {/* Option 1: Send Instant Email */}
              <button
                type="button"
                onClick={handleSendInstantEmail}
                disabled={isSending || isScheduling}
                className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md shadow-blue-600/20 flex items-center gap-1.5 transition-all disabled:opacity-50"
                title="Send email immediately right now via SMTP"
              >
                <Zap className="w-3.5 h-3.5" />
                <span>{isSending ? "Sending..." : "⚡ Send Instant Email"}</span>
              </button>

              {/* Option 2: Smart Schedule Email */}
              <button
                type="button"
                onClick={handleSmartScheduleEmail}
                disabled={isScheduling || isSending}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs shadow-md shadow-indigo-600/20 flex items-center gap-1.5 transition-all disabled:opacity-50"
                title={scheduleData ? `Schedule for ${scheduleData.optimal_slot_local} (Local)` : "Schedule at optimal local morning time"}
              >
                <Calendar className="w-3.5 h-3.5" />
                <span>{isScheduling ? "Scheduling..." : "📅 Smart Schedule Email"}</span>
              </button>

              {/* Copy Text */}
              <button
                type="button"
                onClick={handleCopyToClipboard}
                className={`px-3 py-2 rounded-xl border text-xs font-semibold flex items-center gap-1.5 transition-all ${
                  copied 
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-700' 
                    : 'bg-white hover:bg-slate-100 border-slate-200 text-slate-700 shadow-2xs'
                }`}
                title="Copy full email (Subject + Body) to clipboard"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-600" />}
                <span>{copied ? "Copied!" : "Copy Text"}</span>
              </button>

              {/* Save Draft */}
              <button
                type="button"
                onClick={() => handleSaveDraft({ silent: false })}
                className="px-3 py-2 rounded-xl bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 text-xs font-semibold flex items-center gap-1.5 shadow-2xs transition-all"
                title="Save draft in CRM outbox"
              >
                <Save className="w-3.5 h-3.5 text-slate-500" />
                <span>Save Draft</span>
              </button>

              {/* Mark as Sent */}
              <button
                type="button"
                onClick={handleMarkAsSent}
                className="px-3 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 border border-emerald-300 text-emerald-800 text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-all"
                title="Mark outreach as Sent in CRM (updates status to Sent)"
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Mark as Sent</span>
              </button>
            </div>

            {/* Discard */}
            <button
              type="button"
              onClick={() => {
                if (window.confirm("Discard this email draft?")) {
                  setBody('');
                  setSubject('');
                  closeCompose();
                }
              }}
              className="p-2 text-slate-400 hover:text-rose-600 hover:bg-slate-100 rounded-lg transition-colors"
              title="Discard draft"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GmailCompose;

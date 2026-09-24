import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Settings, 
  Mail, 
  Sparkles, 
  User, 
  Save, 
  Key, 
  ShieldCheck, 
  Server,
  CheckCircle2
} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

const SettingsPage = () => {
  const { user, updateProfile } = useAuth();

  // Profile state
  const [profileForm, setProfileForm] = useState({
    full_name: '',
    target_field: '',
    current_degree: '',
    research_interests: '',
    cv_summary: ''
  });

  // SMTP state
  const [smtpForm, setSmtpForm] = useState({
    smtp_host: 'smtp.gmail.com',
    smtp_port: 587,
    smtp_user: '',
    smtp_password: '',
    smtp_from_name: '',
    smtp_use_tls: true
  });

  const [savingProfile, setSavingProfile] = useState(false);
  const [savingSmtp, setSavingSmtp] = useState(false);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    if (user) {
      setProfileForm({
        full_name: user.full_name || '',
        target_field: user.target_field || '',
        current_degree: user.current_degree || '',
        research_interests: user.research_interests || '',
        cv_summary: user.cv_summary || ''
      });
      setSmtpForm(prev => ({
        ...prev,
        smtp_user: user.smtp_user || user.email || '',
        smtp_from_name: user.full_name || ''
      }));
    }

    const fetchHealth = async () => {
      try {
        const res = await api.get('/health');
        setHealth(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchHealth();
  }, [user]);

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSavingProfile(true);
    try {
      await updateProfile(profileForm);
      toast.success("Candidate Profile updated!");
    } catch (err) {
      toast.error("Failed to update profile.");
    } finally {
      setSavingProfile(false);
    }
  };

  const handleSaveSmtp = async (e) => {
    e.preventDefault();
    setSavingSmtp(true);
    try {
      await api.put('/auth/me/smtp', smtpForm);
      toast.success("SMTP Credentials configured for outreach!");
    } catch (err) {
      toast.error("Failed to save SMTP settings.");
    } finally {
      setSavingSmtp(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          Settings & Configurations
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Configure your candidate profile, personal SMTP email credentials, and verify AI engine status
        </p>
      </div>

      {/* Gemini Engine Pool Health Badge */}
      <div className="p-5 rounded-3xl bg-gradient-to-r from-ai-500/10 via-primary-500/10 to-slate-900 border border-ai-500/20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-ai-500/20 text-ai-400 flex items-center justify-center font-bold">
            <Sparkles className="w-5 h-5 text-ai-400 animate-pulse" />
          </div>
          <div>
            <div className="font-bold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <span>Google Gemini AI Multi-Key Pool</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Active Model: <span className="font-mono text-ai-400 font-semibold">{health?.model || 'gemini-3.6-flash'}</span> • {health?.active_gemini_keys || 6} authorized keys loaded with round-robin failover
            </p>
          </div>
        </div>
        <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 text-xs font-semibold border border-emerald-200 dark:border-emerald-800">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Quota Protected</span>
        </div>
      </div>

      {/* Candidate Profile Settings */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div className="flex items-center gap-2 font-bold text-sm text-slate-900 dark:text-slate-100 mb-4 pb-3 border-b border-slate-100 dark:border-slate-800">
          <User className="w-4 h-4 text-primary-600" />
          <span>Candidate Academic Profile (Grounded Prompt Context)</span>
        </div>

        <form onSubmit={handleSaveProfile} className="space-y-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
                Full Legal Name
              </label>
              <input
                type="text"
                required
                value={profileForm.full_name}
                onChange={(e) => setProfileForm({ ...profileForm, full_name: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
              />
            </div>
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
                Target PhD Discipline
              </label>
              <input
                type="text"
                required
                value={profileForm.target_field}
                onChange={(e) => setProfileForm({ ...profileForm, target_field: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                placeholder="e.g. Computer Science, Machine Learning"
              />
            </div>
          </div>

          <div>
            <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
              Current Degree / Institution
            </label>
            <input
              type="text"
              value={profileForm.current_degree}
              onChange={(e) => setProfileForm({ ...profileForm, current_degree: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
              placeholder="e.g. M.S. in Computer Science at Stanford University"
            />
          </div>

          <div>
            <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
              Research Interests & Technical Specialization
            </label>
            <textarea
              rows={3}
              value={profileForm.research_interests}
              onChange={(e) => setProfileForm({ ...profileForm, research_interests: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
              placeholder="e.g. Multi-Agent Systems, Alignment, LLM Efficiency, Systems for AI..."
            />
          </div>

          <div>
            <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
              CV Highlights / Accomplishments (Injected into Cold Emails)
            </label>
            <textarea
              rows={3}
              value={profileForm.cv_summary}
              onChange={(e) => setProfileForm({ ...profileForm, cv_summary: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
              placeholder="e.g. First-author paper at NeurIPS workshop. 2 years software engineering experience. Developed distributed training pipelines..."
            />
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={savingProfile}
              className="px-4 py-2 rounded-xl bg-primary-600 hover:bg-primary-700 text-white font-semibold flex items-center gap-1.5 shadow-sm disabled:opacity-50"
            >
              <Save className="w-3.5 h-3.5" />
              <span>{savingProfile ? "Saving..." : "Update Profile"}</span>
            </button>
          </div>
        </form>
      </div>

      {/* SMTP Outreach Credentials */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div className="flex items-center gap-2 font-bold text-sm text-slate-900 dark:text-slate-100 mb-4 pb-3 border-b border-slate-100 dark:border-slate-800">
          <Mail className="w-4 h-4 text-emerald-600" />
          <span>Direct Outreach SMTP Credentials (Gmail / University Mail)</span>
        </div>

        <form onSubmit={handleSaveSmtp} className="space-y-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
                SMTP Host Server
              </label>
              <input
                type="text"
                required
                value={smtpForm.smtp_host}
                onChange={(e) => setSmtpForm({ ...smtpForm, smtp_host: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl font-mono text-[11px]"
                placeholder="smtp.gmail.com"
              />
            </div>
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
                SMTP Port
              </label>
              <input
                type="number"
                required
                value={smtpForm.smtp_port}
                onChange={(e) => setSmtpForm({ ...smtpForm, smtp_port: parseInt(e.target.value) })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl font-mono text-[11px]"
                placeholder="587"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
                Email / Username
              </label>
              <input
                type="text"
                required
                value={smtpForm.smtp_user}
                onChange={(e) => setSmtpForm({ ...smtpForm, smtp_user: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
                placeholder="you@gmail.com or you@university.edu"
              />
            </div>
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
                App Password / Secret
              </label>
              <input
                type="password"
                required
                value={smtpForm.smtp_password}
                onChange={(e) => setSmtpForm({ ...smtpForm, smtp_password: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl font-mono text-[11px]"
                placeholder="•••• •••• •••• ••••"
              />
            </div>
          </div>

          <div>
            <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1">
              Sender Display Name
            </label>
            <input
              type="text"
              value={smtpForm.smtp_from_name}
              onChange={(e) => setSmtpForm({ ...smtpForm, smtp_from_name: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
              placeholder="e.g. Sumit Raj"
            />
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={savingSmtp}
              className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold flex items-center gap-1.5 shadow-sm disabled:opacity-50"
            >
              <Server className="w-3.5 h-3.5" />
              <span>{savingSmtp ? "Saving..." : "Save SMTP Credentials"}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SettingsPage;

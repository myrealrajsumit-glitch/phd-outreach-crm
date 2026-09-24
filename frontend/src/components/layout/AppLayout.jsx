import React from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import GmailCompose from '../email/GmailCompose';

const AppLayout = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-[#F6F8FC] text-slate-800 font-sans">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-5 md:p-6 overflow-y-auto max-w-[1400px] w-full mx-auto">
          {children}
        </main>
      </div>
      {/* Global Gmail Docked Compose Modal */}
      <GmailCompose />
    </div>
  );
};

export default AppLayout;

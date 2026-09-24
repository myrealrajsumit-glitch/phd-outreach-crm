import React, { createContext, useContext, useState } from 'react';

const ComposeContext = createContext();

export const ComposeProvider = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  
  // Data passed into compose
  const [composeData, setComposeData] = useState({
    professorId: null,
    recipientEmail: '',
    professorName: '',
    institution: '',
    subject: '',
    body: '',
    mode: 'new', // 'new', 'draft', 'follow_up'
    followUpStage: 1,
    previousSubject: '',
    previousBody: '',
    draftId: null
  });

  const openCompose = (data = {}) => {
    setComposeData({
      professorId: data.professorId || null,
      recipientEmail: data.recipientEmail || '',
      professorName: data.professorName || '',
      institution: data.institution || '',
      subject: data.subject || '',
      body: data.body || '',
      mode: data.mode || 'new',
      followUpStage: data.followUpStage || 1,
      previousSubject: data.previousSubject || '',
      previousBody: data.previousBody || '',
      draftId: data.draftId || null
    });
    setIsOpen(true);
    setIsMinimized(false);
  };

  const closeCompose = () => {
    setIsOpen(false);
  };

  const toggleMinimize = () => {
    setIsMinimized(prev => !prev);
  };

  const toggleMaximize = () => {
    setIsMaximized(prev => !prev);
  };

  return (
    <ComposeContext.Provider
      value={{
        isOpen,
        isMinimized,
        isMaximized,
        composeData,
        openCompose,
        closeCompose,
        toggleMinimize,
        toggleMaximize,
        setComposeData
      }}
    >
      {children}
    </ComposeContext.Provider>
  );
};

export const useCompose = () => useContext(ComposeContext);

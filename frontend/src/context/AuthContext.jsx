import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState({
    id: 1,
    full_name: 'Sumit Raj',
    email: 'candidate.test@stanford.edu',
    target_field: 'Computer Science & AI',
    current_degree: 'M.S. in Computer Science',
    research_interests: 'Large Language Models, Distributed Systems, Multi-Agent Systems'
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get('/auth/me');
        if (res.data) {
          setUser(res.data);
        }
      } catch (err) {
        console.warn("Using default local user profile:", err);
      }
    };
    fetchUser();
  }, []);

  const updateProfile = async (updates) => {
    try {
      const res = await api.put('/auth/me', updates);
      setUser(res.data);
      return res.data;
    } catch (err) {
      setUser(prev => ({ ...prev, ...updates }));
      return updates;
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, updateProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

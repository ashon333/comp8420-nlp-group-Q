import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [nickname, setNickname] = useState(() => {
    return localStorage.getItem('nickname') || null;
  });

  const login = (name) => {
    setNickname(name);
    localStorage.setItem('nickname', name);
  };

  const logout = () => {
    setNickname(null);
    localStorage.removeItem('nickname');
  };

  return (
    <AuthContext.Provider value={{ nickname, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

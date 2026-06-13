import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Sparkles } from 'lucide-react';

export default function Login() {
  const [nickname, setNickname] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (nickname.trim()) {
      login(nickname.trim());
      navigate('/');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1e0d00] via-[#3a1a00] to-[#0a0500] flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl">
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 bg-orange-500/10 border border-orange-500/30 rounded-2xl flex items-center justify-center">
            <Sparkles className="text-orange-500 w-8 h-8" />
          </div>
        </div>
        <h2 className="text-3xl font-bold text-white text-center mb-2">Welcome to Congo Shop</h2>
        <p className="text-white/60 text-center mb-8 text-sm">Enter a nickname to enter the portal</p>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="nickname" className="block text-xs font-semibold text-orange-200/80 uppercase tracking-wider mb-2">Nickname</label>
            <input
              type="text"
              id="nickname"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              className="w-full px-4 py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
              placeholder="e.g. CoffeeLover99"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white font-bold py-3.5 rounded-xl hover:opacity-95 transition-opacity focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-stone-900 shadow-lg shadow-orange-500/20"
          >
            Enter Portal
          </button>
        </form>
      </div>
    </div>
  );
}

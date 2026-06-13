import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Home, ShoppingBag, Info, LogOut, ShoppingCart, Menu } from 'lucide-react';

export default function Navbar() {
  const { nickname, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { name: 'Home', path: '/', icon: Home },
    // { name: 'Products', path: '/products', icon: ShoppingBag },
    { name: 'About', path: '/about', icon: Info },
  ];

  return (
    <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20 items-center">
          {/* Logo */}
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
            <div className="bg-orange-500 p-2 rounded-xl text-white shadow-md shadow-orange-500/10">
              <ShoppingCart className="w-5 h-5" />
            </div>
            <span className="text-xl font-extrabold text-slate-800 tracking-tight">Congo Shop</span>
          </div>

          {/* Nav Items (Every menu has an icon, Image search next to Home) */}
          <div className="hidden md:flex items-center space-x-6">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <button
                  key={item.name}
                  onClick={() => navigate(item.path)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 ${isActive
                    ? 'bg-orange-500 text-white shadow-lg shadow-orange-500/20'
                    : 'text-slate-600 hover:text-orange-500 hover:bg-orange-50/50'
                    }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.name}</span>
                </button>
              );
            })}
          </div>

          {/* User Info & Actions */}
          <div className="flex items-center space-x-4">
            <span className="text-slate-500 font-semibold text-xs bg-slate-100 px-3 py-1.5 rounded-full hidden sm:block">
              Hi, {nickname}
            </span>
            <button
              onClick={() => { logout(); navigate('/login'); }}
              className="bg-orange-100 hover:bg-orange-200 text-orange-600 px-4 py-2 rounded-xl font-bold transition-all text-xs flex items-center gap-2 active:scale-95"
            >
              Sign Out <LogOut className="w-3.5 h-3.5" />
            </button>
            <button className="md:hidden text-slate-600 p-2 hover:bg-slate-50 rounded-xl">
              <Menu className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

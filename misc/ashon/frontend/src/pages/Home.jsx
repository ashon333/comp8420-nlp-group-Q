import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import { Search, Sparkles, Star, ChevronRight, Plus } from 'lucide-react';
import Navbar from '../components/Navbar';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export default function Home() {
  const { nickname, logout } = useAuth();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [isPromptSearch, setIsPromptSearch] = useState(false);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const productsRef = useRef(null);

  useEffect(() => {
    fetchTopProducts();
  }, []);

  const fetchTopProducts = async () => {
    try {
      const res = await fetch(`${API_BASE}/products`);
      const data = await res.json();
      setProducts(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      fetchTopProducts();
      return;
    }
    
    setLoading(true);
    try {
      const endpoint = isPromptSearch ? '/products/semantic-search' : '/products/search';
      const body = isPromptSearch ? { prompt: query } : { query: query };
      
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      setProducts(data);

      // Smooth scroll to results
      setTimeout(() => {
        productsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);

    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fffcf9] font-sans">
      <Navbar />

      <main>
        {/* Hero Section */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mt-6">
          <div className="bg-gradient-to-r from-[#ff4d4d] to-[#ff9900] rounded-[2rem] overflow-hidden flex flex-col md:flex-row shadow-xl">
            <div className="md:w-1/2 p-10 md:p-16 flex flex-col justify-center">
              <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
                Style Meets <br/> Comfort
              </h1>
              <p className="text-white/90 text-lg mb-8 max-w-md">
                Discover our exclusive collection of products designed for comfort and style without limits.
              </p>
              
              {/* Search Form inside Hero */}
              <form onSubmit={handleSearch} className="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 shadow-lg mb-8">
                <div className="flex flex-col sm:flex-row gap-3">
                  <div className="relative flex-1">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      {isPromptSearch ? <Sparkles className="h-5 w-5 text-orange-200" /> : <Search className="h-5 w-5 text-orange-200" />}
                    </div>
                    <input
                      type="text"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      placeholder={isPromptSearch ? "E.g., I want to make coffee..." : "Search products..."}
                      className="block w-full pl-10 pr-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-white/70 focus:ring-2 focus:ring-white focus:outline-none transition-all"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-white text-orange-600 px-6 py-3 rounded-xl font-bold hover:bg-orange-50 transition-colors shadow-md disabled:opacity-80 whitespace-nowrap"
                  >
                    {loading ? 'Searching...' : 'Search'}
                  </button>
                </div>
                
                <div className="flex items-center justify-start space-x-3 mt-3">
                  <span className={`text-xs ${!isPromptSearch ? 'text-white font-semibold' : 'text-white/70'}`}>Normal</span>
                  <button
                    type="button"
                    onClick={() => setIsPromptSearch(!isPromptSearch)}
                    className={`relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none bg-white/30`}
                  >
                    <span className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${isPromptSearch ? 'translate-x-4' : 'translate-x-0'}`} />
                  </button>
                  <span className={`text-xs flex items-center ${isPromptSearch ? 'text-white font-semibold' : 'text-white/70'}`}>
                    AI Semantic <Sparkles className="w-3 h-3 ml-1" />
                  </span>
                </div>
              </form>              
            </div>
            
            <div className="md:w-1/2 relative min-h-[300px] bg-[url('https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=800')] bg-cover bg-center">
               {/* Just using a generic placeholder image for the hero */}
               <div className="absolute inset-0 bg-gradient-to-l from-transparent to-[#ff9900]/80"></div>
            </div>
          </div>
        </section>


        {/* Products Section */}
        <section ref={productsRef} className="bg-[#ffebcc] py-16 px-4 sm:px-6 lg:px-8 mt-8 rounded-t-[3rem]">
          <div className="max-w-7xl mx-auto">
            <div className="flex justify-between items-end mb-10">
              <h2 className="text-3xl font-bold text-slate-800">
                {query && !loading ? 'Search Results' : 'Best Selling Product'}
              </h2>
              <a href="#" className="text-orange-600 font-semibold flex items-center">View All <ChevronRight className="w-5 h-5 ml-1"/></a>
            </div>
            
            {products.length === 0 ? (
              <div className="text-center py-16 bg-white/50 backdrop-blur-sm rounded-3xl border border-orange-200">
                <p className="text-orange-800 font-medium">No products found. Try a different search.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {products.map((product) => (
                  <Link to={`/product/${product.id}`} key={product.id} className="bg-white rounded-3xl p-4 shadow-sm hover:shadow-xl transition-all duration-300 group flex flex-col">
                    <div className="bg-[#f8f9fa] rounded-2xl aspect-square mb-4 overflow-hidden flex items-center justify-center p-4 relative">
                      <img
                        src={product.image_url}
                        alt={product.name}
                        className="object-contain h-full w-full group-hover:scale-110 transition-transform duration-500 mix-blend-multiply"
                      />
                    </div>
                    
                    <div className="flex-1 flex flex-col px-2 pb-2">
                      <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">{product.category}</p>
                      <h3 className="text-base font-bold text-slate-800 mb-2 line-clamp-1">{product.name}</h3>
                      
                      <div className="flex items-center gap-1 mb-4">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={`w-3.5 h-3.5 ${i < Math.floor(product.average_rating) ? 'text-orange-500 fill-current' : 'text-slate-300'}`} />
                        ))}
                      </div>
                      
                      <div className="mt-auto flex items-center justify-between">
                        <span className="text-xl font-bold text-slate-900">${product.price.toFixed(2)}</span>
                        <button className="bg-orange-100 text-orange-600 p-2 rounded-full hover:bg-orange-500 hover:text-white transition-colors">
                          <Plus className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </section>
        
        {/* Categories (Placeholder for the design) */}
        <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-800 mb-8">Shop By Category</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="relative rounded-3xl overflow-hidden h-64 group cursor-pointer">
              <img src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=600" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" alt="Women" />
              <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                <span className="text-white text-2xl font-bold tracking-widest uppercase">Women</span>
              </div>
            </div>
            <div className="relative rounded-3xl overflow-hidden h-64 group cursor-pointer">
              <img src="https://images.unsplash.com/photo-1516257984-b1b4d707412e?q=80&w=600" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" alt="Men" />
              <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                <span className="text-white text-2xl font-bold tracking-widest uppercase">Men</span>
              </div>
            </div>
            <div className="relative rounded-3xl overflow-hidden h-64 group cursor-pointer">
              <img src="https://images.unsplash.com/photo-1526506114631-f1f3a364be2c?q=80&w=600" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" alt="Sports" />
              <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                <span className="text-white text-2xl font-bold tracking-widest uppercase">Sports</span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

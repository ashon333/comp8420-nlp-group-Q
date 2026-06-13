import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import { Search, Sparkles, ChevronRight, Plus } from 'lucide-react';
import Navbar from '../components/Navbar';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export default function Home() {
  const { nickname, logout } = useAuth();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);

  const productsRef = useRef(null);

  useEffect(() => {
    fetchTopProducts();
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const res = await fetch(`${API_BASE}/categories`);
      const data = await res.json();
      setCategories(data.categories || []);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchTopProducts = async () => {
    try {
      const res = await fetch(`${API_BASE}/products`);
      const data = await res.json();
      setProducts(data.products || []);
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
      const endpoint = '/search'; // Backend handles semantic search natively
      const body = { query: query };

      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      setProducts(data.results || []);

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
          <div className="bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-800 rounded-[2rem] overflow-hidden flex flex-col md:flex-row shadow-2xl relative">
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10 mix-blend-overlay pointer-events-none"></div>
            <div className="md:w-1/2 p-10 md:p-16 flex flex-col justify-center relative z-10">
              <h1 className="text-4xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-500 mb-6 leading-tight drop-shadow-sm">
                Next-Gen <br /> Intelligence
              </h1>
              <p className="text-slate-300 text-lg mb-8 max-w-md font-medium">
                Discover our exclusive collection of AI-powered electronics and smart home devices.
              </p>

              {/* Search Form inside Hero */}
              <div className="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 shadow-lg mb-8 flex flex-col gap-4">
                <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
                  <div className="relative flex-1 group">
                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                      <Search className="h-5 w-5 text-cyan-400 drop-shadow-[0_0_8px_rgba(34,211,238,0.8)]" />
                    </div>
                    <input
                      type="text"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      placeholder={"Search electronics..."}
                      className="block w-full pl-12 pr-4 py-4 bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl text-white placeholder-slate-300 focus:ring-2 focus:ring-fuchsia-400 focus:border-transparent focus:outline-none transition-all shadow-inner"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-8 py-4 rounded-2xl font-bold hover:scale-105 hover:shadow-[0_0_20px_rgba(34,211,238,0.5)] transition-all duration-300 disabled:opacity-70 disabled:hover:scale-100 whitespace-nowrap"
                  >
                    {loading ? 'Searching...' : 'Search'}
                  </button>
                </form>
                

              </div>
            </div>

            <div className="md:w-1/2 relative min-h-[350px] bg-[url('https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=800')] bg-cover bg-center">
              <div className="absolute inset-0 bg-gradient-to-r from-slate-900 to-transparent"></div>
              <div className="absolute inset-0 bg-indigo-900/20 mix-blend-multiply"></div>
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
              <a href="#" className="text-orange-600 font-semibold flex items-center">View All <ChevronRight className="w-5 h-5 ml-1" /></a>
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
                        src={product.image}
                        alt={product.name}
                        className="object-contain h-full w-full group-hover:scale-110 transition-transform duration-500 mix-blend-multiply"
                      />
                    </div>

                    <div className="flex-1 flex flex-col px-2 pb-2">
                      <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">{product.category}</p>
                      <h3 className="text-base font-bold text-slate-800 mb-2 line-clamp-1">{product.name}</h3>



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

        {/* Categories (Updated for Amazon Dataset) */}
        <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <h2 className="text-3xl font-extrabold text-slate-800 mb-10 text-center relative">
            Shop By Category
            <div className="absolute w-24 h-1 bg-gradient-to-r from-cyan-400 to-blue-500 bottom-[-12px] left-1/2 transform -translate-x-1/2 rounded-full"></div>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {categories.map((cat, idx) => (
              <div key={idx} className="relative rounded-[2rem] overflow-hidden h-72 group cursor-pointer shadow-lg hover:shadow-2xl transition-all duration-500 bg-white">
                <img src={cat.image} className="w-full h-full object-contain p-8 group-hover:scale-110 transition-transform duration-700 mix-blend-multiply" alt={cat.name} />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/40 to-transparent flex items-end justify-center pb-8">
                  <span className="text-white text-2xl font-bold tracking-widest uppercase group-hover:-translate-y-2 transition-transform duration-300 text-center px-4 line-clamp-1">{cat.name}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
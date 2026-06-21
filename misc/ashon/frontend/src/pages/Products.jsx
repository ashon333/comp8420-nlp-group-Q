import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { Link } from 'react-router-dom';
import { Star, Plus, SlidersHorizontal, ArrowUpDown } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export default function Products() {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filter states
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [maxPrice, setMaxPrice] = useState(250);
  const [minRating, setMinRating] = useState(0);

  // Sorting state
  const [sortBy, setSortBy] = useState('rating-desc'); // rating-desc, price-asc, price-desc

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await fetch(`${API_BASE}/products`);
      const data = await res.json();
      setProducts(data);
      setFilteredProducts(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Run filters and sorting
  useEffect(() => {
    let result = [...products];

    // Category filter
    if (selectedCategory !== 'All') {
      result = result.filter(p => p.category === selectedCategory);
    }

    // Price filter
    result = result.filter(p => p.price <= maxPrice);

    // Rating filter
    result = result.filter(p => p.average_rating >= minRating);

    // Sorting
    if (sortBy === 'price-asc') {
      result.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-desc') {
      result.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'rating-desc') {
      result.sort((a, b) => b.average_rating - a.average_rating);
    }

    setFilteredProducts(result);
  }, [products, selectedCategory, maxPrice, minRating, sortBy]);

  const categories = ['All', 'Running', 'Trail', 'Comfort', 'Lifestyle'];

  return (
    <div className="min-h-screen bg-[#fffcf9] font-sans pb-16">
      <Navbar />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex flex-col md:flex-row gap-8">
          
          {/* Sidebar / Filters (Left Column) */}
          <aside className="w-full md:w-64 bg-white rounded-3xl p-6 border border-slate-100 shadow-sm self-start shadow-orange-500/5">
            <div className="flex items-center gap-2 mb-6 border-b border-slate-50 pb-4">
              <SlidersHorizontal className="w-4 h-4 text-orange-500" />
              <h2 className="font-bold text-slate-800 text-base">Filters</h2>
            </div>

            {/* Category Filter */}
            <div className="mb-6">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Category</h3>
              <div className="space-y-2">
                {categories.map(cat => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`w-full text-left px-3.5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                      selectedCategory === cat
                        ? 'bg-orange-50 text-orange-600'
                        : 'text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            {/* Max Price Filter */}
            <div className="mb-6">
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Max Price</h3>
                <span className="text-sm font-bold text-orange-600">${maxPrice}</span>
              </div>
              <input
                type="range"
                min="50"
                max="300"
                step="10"
                value={maxPrice}
                onChange={e => setMaxPrice(Number(e.target.value))}
                className="w-full h-1.5 bg-orange-100 rounded-lg appearance-none cursor-pointer accent-orange-500"
              />
            </div>

            {/* Min Rating Filter */}
            <div>
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Min Rating</h3>
              <div className="flex gap-1.5">
                {[1, 2, 3, 4, 5].map(rating => (
                  <button
                    key={rating}
                    onClick={() => setMinRating(minRating === rating ? 0 : rating)}
                    className={`p-2 rounded-lg border transition-all ${
                      minRating >= rating
                        ? 'border-orange-500 bg-orange-50 text-orange-500'
                        : 'border-slate-100 bg-white text-slate-300 hover:border-slate-200'
                    }`}
                  >
                    <Star className="w-4 h-4 fill-current" />
                  </button>
                ))}
              </div>
            </div>
          </aside>

          {/* Product Listing (Right Column) */}
          <div className="flex-1">
            {/* Sorting Header */}
            <div className="bg-white rounded-3xl p-4 border border-slate-100 shadow-sm shadow-orange-500/5 mb-6 flex flex-col sm:flex-row justify-between items-center gap-4">
              <p className="text-sm text-slate-500 font-medium">
                Showing <span className="font-bold text-slate-800">{filteredProducts.length}</span> products
              </p>
              
              <div className="flex items-center gap-2">
                <ArrowUpDown className="w-4 h-4 text-slate-400" />
                <select
                  value={sortBy}
                  onChange={e => setSortBy(e.target.value)}
                  className="bg-slate-50 border-0 rounded-xl px-3.5 py-2 text-sm font-semibold text-slate-600 focus:ring-2 focus:ring-orange-500 focus:outline-none"
                >
                  <option value="rating-desc">Highest Rated</option>
                  <option value="price-asc">Price: Low to High</option>
                  <option value="price-desc">Price: High to Low</option>
                </select>
              </div>
            </div>

            {loading ? (
              <div className="text-center py-20 text-orange-500 font-bold">Loading products...</div>
            ) : filteredProducts.length === 0 ? (
              <div className="bg-white rounded-3xl p-16 text-center border border-slate-100">
                <p className="text-slate-400 font-bold text-sm">No products matches the active filters.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredProducts.map(product => (
                  <Link to={`/product/${product.id}`} key={product.id} className="bg-white rounded-3xl p-4 shadow-sm hover:shadow-xl transition-all duration-300 group flex flex-col border border-slate-50">
                    <div className="bg-[#f8f9fa] rounded-2xl aspect-square mb-4 overflow-hidden flex items-center justify-center p-4 relative">
                      <img
                        src={product.image_url}
                        alt={product.name}
                        className="object-contain h-full w-full group-hover:scale-110 transition-transform duration-500 mix-blend-multiply"
                      />
                    </div>
                    
                    <div className="flex-grow flex flex-col px-2 pb-2">
                      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">{product.category}</p>
                      <h3 className="text-sm font-bold text-slate-800 mb-2 line-clamp-1">{product.name}</h3>
                      
                      <div className="flex items-center gap-0.5 mb-4">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={`w-3.5 h-3.5 ${i < Math.floor(product.average_rating) ? 'text-orange-500 fill-current' : 'text-slate-200'}`} />
                        ))}
                      </div>
                      
                      <div className="mt-auto flex items-center justify-between">
                        <span className="text-lg font-extrabold text-slate-900">${product.price.toFixed(2)}</span>
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

        </div>
      </main>
    </div>
  );
}

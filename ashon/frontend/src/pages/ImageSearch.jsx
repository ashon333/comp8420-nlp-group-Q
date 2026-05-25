import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Upload, ArrowLeft, Image as ImageIcon, Star, Sparkles } from 'lucide-react';
import Navbar from '../components/Navbar';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export default function ImageSearch() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setResults([]);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const res = await fetch(`${API_BASE}/images/search`, {
        method: 'POST',
        body: formData,
      });
      
      if (res.ok) {
        const data = await res.json();
        setResults(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fffcf9] pb-16">
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 mt-10">
        <button onClick={() => navigate(-1)} className="flex items-center text-slate-500 hover:text-orange-500 mb-8 transition-colors font-medium">
          <ArrowLeft className="w-5 h-5 mr-2" /> Back
        </button>

        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-3xl bg-orange-100 mb-4 shadow-sm">
            <ImageIcon className="w-7 h-7 text-orange-600" />
          </div>
          <h1 className="text-3xl font-bold text-slate-800 mb-4">Visual Search</h1>
          <p className="text-base text-slate-500 max-w-xl mx-auto leading-relaxed">Upload an image of a product you like, and we'll find similar items in our catalog using AI visual matching.</p>
        </div>

        <div className="bg-white rounded-3xl shadow-sm border border-slate-100 p-8 mb-10 max-w-2xl mx-auto shadow-orange-500/5">
          <div className="border-2 border-dashed border-orange-200 rounded-2xl p-8 text-center transition-colors hover:border-orange-400 bg-orange-50/20">
            {!previewUrl ? (
              <>
                <Upload className="w-12 h-12 text-orange-300 mx-auto mb-4" />
                <p className="text-slate-700 font-bold mb-2 text-sm">Drag and drop an image, or click to browse</p>
                <p className="text-slate-400 text-xs mb-6">Supports JPG, PNG, WEBP (Max 5MB)</p>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer bg-white border border-slate-200 text-slate-700 font-bold py-2.5 px-6 rounded-xl hover:bg-slate-50 transition-colors inline-block text-xs"
                >
                  Browse Files
                </label>
              </>
            ) : (
              <div className="flex flex-col items-center">
                <div className="relative mb-6 group">
                  <img src={previewUrl} alt="Preview" className="max-h-64 rounded-2xl shadow-md object-contain" />
                  <button 
                    onClick={() => { setFile(null); setPreviewUrl(null); setResults([]); }}
                    className="absolute -top-3 -right-3 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-sm font-bold"
                  >
                    &times;
                  </button>
                </div>
                <button
                  onClick={handleUpload}
                  disabled={loading}
                  className="bg-orange-500 text-white font-bold py-3.5 px-8 rounded-xl hover:bg-orange-600 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition-all flex items-center shadow-lg shadow-orange-500/10 disabled:opacity-70 text-sm"
                >
                  {loading ? (
                    <>Scanning image...</>
                  ) : (
                    <><Sparkles className="w-4 h-4 mr-2" /> Find Similar Products</>
                  )}
                </button>
              </div>
            )}
          </div>
        </div>

        {results.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-slate-800 mb-6 flex items-center">
              <Sparkles className="w-5 h-5 text-orange-500 mr-2" /> We found these matches
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((product) => (
                <Link to={`/product/${product.id}`} key={product.id} className="group flex flex-col bg-white rounded-3xl p-4 shadow-sm hover:shadow-xl transition-all duration-300">
                  <div className="bg-[#f8f9fa] rounded-2xl aspect-square mb-4 overflow-hidden flex items-center justify-center p-4">
                    <img
                      src={product.image_url}
                      alt={product.name}
                      className="h-full w-full object-contain mix-blend-multiply group-hover:scale-105 transition-transform duration-500"
                    />
                  </div>
                  <div className="px-2 pb-2 flex-1 flex flex-col">
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">{product.category}</p>
                    <h3 className="text-base font-bold text-slate-800 mb-2 line-clamp-1">{product.name}</h3>
                    <p className="text-xs text-slate-400 mb-4 line-clamp-2 leading-relaxed">{product.description}</p>
                    <div className="flex items-center justify-between mt-auto">
                      <span className="text-lg font-bold text-slate-900">${product.price.toFixed(2)}</span>
                      <div className="flex items-center">
                        <Star className="w-3.5 h-3.5 text-orange-500 mr-1 fill-current" />
                        <span className="text-xs font-bold text-slate-700">{product.average_rating}</span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

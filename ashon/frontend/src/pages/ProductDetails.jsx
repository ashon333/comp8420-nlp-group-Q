import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Star, ArrowLeft, Send, AlertTriangle, CheckCircle, BrainCircuit, ThumbsUp, ThumbsDown } from 'lucide-react';
import Navbar from '../components/Navbar';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export default function ProductDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { nickname } = useAuth();
  
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // New review form
  const [newReviewText, setNewReviewText] = useState('');
  const [newReviewRating, setNewReviewRating] = useState(5);
  const [submitting, setSubmitting] = useState(false);
  
  // Analysis modal
  const [selectedReview, setSelectedReview] = useState(null);

  useEffect(() => {
    fetchProductDetails();
  }, [id]);

  const fetchProductDetails = async () => {
    try {
      const prodRes = await fetch(`${API_BASE}/products/${id}`);
      if (prodRes.ok) setProduct(await prodRes.json());
      
      const revRes = await fetch(`${API_BASE}/products/${id}/reviews`);
      if (revRes.ok) setReviews(await revRes.json());
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const submitReview = async (e) => {
    e.preventDefault();
    if (!newReviewText.trim()) return;
    
    setSubmitting(true);
    try {
      const res = await fetch(`${API_BASE}/products/${id}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_nickname: nickname,
          rating: newReviewRating,
          text: newReviewText
        })
      });
      if (res.ok) {
        const addedReview = await res.json();
        setReviews([...reviews, addedReview]);
        setNewReviewText('');
        setNewReviewRating(5);
        // Automatically show analysis for the newly submitted review
        setSelectedReview(addedReview);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center text-orange-600 font-bold">Loading...</div>;
  if (!product) return <div className="min-h-screen flex items-center justify-center text-slate-600">Product not found.</div>;

  return (
    <div className="min-h-screen bg-[#fffcf9] pb-16">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-10">
        <button onClick={() => navigate(-1)} className="flex items-center text-slate-500 hover:text-orange-500 mb-6 transition-colors font-medium">
          <ArrowLeft className="w-5 h-5 mr-2" /> Back to Search
        </button>
        
        {/* Product Header */}
        <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden mb-8 flex flex-col md:flex-row shadow-orange-500/5">
          <div className="md:w-1/3 bg-[#f8f9fa] p-6 flex items-center justify-center">
            <img src={product.image_url} alt={product.name} className="w-full h-64 md:h-full object-contain max-h-[300px] mix-blend-multiply" />
          </div>
          <div className="p-8 md:w-2/3 flex flex-col justify-center">
            <div className="flex justify-between items-start mb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-orange-500 mb-1 block">{product.category}</span>
                <h1 className="text-3xl font-bold text-slate-800">{product.name}</h1>
              </div>
              <span className="text-2xl font-bold text-slate-900">${product.price.toFixed(2)}</span>
            </div>
            <p className="text-slate-500 mb-6 text-base leading-relaxed">{product.description}</p>
            <div className="flex items-center bg-orange-50 self-start px-3 py-1.5 rounded-xl">
              <Star className="w-4 h-4 text-orange-500 mr-2 fill-current" />
              <span className="font-bold text-orange-700 text-sm">{product.average_rating} Average Rating</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Reviews List */}
          <div>
            <h2 className="text-xl font-bold text-slate-800 mb-6">Customer Reviews</h2>
            {reviews.length === 0 ? (
              <p className="text-slate-500 bg-white p-6 rounded-2xl border border-slate-100">No reviews yet. Be the first!</p>
            ) : (
              <div className="space-y-4">
                {reviews.map(review => (
                  <div 
                    key={review.id} 
                    onClick={() => setSelectedReview(review)}
                    className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md cursor-pointer transition-all hover:border-orange-300"
                  >
                    <div className="flex justify-between items-start mb-3">
                      <span className="font-bold text-slate-800 text-sm">{review.user_nickname}</span>
                      <div className="flex">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={`w-3.5 h-3.5 ${i < review.rating ? 'text-orange-500 fill-current' : 'text-slate-200'}`} />
                        ))}
                      </div>
                    </div>
                    <p className="text-slate-500 text-xs leading-relaxed line-clamp-3">{review.text}</p>
                    <div className="mt-4 text-xs text-orange-600 font-semibold flex items-center">
                      <BrainCircuit className="w-3.5 h-3.5 mr-1" /> Click to view AI Analysis
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Add Review Form */}
          <div>
            <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm sticky top-24 shadow-orange-500/5">
              <h3 className="text-lg font-bold text-slate-800 mb-4">Write a Review</h3>
              <form onSubmit={submitReview}>
                <div className="mb-4">
                  <label className="block text-xs font-semibold text-slate-400 uppercase mb-2">Rating</label>
                  <div className="flex space-x-2">
                    {[1, 2, 3, 4, 5].map(star => (
                      <button
                        type="button"
                        key={star}
                        onClick={() => setNewReviewRating(star)}
                        className="focus:outline-none transition-transform active:scale-95"
                      >
                        <Star className={`w-8 h-8 ${star <= newReviewRating ? 'text-orange-500 fill-current' : 'text-slate-200'}`} />
                      </button>
                    ))}
                  </div>
                </div>
                <div className="mb-6">
                  <label className="block text-xs font-semibold text-slate-400 uppercase mb-2">Your Review</label>
                  <textarea
                    rows="4"
                    value={newReviewText}
                    onChange={(e) => setNewReviewText(e.target.value)}
                    className="w-full px-4 py-3 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-orange-500 focus:border-orange-500 focus:outline-none transition-all resize-none text-sm"
                    placeholder="What did you think about this product?"
                    required
                  ></textarea>
                </div>
                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full bg-orange-500 text-white font-bold py-3.5 rounded-xl hover:bg-orange-600 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 flex items-center justify-center transition-colors shadow-lg shadow-orange-500/10 disabled:opacity-70"
                >
                  {submitting ? 'Analyzing...' : <><Send className="w-4 h-4 mr-2" /> Submit Review</>}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      {/* Analysis Modal */}
      {selectedReview && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-3xl shadow-xl max-w-lg w-full overflow-hidden border border-slate-100 transform transition-all">
            <div className="bg-gradient-to-r from-orange-500 to-red-500 px-6 py-5 flex justify-between items-center">
              <h3 className="text-lg font-bold text-white flex items-center">
                <BrainCircuit className="w-5 h-5 mr-2" /> AI Review Analysis
              </h3>
              <button onClick={() => setSelectedReview(null)} className="text-white/80 hover:text-white text-2xl leading-none">&times;</button>
            </div>
            
            <div className="p-6">
              <div className="mb-6 p-4 bg-[#fffcf9] rounded-2xl border border-orange-100">
                <p className="text-slate-700 italic text-sm leading-relaxed">"{selectedReview.text}"</p>
                <div className="mt-3 text-xs font-bold text-orange-600">- {selectedReview.user_nickname}</div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 rounded-xl bg-[#fdfdfd] border border-slate-100">
                  <span className="text-xs font-semibold text-slate-500 uppercase">Sentiment</span>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    selectedReview.analysis.sentiment === 'Positive' ? 'bg-green-50 text-green-700' :
                    selectedReview.analysis.sentiment === 'Negative' ? 'bg-red-50 text-red-700' : 'bg-slate-50 text-slate-700'
                  }`}>
                    {selectedReview.analysis.sentiment}
                  </span>
                </div>
                
                <div className="flex items-center justify-between p-3 rounded-xl bg-[#fdfdfd] border border-slate-100">
                  <span className="text-xs font-semibold text-slate-500 uppercase">Recommendation</span>
                  <div className="flex items-center">
                    {selectedReview.analysis.does_recommend ? 
                      <><ThumbsUp className="w-4 h-4 text-green-600 mr-2" /><span className="text-green-700 text-xs font-bold">Recommends</span></> : 
                      <><ThumbsDown className="w-4 h-4 text-red-600 mr-2" /><span className="text-red-700 text-xs font-bold">Does Not Recommend</span></>
                    }
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 rounded-xl bg-[#fdfdfd] border border-slate-100">
                  <span className="text-xs font-semibold text-slate-500 uppercase">AI Generated</span>
                  <div className="flex items-center">
                    {selectedReview.analysis.written_using_ai ? 
                      <><AlertTriangle className="w-4 h-4 text-amber-500 mr-2" /><span className="text-amber-700 text-xs font-bold">Likely AI</span></> : 
                      <><CheckCircle className="w-4 h-4 text-green-600 mr-2" /><span className="text-green-700 text-xs font-bold">Human Written</span></>
                    }
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 rounded-xl bg-[#fdfdfd] border border-slate-100">
                  <span className="text-xs font-semibold text-slate-500 uppercase">Authenticity</span>
                  <div className="flex items-center">
                    {selectedReview.analysis.is_fake_review ? 
                      <><AlertTriangle className="w-4 h-4 text-red-500 mr-2" /><span className="text-red-700 text-xs font-bold">Flagged Fake</span></> : 
                      <><CheckCircle className="w-4 h-4 text-green-600 mr-2" /><span className="text-green-700 text-xs font-bold">Appears Authentic</span></>
                    }
                  </div>
                </div>

                {selectedReview.analysis.matches_product !== null && (
                  <div className="flex items-center justify-between p-3 rounded-xl bg-[#fdfdfd] border border-slate-100">
                    <span className="text-xs font-semibold text-slate-500 uppercase">Matches Product</span>
                    <div className="flex items-center">
                      {selectedReview.analysis.matches_product ? 
                        <><CheckCircle className="w-4 h-4 text-green-600 mr-2" /><span className="text-green-700 text-xs font-bold">Relevant</span></> : 
                        <><AlertTriangle className="w-4 h-4 text-red-500 mr-2" /><span className="text-red-700 text-xs font-bold">Irrelevant Content</span></>
                      }
                    </div>
                  </div>
                )}
              </div>
            </div>
            
            <div className="bg-[#fffcf9] px-6 py-4 border-t border-slate-100">
              <button 
                onClick={() => setSelectedReview(null)}
                className="w-full bg-white border border-slate-200 text-slate-700 font-bold py-2.5 rounded-xl hover:bg-slate-50 transition-colors text-sm"
              >
                Close Analysis
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

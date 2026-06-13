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
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);

  // New review form
  const [newReviewText, setNewReviewText] = useState('');
  const [newReviewRating, setNewReviewRating] = useState(5);
  const [submitting, setSubmitting] = useState(false);

  // Analysis modal
  const [selectedReview, setSelectedReview] = useState(null);
  const [analyzingReview, setAnalyzingReview] = useState(false);

  const [filterRating, setFilterRating] = useState(0);
  const [sortBy, setSortBy] = useState('newest');

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchProductDetails();
  }, [id]);

  useEffect(() => {
    setPage(1);
  }, [filterRating, sortBy]);

  useEffect(() => {
    fetchReviews();
  }, [id, filterRating, sortBy, page]);

  const handleReviewClick = async (review) => {
    setSelectedReview(review);
    if (!review.analysis) {
      setAnalyzingReview(true);
      try {
        const res = await fetch(`${API_BASE}/reviews/${review.id}/analysis`);
        if (res.ok) {
          const analysisData = await res.json();
          const updatedReview = { ...review, analysis: analysisData };
          setSelectedReview(updatedReview);
          setReviews(prev => prev.map(r => r.id === review.id ? updatedReview : r));
        }
      } catch (e) {
        console.error(e);
      } finally {
        setAnalyzingReview(false);
      }
    }
  };

  const fetchReviews = async () => {
    try {
      const revRes = await fetch(`${API_BASE}/products/${id}/reviews?rating=${filterRating}&sort_by=${sortBy}&page=${page}&limit=5`);
      if (revRes.ok) {
        const data = await revRes.json();
        setReviews(data.reviews);
        setTotalPages(data.pages);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const fetchProductDetails = async () => {
    try {
      const prodRes = await fetch(`${API_BASE}/products/${id}`);
      if (prodRes.ok) setProduct(await prodRes.json());

      const analysisRes = await fetch(`${API_BASE}/products/${id}/analysis`);
      if (analysisRes.ok) setAnalysis(await analysisRes.json());
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
        setNewReviewText('');
        setNewReviewRating(5);
        fetchReviews(); // Refetch to get the updated paginated list
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
            <img src={product.image_url || product.image} alt={product.name} className="w-full h-64 md:h-full object-contain max-h-[300px] mix-blend-multiply" />
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
              <span className="font-bold text-orange-700 text-sm">{product.average_rating || analysis?.avg_rating || 0} Average Rating</span>
            </div>
          </div>
        </div>

        {/* AI Analysis Section */}
        {analysis && (
          <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden mb-8 p-8 shadow-orange-500/5">
            <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center">
              <BrainCircuit className="w-6 h-6 text-orange-500 mr-2" />
              Real-time AI Sentiment Analysis
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="col-span-1">
                <div className="text-sm font-semibold text-slate-500 uppercase mb-3">Overall Feedback</div>
                <div className="flex flex-col space-y-4">
                  <div className="flex justify-between items-center bg-green-50 p-3 rounded-xl border border-green-100">
                    <span className="text-green-700 font-bold text-sm">Positive (4-5★)</span>
                    <span className="text-green-800 font-black">{analysis.pct_positive?.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between items-center bg-red-50 p-3 rounded-xl border border-red-100">
                    <span className="text-red-700 font-bold text-sm">Negative (1-2★)</span>
                    <span className="text-red-800 font-black">{analysis.pct_negative?.toFixed(1)}%</span>
                  </div>
                </div>
              </div>
              <div className="col-span-2">
                <div className="text-sm font-semibold text-slate-500 uppercase mb-4">Aspect Sentiments</div>
                <div className="space-y-5">
                  {Object.entries(analysis.aspect_scores || {}).map(([aspect, score]) => (
                    <div key={aspect}>
                      <div className="flex justify-between text-xs font-bold text-slate-700 mb-1.5 capitalize">
                        <span>{aspect}</span>
                        <span className={score > 0.1 ? 'text-green-600' : score < -0.1 ? 'text-red-600' : 'text-slate-500'}>
                          {score > 0.1 ? 'Positive' : score < -0.1 ? 'Negative' : 'Neutral'}
                        </span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden flex relative">
                        <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-200 z-10"></div>
                        {score > 0 ? (
                          <div className="h-3 bg-green-500 absolute left-1/2 transition-all duration-1000" style={{ width: `${score * 50}%` }}></div>
                        ) : (
                          <div className="h-3 bg-red-500 absolute right-1/2 transition-all duration-1000" style={{ width: `${Math.abs(score) * 50}%` }}></div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Reviews List */}
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-slate-800">Customer Reviews</h2>
              <div className="flex space-x-3">
                <select
                  value={filterRating}
                  onChange={(e) => setFilterRating(Number(e.target.value))}
                  className="bg-white border border-slate-200 text-slate-700 text-sm rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
                >
                  <option value={0}>All Ratings</option>
                  <option value={5}>5 Stars</option>
                  <option value={4}>4 Stars</option>
                  <option value={3}>3 Stars</option>
                  <option value={2}>2 Stars</option>
                  <option value={1}>1 Star</option>
                </select>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="bg-white border border-slate-200 text-slate-700 text-sm rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
                >
                  <option value="newest">Newest</option>
                  <option value="oldest">Oldest</option>
                  <option value="highest">Highest</option>
                  <option value="lowest">Lowest</option>
                </select>
              </div>
            </div>
            {reviews.length === 0 ? (
              <p className="text-slate-500 bg-white p-6 rounded-2xl border border-slate-100">No reviews yet. Be the first!</p>
            ) : (
              <div className="space-y-4">
                {reviews.map(review => (
                  <div
                    key={review.id}
                    onClick={() => handleReviewClick(review)}
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

                {totalPages > 1 && (
                  <div className="flex justify-between items-center mt-6 pt-4 border-t border-slate-100">
                    <button
                      disabled={page === 1}
                      onClick={() => setPage(p => Math.max(1, p - 1))}
                      className="px-4 py-2 bg-white border border-slate-200 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 transition-colors text-sm font-semibold text-slate-700 shadow-sm"
                    >
                      Previous
                    </button>
                    <span className="text-sm font-semibold text-slate-500">
                      Page {page} of {totalPages}
                    </span>
                    <button
                      disabled={page === totalPages}
                      onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                      className="px-4 py-2 bg-white border border-slate-200 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 transition-colors text-sm font-semibold text-slate-700 shadow-sm"
                    >
                      Next
                    </button>
                  </div>
                )}
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

              {selectedReview.analysis ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 rounded-xl bg-[#fdfdfd] border border-slate-100">
                    <span className="text-xs font-semibold text-slate-500 uppercase">Sentiment</span>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${selectedReview.analysis.sentiment === 'Positive' ? 'bg-green-50 text-green-700' :
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
              ) : (
                <div className="p-6 bg-slate-50 rounded-xl text-center border border-slate-100">
                  {analyzingReview ? (
                    <>
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto mb-3"></div>
                      <p className="text-slate-500 text-sm font-semibold animate-pulse">Running live AI analysis...</p>
                    </>
                  ) : (
                    <>
                      <BrainCircuit className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                      <p className="text-slate-500 text-sm font-semibold">AI Analysis pending for this review.</p>
                    </>
                  )}
                </div>
              )}
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

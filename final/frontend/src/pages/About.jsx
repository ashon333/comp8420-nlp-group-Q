import React from 'react';
import Navbar from '../components/Navbar';
import { Shield, Award, Users, GitBranch } from 'lucide-react';

export default function About() {
  const members = [
    { name: 'Alex Carter', role: 'Project Lead & NLP Research', avatar: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&q=80' },
    { name: 'Sarah Jenkins', role: 'Full Stack Engineer', avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&q=80' },
    { name: 'Michael Zhao', role: 'ML Engineer & Search Specialist', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&q=80' },
    { name: 'Elena Rostova', role: 'UI/UX Designer', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&q=80' },
    { name: 'David Vance', role: 'Database Architect', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&q=80' },
  ];

  return (
    <div className="min-h-screen bg-[#fffcf9] font-sans pb-16">
      <Navbar />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-12">
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center bg-orange-100 p-3.5 rounded-3xl text-orange-600 mb-4 shadow-sm">
            <Users className="w-8 h-8" />
          </div>
          <h1 className="text-4xl font-extrabold text-slate-800 tracking-tight mb-4">About the Project</h1>
          <p className="text-slate-500 font-semibold text-sm uppercase tracking-wider bg-orange-50 px-4 py-1.5 rounded-full inline-block">
            Made by Group Q
          </p>
        </div>

        {/* Project Description */}
        <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm mb-12 relative overflow-hidden">
          <div className="absolute right-0 top-0 w-32 h-32 bg-orange-500/5 rounded-full -mr-12 -mt-12"></div>
          <h2 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-orange-500" /> COMP8420 - Natural Language Processing
          </h2>
          <p className="text-slate-500 leading-relaxed text-sm">
            This advanced Product Portal is a demonstration of modern natural language processing and semantic understanding techniques. By integrating semantic query logic, user sentiment parsing, AI writing detection, and visual similarity analysis, our team has built a highly premium interface that illustrates how artificial intelligence enhances contemporary e-commerce experiences.
          </p>
        </div>

        {/* Member Grid */}
        <div>
          <h2 className="text-2xl font-bold text-slate-800 mb-8 flex items-center gap-2">
            <Award className="w-6 h-6 text-orange-500" /> Meet Group Q
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {members.map((member) => (
              <div key={member.name} className="bg-white rounded-3xl p-6 border border-slate-100 shadow-sm flex flex-col items-center text-center hover:shadow-lg transition-shadow duration-300">
                <img
                  src={member.avatar}
                  alt={member.name}
                  className="w-20 h-20 rounded-2xl object-cover mb-4 shadow-inner ring-4 ring-orange-50"
                />
                <h3 className="font-bold text-slate-800 mb-1 text-base">{member.name}</h3>
                <p className="text-slate-400 text-xs font-medium mb-4">{member.role}</p>
                <div className="mt-auto pt-2 border-t border-slate-50 w-full flex justify-center">
                  <button className="text-slate-400 hover:text-slate-600 transition-colors">
                    <GitBranch className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

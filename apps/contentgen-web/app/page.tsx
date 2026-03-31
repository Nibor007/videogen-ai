'use client';
import { useState, useEffect, useCallback } from 'react';
import { getJobs, Job } from '@/lib/api';
import GenerateForm from '@/components/GenerateForm';
import JobCard from '@/components/JobCard';

export default function Home() {
  const [jobs,    setJobs]    = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchJobs = useCallback(async () => {
    try {
      const data = await getJobs();
      setJobs(data);
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, [fetchJobs]);

  const handleJobCreated = (job: Job) => {
    setJobs(prev => [job, ...prev]);
  };

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <div className="max-w-4xl mx-auto px-4 py-10">

        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-white mb-1">ContentGen AI</h1>
          <p className="text-sm text-zinc-500">Generate images, audio and video with Amazon Bedrock</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <GenerateForm onJobCreated={handleJobCreated} />
          </div>

          <div className="lg:col-span-2">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-medium text-zinc-400">
                Recent jobs {jobs.length > 0 && `(${jobs.length})`}
              </h2>
              <button
                onClick={fetchJobs}
                className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
              >
                Refresh
              </button>
            </div>

            {loading ? (
              <div className="space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 animate-pulse">
                    <div className="h-4 bg-zinc-800 rounded w-1/3 mb-3"/>
                    <div className="h-3 bg-zinc-800 rounded w-2/3"/>
                  </div>
                ))}
              </div>
            ) : jobs.length === 0 ? (
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-8 text-center">
                <p className="text-zinc-500 text-sm">No jobs yet. Create your first one.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {jobs.map(job => <JobCard key={job._id} job={job} />)}
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
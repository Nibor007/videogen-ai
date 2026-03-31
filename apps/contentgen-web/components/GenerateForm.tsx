'use client';
import { useState } from 'react';
import { createJob, Job, JobType } from '@/lib/api';

const STYLES = ['photorealistic', 'cinematic', 'illustration', 'anime'];
const SIZES  = ['1024x1024', '1152x768', '768x1152'];

export default function GenerateForm({ onJobCreated }: { onJobCreated: (job: Job) => void }) {
  const [prompt,  setPrompt]  = useState('');
  const [type,    setType]    = useState<JobType>('image');
  const [style,   setStyle]   = useState('photorealistic');
  const [size,    setSize]    = useState('1024x1024');
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setError('');

    try {
      const job = await createJob(type, prompt, { style, size });
      onJobCreated(job);
      setPrompt('');
    } catch (err) {
      setError('Failed to create job. Check API connection.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-4">
      <div>
        <label className="text-xs text-zinc-400 mb-1.5 block">Content type</label>
        <div className="flex gap-2">
          {(['image', 'audio', 'video'] as JobType[]).map(t => (
            <button
              key={t}
              type="button"
              onClick={() => setType(t)}
              className={`px-3 py-1.5 rounded-lg text-sm border transition-colors ${
                type === t
                  ? 'bg-violet-600 border-violet-500 text-white'
                  : 'bg-zinc-800 border-zinc-700 text-zinc-400 hover:border-zinc-600'
              }`}
            >
              {t === 'image' ? '🖼 Image' : t === 'audio' ? '🎵 Audio' : '🎬 Video'}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="text-xs text-zinc-400 mb-1.5 block">Prompt</label>
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          placeholder="A futuristic city at sunset, neon lights reflecting on wet streets..."
          rows={3}
          className="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-sm text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-violet-500 resize-none"
        />
      </div>

      {type === 'image' && (
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-zinc-400 mb-1.5 block">Style</label>
            <select
              value={style}
              onChange={e => setStyle(e.target.value)}
              className="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-sm text-zinc-200 focus:outline-none focus:border-violet-500"
            >
              {STYLES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="text-xs text-zinc-400 mb-1.5 block">Size</label>
            <select
              value={size}
              onChange={e => setSize(e.target.value)}
              className="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-sm text-zinc-200 focus:outline-none focus:border-violet-500"
            >
              {SIZES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>
      )}

      {error && (
        <p className="text-xs text-red-400 bg-red-500/10 rounded-lg p-2">{error}</p>
      )}

      <button
        type="submit"
        disabled={loading || !prompt.trim()}
        className="w-full py-2.5 bg-violet-600 hover:bg-violet-500 disabled:bg-zinc-700 disabled:text-zinc-500 text-white text-sm font-medium rounded-lg transition-colors"
      >
        {loading ? 'Creating job...' : 'Generate'}
      </button>
    </form>
  );
}
'use client';
import { Job } from '@/lib/api';

const STATUS_STYLES: Record<string, string> = {
  pending:    'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  processing: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  completed:  'bg-green-500/20 text-green-400 border-green-500/30',
  failed:     'bg-red-500/20 text-red-400 border-red-500/30',
};

const TYPE_ICON: Record<string, string> = {
  image: '🖼',
  audio: '🎵',
  video: '🎬',
};

export default function JobCard({ job }: { job: Job }) {
  const timeAgo = (date: string) => {
    const seconds = Math.floor((Date.now() - new Date(date).getTime()) / 1000);
    if (seconds < 60)  return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    return `${Math.floor(seconds / 3600)}h ago`;
  };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 hover:border-zinc-700 transition-colors">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-2">
          <span className="text-lg">{TYPE_ICON[job.type]}</span>
          <span className={`text-xs px-2 py-0.5 rounded-full border ${STATUS_STYLES[job.status]}`}>
            {job.status}
          </span>
        </div>
        <span className="text-xs text-zinc-500">{timeAgo(job.createdAt)}</span>
      </div>

      <p className="text-sm text-zinc-300 mb-3 line-clamp-2">{job.prompt}</p>

      {job.results.length > 0 && (
        <div className="grid grid-cols-2 gap-2 mt-3">
          {job.results.map((url, i) => (
            <img
              key={i}
              src={url}
              alt={`Result ${i + 1}`}
              className="w-full rounded-lg object-cover aspect-square"
            />
          ))}
        </div>
      )}

      {job.status === 'failed' && job.error && (
        <p className="text-xs text-red-400 mt-2 bg-red-500/10 rounded-lg p-2">
          {job.error}
        </p>
      )}

      {job.status === 'pending' && (
        <div className="mt-3 flex items-center gap-2 text-xs text-zinc-500">
          <div className="w-1.5 h-1.5 rounded-full bg-yellow-500 animate-pulse"/>
          Waiting in queue...
        </div>
      )}
    </div>
  );
}
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://videogen-alb-1738263676.us-east-1.elb.amazonaws.com';

export type JobType = 'image' | 'audio' | 'video';
export type JobStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface Job {
  _id:       string;
  type:      JobType;
  status:    JobStatus;
  prompt:    string;
  params:    Record<string, any>;
  results:   string[];
  error?:    string;
  createdAt: string;
  updatedAt: string;
}

export async function createJob(
  type: JobType,
  prompt: string,
  params: Record<string, any> = {}
): Promise<Job> {
  const res = await fetch(`${API_BASE}/jobs`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ type, prompt, params }),
  });
  if (!res.ok) throw new Error('Failed to create job');
  return res.json();
}

export async function getJob(id: string): Promise<Job> {
  const res = await fetch(`${API_BASE}/jobs/${id}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch job');
  return res.json();
}

export async function getJobs(): Promise<Job[]> {
  const res = await fetch(`${API_BASE}/jobs`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch jobs');
  return res.json();
}
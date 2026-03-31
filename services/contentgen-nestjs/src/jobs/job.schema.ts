import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type JobDocument = Job & Document;

export enum JobStatus {
  PENDING    = 'pending',
  PROCESSING = 'processing',
  COMPLETED  = 'completed',
  FAILED     = 'failed',
}

export enum JobType {
  IMAGE = 'image',
  AUDIO = 'audio',
  VIDEO = 'video',
}

@Schema({ timestamps: true })
export class Job {
  @Prop({ required: true, enum: JobType })
  type: JobType;

  @Prop({ required: true, enum: JobStatus, default: JobStatus.PENDING })
  status: JobStatus;

  @Prop({ required: true })
  prompt: string;

  @Prop({ type: Object, default: {} })
  params: Record<string, any>;

  @Prop({ type: [String], default: [] })
  results: string[];

  @Prop()
  error?: string;

  @Prop()
  completedAt?: Date;
}

export const JobSchema = SchemaFactory.createForClass(Job);
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';
import { Job, JobDocument, JobStatus } from './job.schema';
import { CreateJobDto } from './dto/create-job.dto';

@Injectable()
export class JobsService {
  private sqs: SQSClient;
  private queueUrl: string;

  constructor(@InjectModel(Job.name) private jobModel: Model<JobDocument>) {
    this.sqs = new SQSClient({ region: process.env.AWS_REGION || 'us-east-1' });
    this.queueUrl = process.env.SQS_QUEUE_URL;
  }

  async create(dto: CreateJobDto): Promise<JobDocument> {
    const job = new this.jobModel({
      type:   dto.type,
      prompt: dto.prompt,
      params: dto.params || {},
      status: JobStatus.PENDING,
    });
    await job.save();

    await this.sqs.send(new SendMessageCommand({
      QueueUrl:    this.queueUrl,
      MessageBody: JSON.stringify({
        jobId:  job._id.toString(),
        type:   job.type,
        prompt: job.prompt,
        params: job.params,
      }),
    }));

    return job;
  }

  async findOne(id: string): Promise<JobDocument> {
    const job = await this.jobModel.findById(id).exec();
    if (!job) throw new NotFoundException(`Job ${id} not found`);
    return job;
  }

  async findAll(limit = 20): Promise<JobDocument[]> {
    return this.jobModel.find().sort({ createdAt: -1 }).limit(limit).exec();
  }

  async updateStatus(
    id: string,
    status: JobStatus,
    results?: string[],
    error?: string,
  ): Promise<JobDocument> {
    const update: any = { status };
    if (results) update.results = results;
    if (error)   update.error   = error;
    if (status === JobStatus.COMPLETED || status === JobStatus.FAILED) {
      update.completedAt = new Date();
    }
    return this.jobModel.findByIdAndUpdate(id, update, { new: true }).exec();
  }
}
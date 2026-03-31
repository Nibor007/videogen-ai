import { IsString, IsEnum, IsOptional, IsObject, MinLength } from 'class-validator';
import { JobType } from '../job.schema';

export class CreateJobDto {
  @IsEnum(JobType)
  type: JobType;

  @IsString()
  @MinLength(3)
  prompt: string;

  @IsOptional()
  @IsObject()
  params?: Record<string, any>;
}
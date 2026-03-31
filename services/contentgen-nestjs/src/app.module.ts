import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { MongooseModule } from '@nestjs/mongoose';
import { JobsModule } from './jobs/jobs.module';

@Module({
  imports: [...],
  controllers: [AppController],
})
export class AppModule {}
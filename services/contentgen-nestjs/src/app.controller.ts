import { Controller, Get } from '@nestjs/common';

@Controller()
export class AppController {
  @Get('health')
  health() {
    return {
      status:  'ok',
      service: 'contentgen-nestjs',
      version: '0.1.0',
    };
  }
}
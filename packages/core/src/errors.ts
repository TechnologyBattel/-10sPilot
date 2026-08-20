export class AppError extends Error {
  constructor(
    message: string,
    readonly code: string = 'app_error',
    readonly status: number = 500,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'not_found', 404);
    this.name = 'NotFoundError';
  }
}

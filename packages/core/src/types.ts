export type Id = string;

export type Timestamps = {
  createdAt: string;
  updatedAt: string;
};

export type PilotStatus = 'draft' | 'running' | 'completed' | 'failed';

export type Pilot = Timestamps & {
  id: Id;
  name: string;
  prompt: string;
  status: PilotStatus;
};

export type Run = Timestamps & {
  id: Id;
  pilotId: Id;
  status: PilotStatus;
  output: string | null;
};

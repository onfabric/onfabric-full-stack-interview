export type User = {
    id: string;
    email: string;
    fullname?: string;
    nickname?: string;
    created_at: string;
    updated_at: string;
  };

export type ApiKey = {
    id: string;
    user_id: string;
    key: string;
    name: string;
    last_used_at?: string;
    created_at: string;
    updated_at: string;
  };


export type UserRequest = {
    id: string;
    key_id: string;
    endpoint: string;
    method: string;
    status_code: number;
    created_at: string;
    updated_at: string;
  };

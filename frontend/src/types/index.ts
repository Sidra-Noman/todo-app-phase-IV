export interface User {
  id: string;
  email: string;
  createdAt: string;
}

export interface Todo {
  id: string;
  title: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  message: string;
  user?: {
    id: string;
    email: string;
  };
}

export interface TodoListResponse {
  todos: Todo[];
  total: number;
}

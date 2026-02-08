'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch } from '@/services/api';
import { Todo } from '@/types';
import { LogOut, Trash2, CheckCircle, Circle, Plus, Edit2, X, Check } from 'lucide-react';
import { useSession } from 'next-auth/react';

export default function TodosPage() {
  const router = useRouter();
  const { data: session, status } = useSession();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [appLoading, setAppLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');

  const fetchTodos = async () => {
    try {
      const data = await apiFetch('/todos/');
      setTodos(data.todos);
    } catch (err: any) {
      // Only redirect to signin if it's an authentication error
      if (err.message.includes('401') || err.message.toLowerCase().includes('unauthorized') || err.message.toLowerCase().includes('not authenticated')) {
        router.push('/signin');
      } else {
        console.error('Error fetching todos:', err);
      }
    } finally {
      setAppLoading(false);
    }
  };

  useEffect(() => {
    // Check if user is authenticated before loading todos
    if (status !== 'loading') {
      if (!session) {
        router.push('/signin');
      } else {
        fetchTodos();
      }
    }
  }, [session, status]);

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    setSubmitting(true);
    try {
      const data = await apiFetch('/todos/', {
        method: 'POST',
        body: JSON.stringify({ title: newTitle }),
      });
      if (data && data.todo) {
        setTodos([data.todo, ...todos]);
        setNewTitle('');
      } else {
        console.error('Unexpected response format during todo addition', data);
        fetchTodos();
      }
    } catch (err) {
      alert('Failed to add todo');
    } finally {
      setSubmitting(false);
    }
  };

  const handleToggle = async (id: string) => {
    // Optimistic update
    setTodos(todos.map(t => t.id === id ? { ...t, is_complete: !t.is_complete } : t));
    try {
      await apiFetch(`/todos/${id}/toggle`, { method: 'POST' });
    } catch (err) {
      fetchTodos(); // Revert on failure
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this todo?')) return;
    setTodos(todos.filter(t => t.id !== id));
    try {
      await apiFetch(`/todos/${id}`, { method: 'DELETE' });
    } catch (err) {
      fetchTodos();
    }
  };

  const startEdit = (todo: Todo) => {
    setEditingId(todo.id);
    setEditTitle(todo.title);
  };

  const handleUpdate = async (id: string) => {
    if (!editTitle.trim()) return;
    setTodos(todos.map(t => t.id === id ? { ...t, title: editTitle } : t));
    setEditingId(null);
    try {
      await apiFetch(`/todos/${id}`, {
        method: 'PATCH',
        body: JSON.stringify({ title: editTitle }),
      });
    } catch (err) {
      fetchTodos();
    }
  };

  const handleSignout = async () => {
    try {
      // Use NextAuth's signOut function which handles both backend and frontend state
      await import('next-auth/react').then(({ signOut }) => signOut({ redirect: false }));
      // Also call our backend signout to ensure session cookie is cleared
      await apiFetch('/auth/signout', { method: 'POST' });
      router.push('/signin');
    } catch (err) {
      router.push('/signin');
    }
  };

  if (appLoading || status === 'loading') return <div className="flex h-screen items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 pb-12">
      <nav className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 justify-between items-center">
            <div className="flex space-x-4">
              <h1 className="text-xl font-bold text-gray-900 self-center">My Todos</h1>
              <a
                href="/chat"
                className="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
              >
                💬 AI Assistant
              </a>
            </div>
            <button
              onClick={handleSignout}
              className="inline-flex items-center gap-2 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
            >
              <LogOut size={16} /> Sign out
            </button>
          </div>
        </div>
      </nav>

      <main className="mx-auto max-w-2xl px-4 pt-10 sm:px-6">
        <form onSubmit={handleAddTodo} className="mb-8 flex gap-2">
          <input
            type="text"
            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            placeholder="What needs to be done?"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            disabled={submitting}
          />
          <button
            type="submit"
            disabled={submitting || !newTitle.trim()}
            className="flex items-center justify-center rounded-md bg-indigo-600 px-3 py-2 text-white shadow-sm hover:bg-indigo-500 disabled:opacity-50"
          >
            <Plus size={20} />
          </button>
        </form>

        <div className="space-y-3">
          {todos.length === 0 ? (
            <p className="text-center text-gray-500 py-10">No todos yet. Add one above!</p>
          ) : (
            todos.map((todo) => (
              <div
                key={todo.id}
                className="flex items-center justify-between rounded-lg bg-white p-4 shadow-sm ring-1 ring-gray-200"
              >
                <div className="flex flex-1 items-center gap-3">
                  <button
                    onClick={() => handleToggle(todo.id)}
                    className={`flex-shrink-0 ${todo.is_complete ? 'text-green-500' : 'text-gray-400 hover:text-gray-600'}`}
                  >
                    {todo.is_complete ? <CheckCircle size={24} /> : <Circle size={24} />}
                  </button>

                  {editingId === todo.id ? (
                    <div className="flex flex-1 gap-2">
                      <input
                        autoFocus
                        type="text"
                        className="block w-full rounded-md border-0 py-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') handleUpdate(todo.id);
                          if (e.key === 'Escape') setEditingId(null);
                        }}
                      />
                      <button onClick={() => handleUpdate(todo.id)} className="text-green-600"><Check size={20} /></button>
                      <button onClick={() => setEditingId(null)} className="text-red-600"><X size={20} /></button>
                    </div>
                  ) : (
                    <span className={`flex-1 text-gray-900 ${todo.is_complete ? 'line-through text-gray-400' : ''}`}>
                      {todo.title}
                    </span>
                  )}
                </div>

                <div className="flex gap-1 ml-4">
                  <button
                    onClick={() => startEdit(todo)}
                    className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
                  >
                    <Edit2 size={18} />
                  </button>
                  <button
                    onClick={() => handleDelete(todo.id)}
                    className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-red-600"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
}

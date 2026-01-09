import React from 'react';
import { Button } from './Button';

interface ErrorStateProps {
  title: string;
  message?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export const ErrorState: React.FC<ErrorStateProps> = ({ title, message, action }) => {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12 px-6 text-center rounded-lg bg-error-50 border border-error-200">
      <div className="text-4xl">⚠️</div>
      <h3 className="text-h3 font-semibold text-error-600">{title}</h3>
      {message && <p className="text-body text-gray-700 max-w-md">{message}</p>}
      {action && (
        <Button onClick={action.onClick} variant="danger">
          {action.label}
        </Button>
      )}
    </div>
  );
};

ErrorState.displayName = 'ErrorState';

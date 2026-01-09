import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className, id, ...props }, ref) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

    const baseStyles =
      'w-full px-3 py-2 border rounded-lg text-body transition-smooth focus:ring-2 focus:ring-primary-500 focus:ring-offset-0 focus:border-primary-500';

    const borderStyles = error ? 'border-error-600 focus:ring-error-600' : 'border-gray-300 focus:ring-primary-600';

    const combinedClassName = `${baseStyles} ${borderStyles} ${className || ''}`;

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="block text-body-sm font-medium text-primary mb-1.5">
            {label}
          </label>
        )}
        <input ref={ref} id={inputId} className={combinedClassName} {...props} />
        {error && <p className="text-error-600 text-caption mt-1">{error}</p>}
        {helperText && !error && <p className="text-tertiary text-caption mt-1">{helperText}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';

import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ children, className, ...props }) => {
  const baseStyles = 'bg-white border border-gray-200 rounded-lg shadow-professional-sm p-6';

  return (
    <div className={`${baseStyles} ${className || ''}`} {...props}>
      {children}
    </div>
  );
};

Card.displayName = 'Card';

import React from 'react';
import Link from 'next/link';

interface HeaderProps {
  title: string;
  showLogo?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ title, showLogo = true }) => {
  return (
    <header className="bg-white border-b border-gray-200 shadow-professional-sm">
      <div className="container-content py-4 flex items-center justify-between">
        {showLogo && (
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-h3">✓</span>
            </div>
            <span className="text-h3 font-bold text-primary hidden sm:inline">Todo App</span>
          </Link>
        )}
        <h1 className="text-h2 font-bold text-primary flex-1 sm:flex-none sm:text-center mx-auto">{title}</h1>
        <div className="w-8" />
      </div>
    </header>
  );
};

Header.displayName = 'Header';

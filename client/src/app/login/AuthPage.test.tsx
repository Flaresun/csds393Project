import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import AuthPage from './page';

jest.mock('../../components/Hero.css', () => ({}), { virtual: true });

const mockPush = jest.fn();

jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush
  }),
}));

const mockContextValue = {
  setUserEmail: jest.fn()
};


jest.mock('react', () => {
  const originalReact = jest.requireActual('react');
  return {
    ...originalReact,
    useContext: () => mockContextValue
  };
});

global.fetch = jest.fn().mockImplementation(() => 
  Promise.resolve({
    json: () => Promise.resolve({ 
      success: true, 
      user: { email: 'test@gmail.com' } 
    })
  })
);

describe('AuthPage Navigation', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    render(<AuthPage />);
  });

  test('should navigate to dashboard after successful login', async () => {

    fireEvent.click(screen.getByText('Login', { selector: 'span' }));
    
    fireEvent.change(screen.getByPlaceholderText('Enter your email'), {
      target: { value: 'test@gmail.com' },
    });
    
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), {
      target: { value: 'test' },
    });
    
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/dashboard');
    });
  });

  test('should navigate to dashboard after successful signup', async () => {

    fireEvent.change(screen.getByPlaceholderText('Enter your email'), {
      target: { value: 'test@gmail.com' },
    });
    
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), {
      target: { value: 'test' },
    });
    
    fireEvent.click(screen.getByRole('button', { name: 'Sign Up' }));
    
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/dashboard');
    });
  });
});
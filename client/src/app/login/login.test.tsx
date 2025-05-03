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

// Mocking `useContext` to return the mock context value
jest.mock('react', () => {
  const originalReact = jest.requireActual('react');
  return {
    ...originalReact,
    useContext: () => mockContextValue
  };
});

// Mocking the `fetch` API to simulate successful login and signup responses
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
    // Simulate user interaction for login
    fireEvent.click(screen.getByText('Login', { selector: 'span' }));  // Switch to login form
    
    fireEvent.change(screen.getByPlaceholderText('Enter your email'), {
      target: { value: 'test@gmail.com' },
    });
    
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), {
      target: { value: 'test' },
    });
    
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));  // Click login button
    
    // Assert that the navigation occurs after successful login
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/dashboard');
    });
  });

  test('should navigate to dashboard after successful signup', async () => {
    // Simulate user interaction for signup
    fireEvent.change(screen.getByPlaceholderText('Enter your email'), {
      target: { value: 'test@gmail.com' },
    });
    
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), {
      target: { value: 'test' },
    });
    
    fireEvent.click(screen.getByRole('button', { name: 'Sign Up' }));  // Click sign-up button
    
    // Assert that the navigation occurs after successful signup
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/dashboard');
    });
  });
});

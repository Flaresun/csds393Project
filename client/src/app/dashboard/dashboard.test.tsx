import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import LeftPanel from './components/LeftPanel'; 
import { AppContent } from "../../context/AppContext";

const mockPush = jest.fn();
 
 jest.mock('next/navigation', () => ({
   useRouter: () => ({
     push: mockPush  
   }),
 }));

const mockContextValues = {
  panel: true,
  setPanel: jest.fn(),
  userEmail: 'test@example.com',
  setUserEmail: jest.fn(),
  isAuth: true,
  setIsAuth: jest.fn(),
  userRole: 'faculty',
  setUserRole: jest.fn()
};

describe('LeftPanel Component', () => {
  
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    render(
        <AppContent.Provider value={mockContextValues}>
          <LeftPanel panel={true} />
        </AppContent.Provider>
      );
  });

  test('should navigate to home page when Home is clicked', () => {
    fireEvent.click(screen.getByText('Home'));
    expect(mockPush).toHaveBeenCalledWith('dashboard');
  });

  test('should navigate to upload page when Upload Notes is clicked', () => {
    fireEvent.click(screen.getByText('Upload Notes'));
    expect(mockPush).toHaveBeenCalledWith('upload');
  });

  test('should navigate to search page when Search Files is clicked', () => {
    fireEvent.click(screen.getByText('Search Files'));
    expect(mockPush).toHaveBeenCalledWith('search');
  });

  test('should navigate to saved page when Saved Notes is clicked', () => {
    fireEvent.click(screen.getByText('Saved Notes'));
    expect(mockPush).toHaveBeenCalledWith('saved');
  });

  test('should navigate to settings page when Settings is clicked', () => {
    fireEvent.click(screen.getByText('Settings'));
    expect(mockPush).toHaveBeenCalledWith('settings');
  });

  test('should navigate to create page when Create is clicked', () => {
    fireEvent.click(screen.getByText('Create'));
    expect(mockPush).toHaveBeenCalledWith('create');
  });
  
});
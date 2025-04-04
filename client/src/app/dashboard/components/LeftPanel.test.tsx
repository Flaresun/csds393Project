import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import LeftPanel from './LeftPanel';

const mockPush = jest.fn();

jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush  
  }),
}));

describe('LeftPanel Navigation', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    render(<LeftPanel panel={true} />);
  });

  test('should navigate to home page when Home is clicked', () => {
    fireEvent.click(screen.getByText('Home'));
    expect(mockPush).toHaveBeenCalledWith('home');
  });

  test('should navigate to upload page when Upload Notes is clicked', () => {
    fireEvent.click(screen.getByText('Upload Notes'));
    expect(mockPush).toHaveBeenCalledWith('upload');
  });

  test('should navigate to search page when Search Files is clicked', () => {
    fireEvent.click(screen.getByText('Search Files'));
    expect(mockPush).toHaveBeenCalledWith('search');
  });
});
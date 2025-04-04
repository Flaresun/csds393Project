import React from 'react';
import { render, screen, fireEvent, waitFor} from '@testing-library/react';
import '@testing-library/jest-dom';
import FileSearch from './FileSearch';

jest.mock('./FileSearch.css', () => ({}), { virtual: true });

// Mock fetch
global.fetch = jest.fn();

// Mock console.log
console.log = jest.fn();

describe('FileSearch Component - Simple Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Set default mocks
    Object.defineProperty(window, 'location', {
      value: { search: '' },
      writable: true
    });
    
    Object.defineProperty(document, 'cookie', {
      value: 'access_token=test-token',
      writable: true
    });
  });

  it('updates input value when typing in search field', () => {
    render(<FileSearch />);
    
    const searchInput = screen.getByPlaceholderText('Search File');
    fireEvent.change(searchInput, { target: { value: 'Physics 101' } });
    
    expect(searchInput).toHaveValue('Physics 101');
  });

  it('calls getFiles when search button is clicked', async () => {

    (global.fetch as jest.Mock).mockResolvedValue({
      json: async () => ({ success: true, message: [] })
    });

    await waitFor(() => {
        render(<FileSearch />);
    });


    (global.fetch as jest.Mock).mockClear();

    const searchInput = screen.getByPlaceholderText('Search File');
    fireEvent.change(searchInput, { target: { value: 'Physics 101' } });
    
    fireEvent.click(screen.getByRole('button', { name: /search/i }));

    expect(global.fetch).toHaveBeenCalled();
  });

});
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import FileSearch from './components/FileSearch';
import { AppContent } from '../../context/AppContext';

// Mock CSS import
jest.mock('./components/FileSearch.css', () => ({}));

// Mock fetch API
global.fetch = jest.fn(() => 
  Promise.resolve({
    json: () => Promise.resolve({ allData: [] })
  })
) as jest.Mock;

// Create simple mock context
const mockContext = { userRole: 'student' };

describe('FileSearch Component', () => {
  beforeEach(() => {
    // Set up document cookie for token
    Object.defineProperty(document, 'cookie', {
      value: 'token=test-token',
      writable: true
    });
  });

  /**
   * Renders the FileSearch component wrapped in the AppContext.Provider
   * with mockContext provided as the context value.
   */
  const renderComponent = () => {
    return render(
      <AppContent.Provider value={mockContext}>
        <FileSearch />
      </AppContent.Provider>
    );
  };

  it('renders search input and button', () => {
    renderComponent();
    
    // Asserts that the search input and button are rendered
    expect(screen.getByPlaceholderText('Search File')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument();
  });

  it('updates input value when typing', () => {
    renderComponent();
    
    const input = screen.getByPlaceholderText('Search File');
    fireEvent.change(input, { target: { value: 'Math' } });
    
    // Asserts that the input value has been updated
    expect(input).toHaveValue('Math');
  });

  it('calls search API when button is clicked', () => {
    renderComponent();
    
    const input = screen.getByPlaceholderText('Search File');
    fireEvent.change(input, { target: { value: 'Physics' } });
    
    const searchButton = screen.getByRole('button', { name: /search/i });
    fireEvent.click(searchButton);
    
    // Asserts that the fetch function has been called when the search button is clicked
    expect(global.fetch).toHaveBeenCalled();
  });
});

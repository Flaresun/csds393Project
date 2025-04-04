import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Page from './uploader';
import axios from 'axios';

jest.mock('./uploader.css', () => ({}), { virtual: true });

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock document.cookie
Object.defineProperty(document, 'cookie', {
  writable: true,
  value: 'access_token=test-token',
});

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
  
describe('FileUploader Component - Basic Functionality', () => {
    test('handles file selection', () => {
        // Render component
        render(<Page />);
        
        // Get all inputs and find the file input
        const inputs = document.querySelectorAll('input');
        const fileInput = Array.from(inputs).find(input => input.type === 'file');
        
        // Create a test file and trigger change event
        const testFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
        fireEvent.change(fileInput, { target: { files: [testFile] } });
        
        // Verify the component still renders properly after file selection
        expect(screen.getByText('Upload a File')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /upload/i })).toBeInTheDocument();
      });

    test('updates input value when typing in search field', () => {
        render(<Page />);
        
        const classInput = screen.getByPlaceholderText('Enter class name');
        fireEvent.change(classInput, { target: { value: 'Physics 121' } });
        
        expect(classInput).toHaveValue('Physics 121');
    });
  
    test('upload button triggers file upload', () => {

    // Mock axios post to return a resolved promise
    mockedAxios.post.mockResolvedValue({ data: { file_id: 'test-file-id' } });
    
    // Render component
    render(
        <Page />
    );
    
    // Select a file
    const fileInput = document.querySelector('input[type="file"]');
    const testFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    if (fileInput) {
      fireEvent.change(fileInput, { target: { files: [testFile] } });
    }
    
    // Click upload button
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    fireEvent.click(uploadButton);
    
    // Check if axios.post was called
    expect(mockedAxios.post).toHaveBeenCalled();
    
    // That's it - if axios.post was called, we assume the upload functionality works
  });
});
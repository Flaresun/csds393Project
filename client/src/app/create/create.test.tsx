import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import CourseManager from './components/CreateNotes';

// Mock global fetch API
global.fetch = jest.fn();

// Mock document.cookie
Object.defineProperty(document, 'cookie', {
  writable: true,
  value: 'token=test-token',
});

describe('Course Creation Component', () => {
  // Clear mocks before each test
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock successful API response for fetch
    (global.fetch as jest.Mock).mockResolvedValue({
      json: () => Promise.resolve({ success: true }),
    });
  });

  // Test handling of course form input changes
  test('handles course form input changes', () => {
    render(<CourseManager />);
    
    // Get input elements for course details
    const deptCodeInput = screen.getAllByPlaceholderText('Department Code')[0];
    const courseCodeInput = screen.getAllByPlaceholderText('Course Code')[0];
    const courseNameInput = screen.getByPlaceholderText('Course Name');
    
    // Simulate input changes
    fireEvent.change(deptCodeInput, { target: { value: 'CSDS' } });
    fireEvent.change(courseCodeInput, { target: { value: '132' } });
    fireEvent.change(courseNameInput, { target: { value: 'Programming in Java' } });
    
    // Assert that inputs have the correct values
    expect(deptCodeInput).toHaveValue('CSDS');
    expect(courseCodeInput).toHaveValue('132');
    expect(courseNameInput).toHaveValue('Programming in Java');
  });

  // Test handling of section form input changes
  test('handles section form input changes', () => {
    render(<CourseManager />);
    
    // Get input elements for section details
    const deptCodeInput = screen.getAllByPlaceholderText('Department Code')[1];
    const courseCodeInput = screen.getAllByPlaceholderText('Course Code')[1];
    const instructorEmailInput = screen.getByPlaceholderText('Instructor Email');
    const yearInput = screen.getByPlaceholderText('Year');
    const semesterSelect = screen.getByRole('combobox');
    
    // Simulate input changes
    fireEvent.change(deptCodeInput, { target: { value: 'CS' } });
    fireEvent.change(courseCodeInput, { target: { value: '101' } });
    fireEvent.change(instructorEmailInput, { target: { value: 'instructor@example.com' } });
    fireEvent.change(yearInput, { target: { value: '2025' } });
    fireEvent.change(semesterSelect, { target: { value: 'Fall' } });
    
    // Assert that inputs have the correct values
    expect(deptCodeInput).toHaveValue('CS');
    expect(courseCodeInput).toHaveValue('101');
    expect(instructorEmailInput).toHaveValue('instructor@example.com');
    expect(yearInput).toHaveValue('2025');
    expect(semesterSelect).toHaveValue('Fall');
  });

  // Test submission of course creation form
  test('submits create course form', async () => {
    render(<CourseManager />);
    
    // Get input elements for course details
    const deptCodeInput = screen.getAllByPlaceholderText('Department Code')[0];
    const courseCodeInput = screen.getAllByPlaceholderText('Course Code')[0];
    const courseNameInput = screen.getByPlaceholderText('Course Name');
    
    // Simulate input changes
    fireEvent.change(deptCodeInput, { target: { value: 'CS' } });
    fireEvent.change(courseCodeInput, { target: { value: '101' } });
    fireEvent.change(courseNameInput, { target: { value: 'Intro to Computer Science' } });

    // Simulate clicking the "Create Course" button
    const createButton = screen.getByRole('button', { name: 'Create Course' });
    fireEvent.click(createButton);
    
    // Wait for the fetch call to be made and assert the expected request
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/createCourse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer test-token',
        },
        credentials: 'include',
        body: JSON.stringify({
          departmentCode: 'CS',
          courseCode: '101',
          name: 'Intro to Computer Science',
          token: 'test-token',
        }),
      });
    });
  });

  // Test submission of section creation form
  test('submits add section form', async () => {
    render(<CourseManager />);
    
    // Get input elements for section details
    const deptCodeInput = screen.getAllByPlaceholderText('Department Code')[1];
    const courseCodeInput = screen.getAllByPlaceholderText('Course Code')[1];
    const instructorEmailInput = screen.getByPlaceholderText('Instructor Email');
    const yearInput = screen.getByPlaceholderText('Year');
    const semesterSelect = screen.getByRole('combobox');
    
    // Simulate input changes
    fireEvent.change(deptCodeInput, { target: { value: 'cs' } });
    fireEvent.change(courseCodeInput, { target: { value: '101' } });
    fireEvent.change(instructorEmailInput, { target: { value: 'instructor@example.com' } });
    fireEvent.change(yearInput, { target: { value: '2025' } });
    fireEvent.change(semesterSelect, { target: { value: 'Fall' } });
    
    // Simulate clicking the "Add Section" button
    const addButton = screen.getByRole('button', { name: 'Add Section' });
    fireEvent.click(addButton);
    
    // Wait for the fetch call to be made and assert the expected request
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/createSection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer test-token',
        },
        credentials: 'include',
        body: JSON.stringify({
          departmentCode: 'CS',
          courseCode: '101',
          email: 'instructor@example.com',
          year: '2025',
          semester: 'Fall',
          token: 'test-token',
        }),
      });
    });
  });
  
  // Test handling of missing token (when cookie is empty)
  test('handles missing token', () => {
    // Clear the cookie to simulate no token
    document.cookie = '';
    
    // Spy on console.error to check for the error message
    const consoleSpy = jest.spyOn(console, 'error');
    
    // Render the component
    render(<CourseManager />);
    
    // Assert that an error message is logged when token is missing
    expect(consoleSpy).toHaveBeenCalledWith('No token found');
    
    // Restore the spy
    consoleSpy.mockRestore();
  });
});

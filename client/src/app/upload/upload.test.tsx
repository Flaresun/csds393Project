import React from "react";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";
import UploadPage from "./components/uploader";

// Mock fetch globally
global.fetch = jest.fn();

// Create a more sophisticated mock for FormData
global.FormData = class {
  constructor() {
    this.data = {};
  }
  append(key, value) {
    this.data[key] = value;
  }
};

// Setup initial component rendering with mocked API responses
async function setupComponent() {
  // Mock API responses
  global.fetch.mockImplementation((url) => {
    if (url === "/api/getDepartment") {
      return Promise.resolve({
        json: () => Promise.resolve({ data: { departments: ["Computer Science"] } })
      });
    } else if (url === "/api/getCourse") {
      return Promise.resolve({
        json: () => Promise.resolve({ data: { courses: ["CSDS132"] } })
      });
    } else if (url === "/api/getSection") {
      return Promise.resolve({
        json: () => Promise.resolve({ 
          data: { sections: [{ id: 1, instructor: "Dr. Connamacher", semester: "Fall", year: 2025 }] } 
        })
      });
    } else if (url === "/api/upload") {
      return Promise.resolve({
        json: () => Promise.resolve({ data: { id: "file-123" } })
      });
    }
    return Promise.reject(new Error(`Unhandled fetch url: ${url}`));
  });

  // Mock document.cookie
  Object.defineProperty(document, 'cookie', {
    writable: true,
    value: 'token=test-token',
  });

  // Render component
  const result = render(<UploadPage />);
  
  // Wait for initial departments to load
  await waitFor(() => {
    expect(global.fetch).toHaveBeenCalledWith("/api/getDepartment", expect.any(Object));
  });
  
  return result;
}

describe("Uploader Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("fetches departments on initial load", async () => {
    await setupComponent();
    expect(global.fetch).toHaveBeenCalledWith("/api/getDepartment", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
  });

  test("fetches courses when department is selected and sections when course is selected", async () => {
    await setupComponent();
    
    // Reset fetch mock to clear previous calls
    global.fetch.mockClear();
    
    // Mock specific response for the next fetch call
    global.fetch.mockImplementationOnce(() => 
      Promise.resolve({
        json: () => Promise.resolve({ data: { courses: ["CSDS132"] } })
      })
    );
    
    // Get department select and change its value
    const selects = screen.getAllByRole("combobox");
    const departmentSelect = selects[0];
    
    // Use act to properly handle state updates
    await act(async () => {
      fireEvent.change(departmentSelect, { target: { value: "Computer Science" } });
    });
    
    // Verify course API call
    expect(global.fetch).toHaveBeenCalledWith("/api/getCourse", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ department: "Computer Science" }),
    });
    
    // Reset fetch mock again
    global.fetch.mockClear();
    
    // Mock response for section API
    global.fetch.mockImplementationOnce(() => 
      Promise.resolve({
        json: () => Promise.resolve({ 
          data: { sections: [{ id: 1, instructor: "Dr. Connamacher", semester: "Fall", year: 2023 }] } 
        })
      })
    );
    
    // Get updated selects
    const updatedSelects = screen.getAllByRole("combobox");
    const courseSelect = updatedSelects[1];
    
    // Select course using act
    await act(async () => {
      fireEvent.change(courseSelect, { target: { value: "CSDS132" } });
    });
    
    // Verify section API call
    expect(global.fetch).toHaveBeenCalledWith("/api/getSection", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 
        department: "Computer Science", 
        course: "CSDS132" 
      }),
    });
  });

  test("shows error message when required fields are missing", async () => {
    // Just mock initial departments load
    global.fetch.mockImplementationOnce(() => 
      mockFetchResponse({ departments: ["Computer Science"] })
    );

    render(<UploadPage />);
    
    // Click upload without selecting anything
    const uploadButton = screen.getByRole("button", { name: /upload file/i });
    fireEvent.click(uploadButton);

    // Verify error message appears
    expect(screen.getByText("Please complete all selections and choose a file.")).toBeInTheDocument();
    
    // Verify upload API was NOT called
    expect(global.fetch).not.toHaveBeenCalledWith("/api/upload", expect.anything());
  });
});
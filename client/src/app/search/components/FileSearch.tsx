"use client";

import React, { useEffect, useState, useContext } from "react";
import "./FileSearch.css";
import { AppContent } from "../../../context/AppContext";

interface File {
  id: number;
  name: string;
  instructor: string;
  semester: string;
  year: number;
  content: string;
}

interface Comment {
  comment_id: number;
  parent_com_id: number;
  content: string;
  note_id: number;
  commenter_id: number;
}

const FileSearch: React.FC = () => {
  const [fileList, setFileList] = useState<File[] | null>(null);
  const [text, setText] = useState<string>("");
  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const [currentPdf, setCurrentPdf] = useState<string | null>(null);
  const [comment, setComment] = useState<string>("");
  const [commentValues, setCommentValues] = useState<Comment[]>();
  const [commentVisibility, setCommentVisibility] = useState<{ [key: number]: boolean }>({});
  const [commentSummaries, setCommentSummaries] = useState<{ [key: number]: string[] | string }>({});
  const { userRole } = useContext<any>(AppContent);

  const token = document.cookie
    .split("; ")
    .find((row) => row.startsWith("token="))
    ?.split("=")[1];

  if (!token) {
    console.error("No token found");
    return null;
  }

  const getFiles = async (className: string | null, token: string) => {
    if (!className) return;

    const res = await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      credentials: "include",
      body: JSON.stringify({ className, token }),
    });

    const { allData } = await res.json();
    console.log(allData);
    setFileList(allData);
  };

  useEffect(() => {
    const queryParams = new URLSearchParams(window.location.search);
    const query = queryParams.get("q");

    if (query && token) {
      getFiles(query, token);
    } else {
      console.log("No token found");
    }
  }, []);

  const openModal = (pdfContent: string) => {
    setCurrentPdf(pdfContent);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setCurrentPdf(null);
  };

  const rateNote = async (noteId: number, rating: number) => {
    const res = await fetch("/api/noteRating", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ note_id: noteId, rating, token }),
      credentials: "include",
    });

    const { comments } = await res.json();
    console.log(comments);
  };

  const getComments = async (noteId: number) => {
    const res = await fetch("/api/getComment", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ note_id: noteId, token }),
      credentials: "include",
    });

    const { comments } = await res.json();
    console.log(comments);
    setCommentValues(comments);
    toggleCommentVisibility(noteId);
  };

  const getCommentSummary = async (noteId: number) => {
    console.log(noteId);
    try {
      const res = await fetch("/api/commentSummary", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ note_id: noteId }),
      });

      const { data } = await res.json();
      console.log(data);
      setCommentSummaries((prev) => ({
        ...prev,
        [noteId]: data || "No summary available.",
      }));
    } catch (error) {
      console.error("Failed to fetch summary:", error);
      setCommentSummaries((prev) => ({
        ...prev,
        [noteId]: "Failed to load summary.",
      }));
    }
  };

  const toggleCommentVisibility = (noteId: number) => {
    setCommentVisibility((prev) => ({
      ...prev,
      [noteId]: !prev[noteId],
    }));
  };

  const handleComment = async (noteId: number, parent_com_id: number | null) => {
    const textarea = document.getElementById("textarea" + noteId) as HTMLTextAreaElement;
    const content = textarea.value;
    textarea.value = "";

    if (content === "") {
      console.log("Write a comment");
      return;
    }

    const res = await fetch("/api/addComment", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ note_id: noteId, parent_com_id, content, token }),
      credentials: "include",
    });

    const data = await res.json();
    console.log(data);
  };

  const deleteNote = async (noteId: number) => {
    const confirmDelete = confirm("Are you sure you want to delete this note?");
    if (!confirmDelete) return;

    try {
      const res = await fetch("/api/deleteNote", {
        method: "post",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
        body: JSON.stringify({ note_id: noteId, token }),
      });

      const result = await res.json();
      console.log("Delete response:", result);

      setFileList((prev) => prev?.filter((file) => file.id !== noteId) || null);
    } catch (error) {
      console.error("Failed to delete note:", error);
    }
  };

  return (
    <div className="bg-gray-900 min-h-screen">
      <div className="title">
        <h1>File Finder</h1>
      </div>

      <div className="input__wrapper text-slate-900">
        <input
          type="text"
          placeholder="Search File"
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            if (!e.target.value) {
              setFileList(fileList);
            }
          }}
        />
        <button onClick={() => getFiles(text, token)}>Search</button>
      </div>

      <div className="body">
        {fileList?.length === 0 && <div className="notFound">No File Found</div>}

        {fileList?.length > 0 &&
          fileList.map((file) => (
            <div className="body__item relative" key={file.id}>
              {userRole == "faculty" && (
                <button
                  onClick={() => deleteNote(file.id)}
                  className="absolute top-2 right-2 text-red-500 hover:text-red-700 font-bold text-lg"
                  title="Delete Note"
                >
                  ✕
                </button>
              )}

              <h3>Class Name: {file.name}</h3>
              <p>Type: pdf</p>
              <p>Instructor: {file.instructor}</p>

              <div className="flex flex-col sm:flex-row items-center justify-between text-center">
                <button onClick={() => openModal(file.content)}>View PDF</button>
                <div className="flex flex-col mt-5 sm:mt-0 items-center">
                  <textarea
                    id={`textarea${file.id}`}
                    onChange={(e) => setComment(e.target.value)}
                    rows={4}
                    cols={20}
                    className="p-2 mr-2 text-slate-900 text-wrap"
                    placeholder="Add a comment"
                  />
                  <button
                    onClick={() => handleComment(file.id, null)}
                    className="p-2 rounded-full border w-1/2 mt-2 active:scale-95 transition-all ease-in-out"
                  >
                    Comment
                  </button>
                </div>
              </div>

              {/* Comment Summary Section */}
              <div className="text-white mt-4">
                <button
                  className="underline text-sm mb-1"
                  onClick={() => getCommentSummary(file.id)}
                >
                  Show Comment Summary
                </button>

                <div className="italic text-sm mt-1">
                  {Array.isArray(commentSummaries[file.id]) ? (
                    <ul className="list-disc ml-5">
                      {(commentSummaries[file.id] as string[]).map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>{commentSummaries[file.id]}</p>
                  )}
                </div>
              </div>

              <div className="flex flex-col items-center mt-4">
                <button
                  onClick={() => getComments(file.id)}
                  className="border rounded-md active:scale-95 p-2"
                >
                  Show Comments
                </button>

                <div
                  className={`comments-section transition-all ease-in-out ${
                    commentVisibility[file.id] ? "max-h-[1000px] opacity-100" : "max-h-0 opacity-0"
                  }`}
                  style={{ overflow: "hidden" }}
                >
                  {commentValues?.map((value, index) => {
                    if (value.note_id === file.id) {
                      return (
                        <div key={index} className="flex p-2 mt-4">
                          <p>{value.content}</p>
                        </div>
                      );
                    }
                    return null;
                  })}
                </div>
              </div>
            </div>
          ))}
      </div>

      {modalOpen && currentPdf && (
        <div className="modal">
          <div className="modal-content">
            <button className="close" onClick={closeModal}>
              Close
            </button>
            <iframe src={`data:application/pdf;base64,${currentPdf}`} width="100%" height="100%" />
          </div>
        </div>
      )}
    </div>
  );
};

export default FileSearch;

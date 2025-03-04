import { useState } from "react";

const getBase64 = (file) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });

const ImageUpload = () => {
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewImage, setPreviewImage] = useState("");
  const [previewTitle, setPreviewTitle] = useState("");
  const [fileList, setFileList] = useState([]);
  const [isPdf, setIsPdf] = useState(false);

  const handleCancel = () => setPreviewOpen(false);

  const handlePreview = async (file) => {
    setPreviewImage(file.preview);
    setPreviewOpen(true);
    setPreviewTitle(file.name);
    setIsPdf(file.type === "application/pdf");
  };

  const handleChange = async (event) => {
    try {
      const file = event.target.files[0];
      if (!file) return;

      // Create preview using base64
      const preview = await getBase64(file);
      const newFileItem = {
        uid: Date.now(),
        name: file.name,
        type: file.type,
        status: 'done',
        preview,
      };
      
      setFileList([newFileItem]);
    } catch (error) {
      console.log(error);
    }
  };

  const handleRemove = (uid) => {
    setFileList(fileList.filter(file => file.uid !== uid));
  };

  return (
    <div>
      {/* Upload Area */}
      <div className="image-upload-container" style={{ border: '1px dashed #d9d9d9', borderRadius: '8px', padding: '8px', marginBottom: '8px' }}>
        {fileList.length >= 1 ? (
          <div className="file-list">
            {fileList.map(file => (
              <div key={file.uid} style={{ display: 'inline-block', margin: '8px', position: 'relative' }}>
                {file.type === "application/pdf" ? (
                  <div 
                    style={{ 
                      width: '100px', 
                      height: '100px', 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center', 
                      backgroundColor: '#f5f5f5', 
                      border: '1px solid #d9d9d9',
                      cursor: 'pointer'
                    }}
                    onClick={() => handlePreview(file)}
                  >
                    <div style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: '24px' }}>📄</div>
                      <div style={{ fontSize: '12px', marginTop: '4px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', width: '90px' }}>
                        {file.name}
                      </div>
                    </div>
                  </div>
                ) : (
                  <img 
                    src={file.preview} 
                    alt={file.name} 
                    style={{ width: '100px', height: '100px', objectFit: 'cover' }}
                    onClick={() => handlePreview(file)} 
                  />
                )}
                <button 
                  onClick={() => handleRemove(file.uid)}
                  style={{ position: 'absolute', bottom: '4px', right: '4px', background: 'rgba(0,0,0,0.5)', color: 'white', border: 'none', borderRadius: '50%', width: '20px', height: '20px', cursor: 'pointer' }}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="upload-button-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '16px', cursor: 'pointer' }}>
            <div style={{ fontSize: '24px' }}>+</div>
            <div style={{ marginTop: 8, fontSize: '18px' }}>Upload an Image or PDF</div>
            <input 
              type="file" 
              accept="image/*,application/pdf" 
              onChange={handleChange} 
              style={{ opacity: 0, position: 'absolute', width: '100%', height: '100%', cursor: 'pointer' }}
            />
          </div>
        )}
      </div>

      {/* Preview Modal */}
      {previewOpen && (
        <div className="modal-overlay" style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div className="modal-content" style={{
            backgroundColor: 'white',
            padding: '20px',
            borderRadius: '8px',
            maxWidth: '80%',
            maxHeight: '80%',
            overflow: 'auto'
          }}>
            <div className="modal-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
              <h3>{previewTitle}</h3>
              <button onClick={handleCancel} style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}>×</button>
            </div>
            {isPdf ? (
              <div style={{ height: '500px', width: '100%' }}>
                <object
                  data={previewImage}
                  type="application/pdf"
                  width="100%"
                  height="100%"
                >
                  <p>Your browser does not support PDFs. 
                     <a href={previewImage} target="_blank" rel="noreferrer">Click here to view</a>
                  </p>
                </object>
              </div>
            ) : (
              <img alt="preview" style={{ width: "100%" }} src={previewImage} />
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
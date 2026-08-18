import React, { useEffect, useState, useCallback } from 'react';
import { FileContent, FileInfo, getAgentFileContent, getAgentFiles } from '../api';

interface FileBrowserProps {
  agentId: string;
}

const FileBrowser: React.FC<FileBrowserProps> = ({ agentId }) => {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [currentPath, setCurrentPath] = useState<string>('/');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<FileContent | null>(null);
  const [fileLoading, setFileLoading] = useState<boolean>(false);
  const [fileError, setFileError] = useState<string | null>(null);

  const fetchFiles = useCallback(async (path: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAgentFiles(agentId, path);
      setFiles(data);
      setCurrentPath(path);
      setSelectedFile(null);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch directory contents.');
    } finally {
      setLoading(false);
    }
  }, [agentId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchFiles('/');
  }, [fetchFiles]);

  const getChildPath = useCallback((fileName: string) => (
    currentPath === '/' ? `/${fileName}` : `${currentPath}/${fileName}`
  ), [currentPath]);

  const loadFileContent = async (fileName: string) => {
    const filePath = getChildPath(fileName);
    setFileLoading(true);
    setFileError(null);
    try {
      const content = await getAgentFileContent(agentId, filePath);
      setSelectedFile(content);
    } catch (err) {
      console.error(err);
      setSelectedFile(null);
      setFileError('Failed to fetch file contents.');
    } finally {
      setFileLoading(false);
    }
  };

  const navigateTo = (fileName: string, type: string) => {
    if (type === 'directory') {
      fetchFiles(getChildPath(fileName));
    } else {
      void loadFileContent(fileName);
    }
  };

  const navigateBack = () => {
    if (currentPath === '/') return;
    const parts = currentPath.split('/').filter(p => p !== '');
    parts.pop();
    const newPath = parts.length === 0 ? '/' : `/${parts.join('/')}`;
    fetchFiles(newPath);
  };

  return (
    <div className="flex flex-col gap-4">
      <header className="flex justify-between items-center bg-surface border border-border p-3 rounded-t-lg">
        <div className="flex items-center gap-4 text-sm font-mono overflow-hidden">
          <button 
            onClick={navigateBack} 
            disabled={currentPath === '/'}
            className="text-accent hover:underline disabled:text-muted"
          >
            .. [Up]
          </button>
          <span className="text-muted">Path:</span>
          <span className="text-text truncate">{currentPath}</span>
        </div>
        <button 
          onClick={() => fetchFiles(currentPath)}
          className="text-xs px-2 py-1 bg-background border border-border rounded hover:bg-border transition-colors"
        >
          Refresh
        </button>
      </header>

      <div className="bg-surface border-x border-b border-border rounded-b-lg overflow-hidden">
        {loading ? (
          <div className="p-10 text-center text-muted italic">Accessing remote filesystem...</div>
        ) : error ? (
          <div className="p-10 text-center text-error">{error}</div>
        ) : (
          <table className="w-full text-left text-sm font-mono">
            <thead className="bg-background border-b border-border text-muted uppercase text-xs">
              <tr>
                <th className="px-4 py-2 font-normal">Name</th>
                <th className="px-4 py-2 font-normal">Type</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file) => (
                <tr 
                  key={file.name} 
                  onClick={() => navigateTo(file.name, file.type)}
                  className="border-b border-border hover:bg-background cursor-pointer transition-colors"
                >
                  <td className="px-4 py-3 flex items-center gap-2">
                    <span className={file.type === 'directory' ? 'text-accent' : 'text-text'}>
                      {file.type === 'directory' ? '📁' : '📄'}
                    </span>
                    <span>{file.name}</span>
                  </td>
                  <td className="px-4 py-3 text-muted capitalize">{file.type}</td>
                </tr>
              ))}
              {files.length === 0 && (
                <tr>
                  <td colSpan={2} className="px-4 py-10 text-center text-muted italic">Empty directory.</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      {(fileLoading || fileError || selectedFile) && (
        <section className="bg-surface border border-border rounded-lg overflow-hidden">
          <header className="bg-background border-b border-border px-4 py-2 flex justify-between items-center">
            <span className="text-sm font-mono text-accent">{selectedFile?.path || 'Loading file...'}</span>
            <button
              onClick={() => setSelectedFile(null)}
              className="text-xs text-muted hover:text-text transition-colors"
              type="button"
            >
              Close
            </button>
          </header>
          <div className="p-4 max-h-[420px] overflow-auto bg-black">
            {fileLoading ? (
              <div className="text-muted italic text-sm">Reading remote file...</div>
            ) : fileError ? (
              <div className="text-error text-sm">{fileError}</div>
            ) : (
              <pre className="whitespace-pre-wrap break-words text-success text-xs font-mono leading-relaxed">
                {selectedFile?.content || ''}
              </pre>
            )}
          </div>
        </section>
      )}
    </div>
  );
};

export default FileBrowser;

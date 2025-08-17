import { useState, useEffect, useRef } from 'react';
import { FileUp, Search, SlidersHorizontal, Table2, Image as ImageIcon, Video, FileText, Bot, Save, Code, CheckCircle, XCircle, FileAudio, FileDigit, Globe, Layers, Settings, ChevronRight, ChevronDown, ChevronUp } from 'lucide-react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, doc, addDoc, onSnapshot, collection, serverTimestamp, query, orderBy } from 'firebase/firestore';
import Button from './Button';

const LOCAL_STORAGE_KEY = 'reconciliation-services-state';

// Simple utility to simulate a delay
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const App = () => {
  const mainRef = useRef(null);
  const consoleRef = useRef(null);
  
  // Firebase State
  const [db, setDb] = useState(null);
  const [auth, setAuth] = useState(null);
  const [userId, setUserId] = useState(null);
  const [isAuthReady, setIsAuthReady] = useState(false);
  const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';

  // App State
  const [activeMode, setActiveMode] = useState('llm-reconcile');
  const [fileContent, setFileContent] = useState(null);
  const [fileName, setFileName] = useState("");
  const [dataType, setDataType] = useState('tabular');
  const [llmPrompt, setLlmPrompt] = useState("");
  const [llmResponse, setLlmResponse] = useState("");
  const [llmLoading, setLlmLoading] = useState(false);
  const [isDeveloperMode, setIsDeveloperMode] = useState(false);
  const [devLog, setDevLog] = useState([]);
  const [expandedLog, setExpandedLog] = useState(null);

  // Load state from local storage
  useEffect(() => {
    const storedState = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    if (storedState) {
      setFileContent(storedState.fileContent);
      setFileName(storedState.fileName);
      setDataType(storedState.dataType);
      setIsDeveloperMode(storedState.isDeveloperMode);
      if (storedState.fileContent) setActiveMode('file-view');
    }
  }, []);

  // Save state to local storage
  useEffect(() => {
    const stateToSave = { fileContent, fileName, dataType, isDeveloperMode };
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(stateToSave));
  }, [fileContent, fileName, dataType, isDeveloperMode]);
  
  // Initialize Firebase
  useEffect(() => {
    const initFirebase = async () => {
      try {
        const firebaseConfig = JSON.parse(process.env.REACT_APP_FIREBASE_CONFIG);
        const app = initializeApp(firebaseConfig);
        const authInstance = getAuth(app);
        const dbInstance = getFirestore(app);
        
        setAuth(authInstance);
        setDb(dbInstance);

        if (typeof __initial_auth_token !== 'undefined') {
          await signInWithCustomToken(authInstance, __initial_auth_token);
        } else {
          await signInAnonymously(authInstance);
        }
      } catch (e) {
        console.error("Firebase init error:", e);
      }
    };
    initFirebase();
  }, []);

  // Auth state listener
  useEffect(() => {
    if (!auth || !db) return;

    const unsubscribe = onAuthStateChanged(auth, (user) => {
      const currentUserId = user ? user.uid : crypto.randomUUID();
      setUserId(currentUserId);
      setIsAuthReady(true);

      if (user) {
        const logsCollectionRef = collection(db, `artifacts/${appId}/users/${currentUserId}/conversations`);
        const q = query(logsCollectionRef);
        
        const unsubscribeSnapshot = onSnapshot(q, (snapshot) => {
          const logs = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
          logs.sort((a, b) => (a.timestamp?.seconds || 0) - (b.timestamp?.seconds || 0));
          setDevLog(logs);
        });
  
        return () => unsubscribeSnapshot();
      }
    });

    return () => unsubscribe();
  }, [auth, db, appId]);
  
  // Mouse hover effect
  useEffect(() => {
    const handleMouseMove = (e) => {
      const el = mainRef.current;
      if (!el) return;
      const rect = el.getBoundingClientRect();
      el.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
      el.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
    };

    const currentRef = mainRef.current;
    currentRef?.addEventListener('mousemove', handleMouseMove);

    return () => {
      currentRef?.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  // Auto-scroll console
  useEffect(() => {
    consoleRef.current?.scrollTo(0, consoleRef.current.scrollHeight);
  }, [devLog]);

  // Log interactions to Firestore
  const logInteraction = async (message, type, details = {}) => {
    if (!isAuthReady || !db || !userId) return;
    
    try {
      await addDoc(collection(db, `artifacts/${appId}/users/${userId}/conversations`), {
        message,
        type,
        timestamp: serverTimestamp(),
        details: JSON.stringify(details),
      });
    } catch (e) {
      console.error("Firestore error:", e);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setActiveMode('file-view');
    const reader = new FileReader();
    const isTextType = ['tabular', 'text', '3d-model', 'gis', 'all-files'].includes(dataType);

    if (isTextType) {
      reader.onload = (e) => {
        setFileContent(e.target.result);
        logInteraction(`File uploaded: ${file.name}`, "INFO", { 
          fileName: file.name, 
          fileSize: file.size, 
          fileType: file.type 
        });
      };
      reader.readAsText(file);
    } else {
      setFileContent(URL.createObjectURL(file));
      logInteraction(`File uploaded: ${file.name}`, "INFO", {
        fileName: file.name,
        fileSize: file.size,
        fileType: file.type
      });
    }
  };

  const handleLlmReconcile = async () => {
    setLlmLoading(true);
    setLlmResponse("");
    setExpandedLog(null);
    
    logInteraction("Reconciliation job initiated.", "INFO");
    await sleep(500);
    logInteraction("Preprocessing user input...", "INFO");

    const mockRequest = { 
      model: "gemini-1.5-pro", 
      action: "reconcile", 
      input_data: llmPrompt.split(',').map(s => s.trim()) 
    };
    
    await sleep(1000);
    logInteraction("Calling LLM API...", "API", { type: "request", payload: mockRequest });

    await sleep(2000);
    const mockApiResponse = {
      status: "success",
      comment: "Based on your input, here are the top matching entities:",
      results: [
        { query: "New York", match: "New York City (Q60)", confidence: 0.98, type: "city" },
        { query: "Paris", match: "Paris (Q90)", confidence: 0.95, type: "city" }
      ],
      job_id: "job_xyz_123"
    };
    
    logInteraction("LLM response received.", "API", { type: "response", payload: mockApiResponse });
    await sleep(500);
    logInteraction("Parsing results...", "INFO");

    const formattedResponse = `
**Results:**
${mockApiResponse.results.map(e => (
  `* **Query:** ${e.query}\n  * **Match:** ${e.match}\n  * **Confidence:** ${e.confidence}`
)).join('\n\n')}
---
**Commentary:**
${mockApiResponse.comment}
    `;
    
    setLlmResponse(formattedResponse);
    await sleep(500);
    logInteraction("Rendering results to UI.", "SUCCESS");
    setLlmLoading(false);
  };

  const handleExport = () => {
    if (!fileContent) {
      alert("No data to export!");
      return;
    }
    
    const blob = new Blob([fileContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reconciled_${fileName}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    logInteraction("File exported.", "INFO", { fileName: a.download });
  };

  const renderFilePreview = () => {
    switch (dataType) {
      case 'tabular':
        const lines = fileContent.trim().split('\n');
        const headers = lines[0].split(',');
        const rows = lines.slice(1).map(line => line.split(','));
        
        return (
          <div className="overflow-hidden border border-gray-700 rounded-lg">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-700">
                <thead className="bg-gray-800">
                  <tr>
                    {headers.map((header) => (
                      <th key={header} className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-gray-800 divide-y divide-gray-700">
                  {rows.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                      {row.map((cell, cellIndex) => (
                        <td key={cellIndex} className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                          {cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );

      case 'image':
        return (
          <div className="flex justify-center items-center p-4">
            <img 
              src={fileContent} 
              alt={fileName} 
              className="max-w-full max-h-[80vh] rounded-lg" 
            />
          </div>
        );

      case 'video':
        return (
          <div className="flex justify-center items-center p-4">
            <video 
              controls 
              src={fileContent} 
              className="max-w-full max-h-[80vh] rounded-lg" 
            />
          </div>
        );

      case 'audio':
        return (
          <div className="flex justify-center items-center p-4">
            <audio 
              controls 
              src={fileContent} 
              className="w-full max-w-2xl" 
            />
          </div>
        );

      default: // text, 3d-model, gis, all-files
        return (
          <div className="p-6 overflow-x-auto bg-gray-800 text-gray-300 rounded-lg">
            <pre className="text-sm whitespace-pre-wrap break-words">
              {fileContent}
            </pre>
          </div>
        );
    }
  };

  const fileAccept = {
    'tabular': '.csv,.tsv,.xlsx',
    'image': 'image/*',
    'video': 'video/*',
    'audio': 'audio/*',
    'text': '.txt,.json,.xml,.yaml,.rdf,.ttl,.n3',
    '3d-model': '.obj,.mtl,.fbx',
    'gis': '.shp,.kml,.geojson',
    'all-files': '*'
  };

  return (
    <div className="flex flex-col h-screen font-sans bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 p-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">Reconciliation</h1>
        <div className="flex items-center space-x-4">
          <button 
            onClick={handleExport}
            className="p-3 bg-gray-800 text-gray-300 rounded-xl hover:bg-gray-700 transition-transform duration-200 transform hover:scale-105"
          >
            <Save size={20} />
          </button>
          <button 
            onClick={() => setIsDeveloperMode(!isDeveloperMode)}
            className={`p-3 rounded-xl transition-transform duration-200 transform hover:scale-105 ${
              isDeveloperMode 
                ? 'bg-purple-600 text-white' 
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            <Settings size={20} />
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-auto p-12 relative overflow-hidden group">
        {/* Animated hover background */}
        <div 
          ref={mainRef}
          className="absolute inset-0 z-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          style={{
            background: 'radial-gradient(400px circle at var(--mouse-x) var(--mouse-y), rgba(124, 58, 237, 0.1), transparent 80%)'
          }}
        ></div>

        {/* Content Card */}
        <div className="bg-gray-900 shadow-2xl rounded-2xl p-12 relative z-10 transition-transform duration-300">
          {/* Mode Title */}
          <h2 className="text-3xl font-bold flex items-center gap-4 mb-8 text-white">
            {activeMode === 'llm-reconcile' ? (
              <>
                <Bot size={32} className="text-purple-400" />
                LLM Reconcile
              </>
            ) : (
              <>
                <FileText size={32} className="text-purple-400" />
                File View & Tools
              </>
            )}
          </h2>

          {/* LLM Reconcile Mode */}
          {activeMode === 'llm-reconcile' && (
            <div className="space-y-6">
              <textarea
                value={llmPrompt}
                onChange={(e) => setLlmPrompt(e.target.value)}
                rows={4}
                placeholder="Enter data or a query..."
                className="w-full p-4 bg-gray-800 border border-gray-700 text-gray-100 placeholder-gray-400 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-shadow duration-300"
              />
              
              <Button
                onClick={handleLlmReconcile}
                disabled={!llmPrompt || llmLoading}
                className="w-full text-lg"
              >
                {llmLoading ? (
                  <span className="flex items-center justify-center space-x-2">
                    <span className="animate-pulse">Reconciling...</span>
                  </span>
                ) : 'Reconcile'}
              </Button>
              
              <div className="flex items-center justify-center space-x-4">
                <span className="text-lg text-gray-500">or</span>
                <label 
                  htmlFor="file-input" 
                  className="cursor-pointer py-3 px-6 text-purple-400 font-medium bg-gray-800 rounded-xl hover:bg-gray-700 transition-colors duration-200 transform hover:scale-105 flex items-center gap-2"
                >
                  <FileUp size={20} /> Upload a file
                </label>
                <input 
                  type="file" 
                  id="file-input" 
                  className="hidden" 
                  onChange={handleFileChange} 
                  accept={fileAccept[dataType]} 
                />
              </div>
              
              {llmResponse && (
                <div className="mt-8 p-6 bg-gray-800 border border-gray-700 rounded-xl transition-opacity duration-500">
                  <h4 className="font-semibold text-xl mb-4">LLM Response:</h4>
                  <pre className="text-sm text-gray-300 whitespace-pre-wrap break-words">
                    {llmResponse}
                  </pre>
                </div>
              )}
            </div>
          )}

          {/* File View Mode */}
          {activeMode === 'file-view' && (
            <div className="space-y-8">
              <div className="flex items-center space-x-4">
                <ChevronRight size={24} className="text-purple-400" />
                <span className="text-lg text-gray-400 font-medium">Viewing:</span>
                <div className="flex-1">
                  <select
                    value={dataType}
                    onChange={(e) => setDataType(e.target.value)}
                    className="w-48 px-4 py-2 bg-gray-800 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="tabular">Tabular</option>
                    <option value="image">Image</option>
                    <option value="video">Video</option>
                    <option value="audio">Audio</option>
                    <option value="text">Text & KG</option>
                    <option value="3d-model">3D Model</option>
                    <option value="gis">GIS</option>
                    <option value="all-files">All Files</option>
                  </select>
                </div>
              </div>
              
              {fileContent && renderFilePreview()}

              <div className="border-t border-gray-700 pt-8">
                <h3 className="text-2xl font-bold flex items-center gap-2 mb-6">Tools</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {dataType === 'tabular' ? (
                    <>
                      <div className="p-8 bg-gray-800 rounded-xl space-y-4 transition-transform duration-200 transform hover:scale-[1.02] cursor-pointer">
                        <h4 className="flex items-center gap-2 text-lg font-medium text-purple-400">
                          <Search size={20} /> Manual Reconcile
                        </h4>
                        <select className="w-full px-4 py-3 bg-gray-900 border border-gray-700 text-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500">
                          <option>-- Choose a column --</option>
                          {fileContent?.split('\n')[0]?.split(',').map((col, i) => (
                            <option key={i} value={col}>{col}</option>
                          ))}
                        </select>
                        <input 
                          type="text" 
                          placeholder="Service Endpoint" 
                          className="w-full px-4 py-3 bg-gray-900 border border-gray-700 text-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500" 
                        />
                        <button className="w-full py-3 text-white font-medium bg-blue-600 hover:bg-blue-700 rounded-xl transition-transform duration-200 transform hover:scale-105">
                          Start
                        </button>
                      </div>
                      
                      <div className="p-8 bg-gray-800 rounded-xl space-y-4 transition-transform duration-200 transform hover:scale-[1.02] cursor-pointer">
                        <h4 className="flex items-center gap-2 text-lg font-medium text-purple-400">
                          <SlidersHorizontal size={20} /> Facets & Clusters
                        </h4>
                        <p className="text-sm text-gray-400">Filter and group data to clean it up.</p>
                        <button className="w-full py-3 text-white font-medium bg-pink-600 hover:bg-pink-700 rounded-xl transition-transform duration-200 transform hover:scale-105">
                          Analyze
                        </button>
                      </div>
                    </>
                  ) : (
                    <div className="p-8 bg-gray-800 rounded-xl col-span-full">
                      <p className="text-sm text-gray-400 text-center">
                        No additional tools for this file type.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Developer Console */}
        {isDeveloperMode && (
          <div className="mt-12 bg-gray-900 shadow-2xl rounded-2xl p-8">
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2 text-white">
              <Code size={24} className="text-green-400" /> Developer Console
            </h3>
            <p className="text-xs text-gray-500 mb-4">
              User ID: <span className="font-mono text-gray-400 break-all">{userId}</span>
            </p>
            <div 
              ref={consoleRef}
              className="bg-gray-950 p-4 text-xs font-mono text-gray-400 rounded-xl border border-gray-800 h-64 overflow-y-auto"
            >
              {devLog.length > 0 ? (
                devLog.map((log) => (
                  <div key={log.id} className="py-1 border-b border-gray-800 last:border-b-0">
                    <div className="flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <span className={`
                          font-bold px-2 py-0.5 rounded
                          ${log.type === 'INFO' ? 'bg-gray-700 text-gray-300' :
                             log.type === 'API' ? 'bg-blue-700 text-blue-200' :
                             'bg-green-700 text-green-200'}
                        `}>
                          {log.type}
                        </span>
                        [{log.timestamp?.toDate().toLocaleTimeString() || 'N/A'}] {log.message}
                      </span>
                      {log.details && (
                        <button 
                          onClick={() => setExpandedLog(expandedLog === log.id ? null : log.id)}
                          className="text-gray-500 hover:text-gray-300 transition-colors"
                        >
                          {expandedLog === log.id ? (
                            <ChevronUp size={16} />
                          ) : (
                            <ChevronDown size={16} />
                          )}
                        </button>
                      )}
                    </div>
                    {expandedLog === log.id && log.details && (
                      <pre className="mt-2 p-3 bg-gray-800 rounded-lg text-gray-300 overflow-x-auto whitespace-pre-wrap break-words">
                        {JSON.stringify(JSON.parse(log.details), null, 2)}
                      </pre>
                    )}
                  </div>
                ))
              ) : (
                <p className="text-center text-gray-600">
                  Console is idle. Trigger an action to view logs.
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
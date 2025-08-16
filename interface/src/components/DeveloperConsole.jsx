import { Code, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

export default function DevConsole({ logs }) {
  const [expanded, setExpanded] = useState(null);
  
  return (
    <div className="console">
      {logs.map((log) => (
        <div key={log.id} className={`log-item ${log.type}`}>
          <div className="log-header">
            <Code size={16} />
            <span>{log.message}</span>
            {log.details && (
              <button onClick={() => setExpanded(expanded === log.id ? null : log.id)}>
                {expanded === log.id ? <ChevronUp /> : <ChevronDown />}
              </button>
            )}
          </div>
          {expanded === log.id && (
            <pre>{JSON.stringify(log.details, null, 2)}</pre>
          )}
        </div>
      ))}
    </div>
  );
}
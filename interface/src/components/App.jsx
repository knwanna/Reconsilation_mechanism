import { FirebaseProvider } from './contexts/FirebaseContext';
import ReconciliationPanel from './components/ReconciliationPanel';
import FileProcessor from './components/FileProcessor';
import DeveloperConsole from './components/DeveloperConsole';

function App() {
  return (
    <FirebaseProvider>
      <main className="app-container">
        <ReconciliationPanel />
        <FileProcessor />
        <DeveloperConsole logs={[]} />
      </main>
    </FirebaseProvider>
  );
}

export default App;
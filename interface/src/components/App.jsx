import { CssBaseline, ThemeProvider } from '@mui/material';
import { FirebaseProvider } from '../contexts/FirebaseContext';
import theme from '../theme';
import ReconciliationPanel from './ReconciliationPanel';
import FileProcessor from './FileProcessor';
import DeveloperConsole from './DeveloperConsole';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <FirebaseProvider>
        <div className="app-container">
          <ReconciliationPanel />
          <FileProcessor />
          <DeveloperConsole logs={[]} />
        </div>
      </FirebaseProvider>
    </ThemeProvider>
  );
}

export default App;
import { useContext } from 'react';
import { FirebaseContext } from '../contexts/FirebaseContext';

export default function useFirebase() {
  const context = useContext(FirebaseContext);
  if (!context) {
    throw new Error('useFirebase must be used within FirebaseProvider');
  }
  return context;
}
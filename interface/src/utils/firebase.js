import { initializeApp } from 'firebase/app';
import { getAuth, getFirestore } from 'firebase/auth';

export const initFirebase = () => {
  const firebaseConfig = JSON.parse(process.env.REACT_APP_FIREBASE_CONFIG);
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  const db = getFirestore(app);
  
  return { app, auth, db };
};
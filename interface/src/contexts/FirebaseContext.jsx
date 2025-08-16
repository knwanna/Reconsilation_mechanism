import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { createContext } from 'react';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export const FirebaseContext = createContext({ app, auth });

export function FirebaseProvider({ children }) {
  return (
    <FirebaseContext.Provider value={{ app, auth }}>
      {children}
    </FirebaseContext.Provider>
  );
}
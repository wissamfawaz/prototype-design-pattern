// Import the functions you need from the SDKs you need
import firebase from "firebase/compat/app"
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import "firebase/compat/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey:  process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: "air-canvas-project.firebaseapp.com",
  projectId: "air-canvas-project",
  storageBucket: "air-canvas-project.appspot.com",
  messagingSenderId: "69767440853",
  appId: "1:69767440853:web:048c807dbe0dbb7e7d355c",
  measurementId: "G-KHS1YN3B2S"
};

const app = firebase.initializeApp(firebaseConfig)
const analytics = getAnalytics(app);

export const auth = firebase.auth();
const provider = new firebase.auth.GoogleAuthProvider();
provider.setCustomParameters({ prompt: 'select_account' });

export const signInWithGoogle = () => auth.signInWithPopup(provider);

export default firebase;
// Firebase Configuration for ZATCA News Manager
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
import { getFirestore, collection, onSnapshot, addDoc, updateDoc, deleteDoc, doc, writeBatch } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyD4GC0EkaZokVoMWey1qsZqVH5_CNZZb20",
    authDomain: "zakat-e1390.firebaseapp.com",
    projectId: "zakat-e1390",
    storageBucket: "zakat-e1390.firebasestorage.app",
    messagingSenderId: "251476239876",
    appId: "1:251476239876:web:118c663c5c8b1ad43a3751",
    measurementId: "G-2J0JKFH4RV"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export { collection, onSnapshot, addDoc, updateDoc, deleteDoc, doc, writeBatch };

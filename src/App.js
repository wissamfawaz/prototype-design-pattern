import logo from './logo.svg';
import Login from './components/Login';
import Home from './components/Home';
import Info from './components/Info';
import Creators from './components/Creators';
import ProdDemo from './components/ProdDemo';
import firebase from './firebase';
import { useState, useEffect } from 'react';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    firebase.auth().onAuthStateChanged(user => {
      setUser(user);
    })
  }, [])

  return (
    <>
    {user ? <Home props={user} /> 
    : <>
        <Login/> 
        <Info /> 
        <ProdDemo />
        <Creators />
      </>}
    </>
  );
}

export default App;

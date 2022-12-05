import particlesConfig from '../config/particlesConfig';
import Particles from 'react-tsparticles';
import { loadFull } from 'tsparticles';
import { signInWithGoogle } from '../firebase';

import '../styles/Login.css';

const Login = () => {
  return (
    <div id="login">
        <h1 id="main-title"> Air Canvas <br/> Your fingertips are your brush!</h1>
        <button id="start-button" onClick={signInWithGoogle}> Let's start! </button>
        <h4> If you're curious, you can also scroll down to read a bit about our product and the creators! (us ;))</h4>
      <Particles id = "tsparticles" height="100vh" width="100vw" init = {async (main) => {await loadFull(main)}} options={particlesConfig}></Particles>
    </div>
  );
}

export default Login;

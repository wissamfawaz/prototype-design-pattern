import { auth } from "../firebase";
import '../styles/Home.css';
import { useState, useEffect } from "react";
import mainFile from "../media/main.exe"

const Home = ({props}) => {
    return(
        <>
        <section id="home">
            <h1>Hello {props.displayName}! </h1>
            <img src={props.photoURL} id="pfp" alt="Profile Picture" />
            <h2>Let's get started, for real this time.</h2>
            <p> You have 2 options: <br/> Download the file and run it on your laptop or open the code in Google Colab</p>
            <div id="buttons">
                <a href={mainFile} download>
                    <button> Download the code</button> <br/>
                </a>
                <button onClick={() => { window.open("https://colab.research.google.com/drive/1y5iXuroVAj2JF3ePJregRPKnDDfZVN8D?usp=sharing", "_blank")}}> Open in Google Colab</button>
            </div>

            <h1> Hold on, we have a feature that allows you to create a cover image with our theme super easily! Fill this out: </h1>
            <PhotoForm />

            <h3>Don't like what you see? You can log out at any moment</h3>
            <button className="signout" onClick={() => auth.signOut()}>Sign out</button>
        </section>

        </>

    )
}


const PhotoForm = (props) => {
    const [text, setText] = useState('');
    const [img, setImg] = useState(null);

    const changeText = (event) => {
        setText(event.target.value);
    };

    const transferValue = async (event) => {
        event.preventDefault();
        const val = { text }
        let data = {
            "template": "kY4Qv7D8VemmZB0qmP",
            "modifications": [
              {
                "name": "message",
                "text": val.text,
                "color": null,
                "background": null
              },
              {
                "name": "face",
                "image_url": "https://i.ytimg.com/vi/e90eWYPNtJ8/mqdefault.jpg"
              }
            ],
            "webhook_url": null,
            "transparent": false,
            "metadata": null
          }


        await fetch('https://api.bannerbear.com/v2/images', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type' : 'application/json',
                'Authorization' : `Bearer ${process.env.REACT_APP_BANNER_BEAR_API_KEY}`
            }
        })

    };

    let displayValue = async (e) => { 
        e.preventDefault();
        fetch('https://api.bannerbear.com/v2/images/', {
                method: 'GET',
                headers: {
                    'Authorization' : `Bearer  ${process.env.REACT_APP_BANNER_BEAR_API_KEY}`
        }
    })
    .then(response => response.json())
    .then((e) => {
        console.log(e[0]['image_url']);
        setImg(e[0]['image_url'])
    })
}

    useEffect(() => {
        
      }, [img]);
    

    return (
        <>
        {img === null ? 
            <div id="Picture info">
                <label>Text you would like to put in your picture</label> <br/>
                <input type="text" value={text} onChange={changeText} /> <br/>
                <button onClick={transferValue}> Generate</button> <br/>
                <button onClick={displayValue}> Display Image</button> <br/>
            </div> 
            : 
            <div>
                <img src={img} alt="icons" />
                <button onClick={displayValue} >Regenerate</button>
            </div>
 }
        </>

    );
}

export default Home;
import '../styles/Info.css';

const Info = () => {
    return(
        <section className="cards">
            <Card title="What?" details="We love technology and we hate whiteboard markers. We also thought that using our fingers to draw would be cool." />
            <Card title="How?" details="We decided to make an air-canvas where you can draw with 0 additional tools. Sign in, download the file, and you're good to go!" />
            <Card title="Is it free?" details="Yes, and it will always be. The code is open source and to be honest, the community helped us write it :)" />
        </section>
    )
}

export const Card = ({title, details}) => {
    return(
        <div className="card">
        <h2>{title}</h2>
        <p>{details}</p>
        </div>
    )
}

export default Info;
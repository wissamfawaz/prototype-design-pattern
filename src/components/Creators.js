import '../styles/Creators.css';
import chris from '../media/chris.jpeg';
import nour from '../media/nour.jpg'
import riad from '../media/riad.jpeg';

const Creators = () => {
    return(
        <section id = "creators">
            <Creator pic = {chris} name = "Christopher" desc="Likes to eat" />
            <Creator pic = {nour} name = "Nour" desc="Obsessed with ducks" />
            <Creator pic = {riad} name = "Mohamad Riad" desc="Is a ginger"/>
        </section>
    )


}

const Creator = ({name, pic, desc}) => {
    return(
        <div className="creator">
            <img src={pic}/>
            <h2>{name}</h2>
            <p>{desc}</p>
        </div>
    )
}

export default Creators;
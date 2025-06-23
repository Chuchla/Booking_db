import {useState, useEffect} from "react";
import {Link} from "react-router-dom";

function PropertiesList({list}) {


    if (!list) return <p>Loading...</p>
    const message = list.length === 0 && <p>No item found</p>
    return (
        <>
        {message}
        <ul className="list-group">
            {list.map((ele, index) => (
                <li key={index} className="list-group-item">
                    <div className='card' style={{ width: '18rem' }}>
                        <img src='vite.svg' className="card-img-top" alt='...'></img>
                        <div className='card-body'>
                            <h5 className='card-title'>{ele.name}</h5>
                            <p className='card-text'>{ele.description}</p>
                            <p className='card-text'><strong>{ele.price} zł / noc</strong> </p>
                            <p className='card-footer'>{ele.country} {ele.region} {ele.city} ul.{ele.street}</p>
                            <Link className='btn btn-primary' to={`/property/${ele.house_id}`}>
                                Obejrzyj!
                            </Link>
                        </div>
                    </div>
                </li>
            ))}
        </ul>
        </>
    );
}

export default PropertiesList;

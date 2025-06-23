import {Fragment, useState} from "react";
import eventHandler from "bootstrap/js/src/dom/event-handler.js";
// Jest spora szansa ze zamiast li key={ele] bedziesz robil li key={ele.id} jezeli ele to np jeden z domow, bo
// wtedy masz szanse sie do kazdego z nich odowlac


function ListGroup({list, onSelectItem}) {
    //var items = ['Rejestracja', 'Logowanie', 'Przegladanie obiektow', 'Zarzadzanie obiektami', 'Wystaw opinie']
    // Hook - get into build in features of React
    const [selectedIndex, setSelectedIndex] = useState(-1);
    const [name, setName] = useState('')
    //arr[0] // variable (selectedIndex)
    //arr[1] // updated function

    // Logika A * 1 = A A * 0 = 0 dlatego items.length === 0 && <p>No item found</p> == no item found
    const message = list.length === 0 && <p>No item found</p>;
    return (

        <Fragment>
            {message}
            <ul className="list-group">
                {list.map((ele, index) => (
                    <li className={ selectedIndex === index ? "list-group-item active" : "list-group-item"}
                        key={ele}
                        onClick={() => {
                            setSelectedIndex(index)
                            onSelectItem(ele)
                        }}

                    >
                        {message}
                        {ele}
                    </li>))}
            </ul>
        </Fragment>
);
}

export default ListGroup;
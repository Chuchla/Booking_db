import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import BookingForm from "./forms/BookingForm.jsx";
import BookingCalendar from "./BookingCalendar.jsx";
import {ReviewForm} from "./forms/ReviewForm.jsx";

function PropertyDetails()
{
    const { houseId } = useParams();
    const [property, setProperty] = useState(null);

    useEffect(() => {
    fetch(`http://localhost:8000/api/property/${houseId}/`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch property details");
        }
        return res.json();
      })
      .then((data) => setProperty(data))
      .catch((err) => console.error(err));
  }, [houseId]);

    if (!property) return <p>Loading details...</p>;

    return(
        <div>
            <h2>{property.name}</h2>
            <p><strong>Opis:</strong> {property.description}</p>
            <p><strong>Cena:</strong> {property.price}</p>
            <BookingForm houseId={property.house_id}/>
            <BookingCalendar houseId={property.house_id}/>
            <ReviewForm houseId={property.house_id}/>
        </div>
    )
}

export default PropertyDetails;
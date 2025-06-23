import Calendar from "react-calendar";
import 'react-calendar/dist/Calendar.css';
import {useState, useEffect} from "react";

function BookingCalendar({houseId}) {
    const [bookings, setBookings] = useState([]);
    const [selectedDate, setSelectedDate] = useState(new Date());
    const stripTime = (date) => {
        return new Date(date.getFullYear(), date.getMonth(), date.getDate());
    }
    useEffect(() => {
        fetch(`http://localhost:8000/api/booking/${houseId}/`)
            .then((res) => res.json())
            .then((data) => setBookings(data))
            .catch((err) => console.error("Booking fetch error:", err));
    }, [houseId]);


    const tileClassName = ({date, view}) => {
        if (view !== 'month') return;

        const current = stripTime(date);

        for (const booking of bookings) {
            const checkIn = stripTime(new Date(booking.check_in_date));
            const checkOut = stripTime(new Date(booking.check_out_date));

            if (current >= checkIn && current < checkOut) {
                return ('bg-danger text-white');
            }
        }
    };

    return (
        <div className="mt-4">
            <h5>Kalendarz rezerwacji</h5>
            <Calendar
                onChange={setSelectedDate}
                value={selectedDate}
                tileClassName={tileClassName}
            />
        </div>
    );
}

export default BookingCalendar;

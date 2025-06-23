import { useState } from "react";

function BookingForm({ houseId, onBookingCreated }) {
  const [checkIn, setCheckIn] = useState(localStorage.getItem("booking_checkIn") || "");
  const [checkOut, setCheckOut] = useState(localStorage.getItem("booking_checkOut") || "");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Dokonaj rezerwacji token:", localStorage.getItem("token"))
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Musisz być zalogowany, aby dokonać rezerwacji.");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/api/booking/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${token}`
        },
        body: JSON.stringify({
          house_id: houseId,
          check_in_date: checkIn,
          check_out_date: checkOut,
        }),
      });
      if (res.ok) {
        setSuccess("Rezerwacja została utworzona!");
        setError("");
        // Opcjonalnie: czyścimy pola po udanej rezerwacji
        // setCheckIn("");
        // setCheckOut("");
        onBookingCreated && onBookingCreated();
      } else {
        const data = await res.json();
        // Możesz tu rozbić komunikaty błędów, na przykład:
        if (data.non_field_errors) {
          setError(data.non_field_errors.join(" "));
        } else if (data.check_in_date) {
          setError(data.check_in_date.join(" "));
        } else {
          setError(JSON.stringify(data));
        }
        setSuccess("");
      }
    } catch (err) {
      setError("Wystąpił błąd podczas tworzenia rezerwacji.");
      setSuccess("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 border p-3 rounded">
      <h5>Utwórz rezerwację</h5>
      <div className="mb-3">
        <label className="form-label">Data zameldowania</label>
        <input
          type="date"
          className="form-control"
          value={checkIn}
          onChange={(e) => setCheckIn(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Data wymeldowania</label>
        <input
          type="date"
          className="form-control"
          value={checkOut}
          onChange={(e) => setCheckOut(e.target.value)}
          required
        />
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <button type="submit" className="btn btn-primary">Dokonaj rezerwacji</button>
    </form>
  );
}

export default BookingForm;

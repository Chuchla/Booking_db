import React, { useState } from "react";

function CreatePropertyForm() {
  const [form, setForm] = useState({
    name: "",
    description: "",
    price: "",
    max_guests: "",
    country: "",
    region: "",
    city: "",
    street: "",
    house_number: "",
    apartment_number: ""
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Musisz być zalogowany, aby utworzyć obiekt.");
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/property/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${token}`
        },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        setSuccess("Obiekt został utworzony!");
        setError("");
        setForm({
          name: "",
          description: "",
          price: "",
          max_guests: "",
          country: "",
          region: "",
          city: "",
          street: "",
          house_number: "",
          apartment_number: ""
        });
      } else {
        const data = await res.json();
        setError(JSON.stringify(data));
        setSuccess("");
      }
    } catch (err) {
      setError("Wystąpił błąd podczas tworzenia obiektu.");
      setSuccess("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4">
      <h2>Utwórz obiekt</h2>
      <div className="mb-3">
        <label className="form-label">Nazwa obiektu</label>
        <input
          type="text"
          name="name"
          className="form-control"
          value={form.name}
          onChange={handleChange}
          required
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Opis obiektu</label>
        <textarea
          name="description"
          className="form-control"
          rows="3"
          value={form.description}
          onChange={handleChange}
          required
        ></textarea>
      </div>

      <div className="row g-3 mb-3">
        <div className="col-md-6">
          <label className="form-label">Cena za noc</label>
          <input
            type="number"
            name="price"
            className="form-control"
            value={form.price}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-md-6">
          <label className="form-label">Maksymalna liczba gości</label>
          <input
            type="number"
            name="max_guests"
            className="form-control"
            value={form.max_guests}
            onChange={handleChange}
            required
          />
        </div>
      </div>

      <div className="row g-3 mb-3">
        <div className="col">
          <label className="form-label">Kraj</label>
          <input
            type="text"
            name="country"
            className="form-control"
            value={form.country}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col">
          <label className="form-label">Region</label>
          <input
            type="text"
            name="region"
            className="form-control"
            value={form.region}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col">
          <label className="form-label">Miasto</label>
          <input
            type="text"
            name="city"
            className="form-control"
            value={form.city}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col">
          <label className="form-label">Ulica</label>
          <input
            type="text"
            name="street"
            className="form-control"
            value={form.street}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col">
          <div className="row">
            <div className="col">
              <label className="form-label">Nr. domu</label>
              <input
                type="text"
                name="house_number"
                className="form-control"
                value={form.house_number}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col">
              <label className="form-label">Nr. mieszkania</label>
              <input
                type="text"
                name="apartment_number"
                className="form-control"
                value={form.apartment_number}
                onChange={handleChange}
              />
            </div>
          </div>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="text-end">
        <button type="submit" className="btn btn-primary">Stwórz obiekt</button>
      </div>
    </form>
  );
}

export default CreatePropertyForm;

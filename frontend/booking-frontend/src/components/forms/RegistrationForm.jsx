import { useState } from "react";

function RegistrationForm({ onRegister }) {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    password: "",
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
    try {
      const res = await fetch("http://localhost:8000/api/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.status === 201) {
        setError("")
        setSuccess("Rejestracja zakończona sukcesem! Możesz się teraz zalogować.")
        setForm({first_name: "", last_name: "", email: "", phone: "", password: ""})
        onRegister();
      } else {
        const data = await res.json();
        if(data.email){
          setError(data.email.join(" "))
        } else {
          const allErrors = Object.entries(data)
              .map(([field, messages]) => '${field} : ${messages.join(" ")}')
              .join(" | ");
          setError(allErrors);
        }
        setSuccess("")
      }
    } catch (err) {
      setError("Wystąpił błąd podczas rejestracji");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4">
      <div className="row g-3">
        <div className="col-md-6">
          <label className="form-label">Imię</label>
          <input
            type="text"
            name="first_name"
            className="form-control"
            value={form.first_name}
            onChange={handleChange}
            required />
        </div>
        <div className="col-md-6">
          <label className="form-label">Nazwisko</label>
          <input
            type="text"
            name="last_name"
            className="form-control"
            value={form.last_name}
            onChange={handleChange}
            required />
        </div>
      </div>
      <div className="mb-3 mt-3">
        <label className="form-label">Email</label>
        <input
          type="email"
          name="email"
          className="form-control"
          value={form.email}
          onChange={handleChange}
          required />
      </div>
      <div className="mb-3">
        <label className="form-label">Telefon</label>
        <input
          type="text"
          name="phone"
          className="form-control"
          value={form.phone}
          onChange={handleChange}
          required />
      </div>
      <div className="mb-3">
        <label className="form-label">Hasło</label>
        <input
          type="password"
          name="password"
          className="form-control"
          value={form.password}
          onChange={handleChange}
          required />
      </div>
      {success && <div className="alert alert-success">{success}</div>}
      {error && <div className="alert alert-danger">{error}</div>}
      <button type="submit" className="btn btn-primary">Zarejestruj się</button>
    </form>
  );
}

export default RegistrationForm;

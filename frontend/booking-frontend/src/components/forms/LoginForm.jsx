import { useState } from "react";

function LoginForm({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      console.log("Login response:", data);
      if (data.token) {
        localStorage.setItem('token', data.token)
        console.log("Token zapisany:", localStorage.getItem('token'))
        //localStorage.setItem("token", data.token);
        onLogin(data.token);
      } else {
        setError("Niepoprawne dane logowania");
      }
    } catch (err) {
      setError("Wystąpił błąd podczas logowania");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4">
      <div className="mb-3">
        <label className="form-label">Email</label>
        <input
          type="email"
          className="form-control"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required />
      </div>
      <div className="mb-3">
        <label className="form-label">Hasło</label>
        <input
          type="password"
          className="form-control"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required />
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
      <button type="submit" className="btn btn-primary">Zaloguj</button>
    </form>
  );
}

export default LoginForm;
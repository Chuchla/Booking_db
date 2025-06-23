// Plik: src/components/Login.js
import axios from "axios";

const loginUser = async (loginData) => {
  try {
    const response = await axios.post("http://localhost:8000/api/login/", loginData);
    // Załóżmy, że odpowiedź ma strukturę: { token: "your_jwt_token_here" }
    const token = response.data.token;
    // Zapisz token np. w localStorage
    localStorage.setItem("access_token", token);
    console.log("Zalogowano, token:", token);
  } catch (error) {
    console.error("Błąd logowania:", error.response?.data);
  }
};

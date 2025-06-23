// Plik: src/components/CreateProperty.js (lub inny odpowiedni plik)
import axios from "axios";

const createProperty = async (propertyData) => {
  // Pobieramy token z localStorage
  const token = localStorage.getItem("access_token");
  try {
    const response = await axios.post(
      "http://localhost:8000/api/property/create/",
      propertyData,
      {
        headers: {
          // Jeśli używasz JWT, nagłówek powinien mieć format Bearer
          'Authorization': `Token ${token}`
        }
      }
    );
    console.log("Obiekt utworzony:", response.data);
  } catch (error) {
    console.error("Błąd przy tworzeniu obiektu:", error.response?.data);
  }
};



import React, {useState} from "react";
import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";
import PropertiesList from "./components/PropertiesList.jsx";
import PropertiesSearchForm from "./components/forms/PropertiesSearchForm.jsx";
import LoginForm from "./components/forms/LoginForm.jsx";
import RegistrationForm from "./components/forms/RegistrationForm.jsx";
import PropertyDetails from "./components/PropertyDetails.jsx";
import CreatePropertyForm from "./components/forms/CreatePropertyForm.jsx";

const App = () => {
    const [properties, setProperties] = useState([])
    const [token, setToken] = useState(localStorage.getItem("token") || null);
    const [isLoggedIn, setIsLoggedIn] = useState(!!token);
    const [errorMessage, setErrorMessage] = useState("")

    const handleLogin = (newToken) => {
        console.log("New token:", newToken)
        localStorage.setItem("token", newToken);
        setToken(newToken);
        setIsLoggedIn(true);
        setErrorMessage("");
    }

    const handleLogout = () => {
        localStorage.removeItem("token");
        setToken(null);
        setIsLoggedIn(false);
    }


    return (
        <Router>
            <div className="container mt-4">
                <Routes>
                    <Route
                        path="/"
                        element={
                            isLoggedIn ? (
                                <>
                                    <div className="d-flex justify-content-between align-items-center mb-4">
                                        <h1>Witaj w portalu Booking</h1>
                                        <div>
                                            <Link className="btn btn-success" to={'/property/create'}>
                                                Dodaj obiekt (( :
                                            </Link>
                                            <button className="btn btn-danger" onClick={handleLogout}>
                                                Wyloguj
                                            </button>
                                        </div>

                                    </div>
                                    <PropertiesSearchForm onSearch={setProperties}/>
                                    <PropertiesList list={properties}/>
                                </>
                            ) : (
                                <>

                                    <h1>Logowanie</h1>
                                    <LoginForm onLogin={handleLogin} setErrorMessage={setErrorMessage}/>
                                    {errorMessage && (
                                        <div className="alert alert-danger mt-3">{errorMessage}</div>
                                    )}
                                    <h2 className="mt-4">Rejestracja</h2>
                                    <RegistrationForm onRegister={() => alert("Zarejestrowano!")}/>
                                </>
                            )
                        }
                    />
                    <Route path="/property/:houseId" element={<PropertyDetails/>}/>
                    <Route path="/property/create" element={<CreatePropertyForm/>}/>
                </Routes>
            </div>
        </Router>
    );

};

export default App;



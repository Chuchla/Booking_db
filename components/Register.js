import {useState} from "react"
import axios from "axios"

const Register = () =>
{
    const [formData, setFormData] = useState(
        {
            first_name: "",
            last_name:  "",
            email:      "",
            password:   "",
            phone:      ""
        }
    );

    const handleChange = (e) =>
    {
        setFormData({...formData, [e.target.name]: e.target.value})
    }

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        try{
            const response = await axios.post("http://localhost:8000/api/register", formData)
            console.log("Rejestracja udana", response.data);
        } catch (error) {
            console.error("Błąd rejestracji:", error.response?.data)
        }
    };

    return(
     <form onSubmit={handleSubmit}>
         <input type={"text"} name={"first_name"} placeholder={"Imie"} onChange={handleChange} />
         <input type={"text"} name={"last_name"} placeholder={"Nazwisko"} onChange={handleChange} />
         <input type={"email"} name={"email"} placeholder={"Email"} onChange={handleChange} />
         <input type={"password"} name={"password"} placeholder={"Haslo"} onChange={handleChange} />
         <button type={"submit"}>Zarejestruj</>
     </form>
    )
}
export default Register;

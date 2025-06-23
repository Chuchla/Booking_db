import {useState} from 'react'

function PropertiesSearchForm({onSearch}) {
    const [form, setForm] = useState({
        region: "",
        city: "",
        minP: "",
        maxP: "",
        minG: "",
        maxG: "",
        country: "",
        description: "",
        checkIn: "",
        checkOut: ""
    });

    const handleChange = (event) => {
        const {name, value} = event.target;
        setForm({...form, [name]: value});
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        const params = new URLSearchParams();

        for (const key in form) {
            if (form[key]) {
                params.append(key, form[key])
            }
        }

        if (form.checkIn && form.checkOut) {
            localStorage.setItem("booking_checkIn", form.checkIn)
            localStorage.setItem("booking_checkOut", form.checkOut)
        } else {
            localStorage.removeItem("booking_checkIn")
            localStorage.removeItem("booking_checkOut")
        }

        try {
            const res = await fetch(`http://localhost:8000/api/property/search/?${params.toString()}`)
            const data = await res.json()
            onSearch(data);
        } catch (error) {
            console.error("Search error:", error)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="mb-4">
            <div className="row g-3">
                <div className="col">
                    <input
                        type="text"
                        name="region"
                        placeholder="Region"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="text"
                        name="city"
                        placeholder="City"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="number"
                        name="minP"
                        placeholder="Min Price"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="number"
                        name="maxP"
                        placeholder="Max Price"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="number"
                        name="minG"
                        placeholder="Min Guests"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="number"
                        name="maxG"
                        placeholder="Max Guests"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="text"
                        name="country"
                        placeholder="Country"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="text"
                        name="description"
                        placeholder="Description"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="date"
                        name="checkIn"
                        placeholder="Check-in"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col">
                    <input
                        type="date"
                        name="checkOut"
                        placeholder="Check-out"
                        className="form-control"
                        onChange={handleChange}
                    />
                </div>
                <div className="col-12 text-end">
                    <button type="submit" className="btn btn-primary">
                        Szukaj z tymi parametrami
                    </button>
                </div>
            </div>
        </form>
    );
}

export default PropertiesSearchForm
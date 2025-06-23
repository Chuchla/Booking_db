import React, {useState} from 'react'

export const ReviewForm = ({houseId}) => {
    const [form, setForm] = useState({
        rating: "",
        description: "",
    })
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const handleChange = (e) => {
        const {name, value } = e.target;
        setForm((prev)=> ({
            ...prev,
            [name] : value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");
        if(!token){
            setError("Musisz byc zalogowany zeby ocenic obiekt");
            return;
        }
        const payload = {
            ...form,
            house_id: houseId
        };
        try{
            const res = await fetch("http://127.0.0.1:8000/api/review/create/", {
                method: "POST",
                headers : {
                    "Content-Type": "application/json",
                    "Authorization": `Token ${token}`
                },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                setSuccess("Pomyślnie utworzono opinie!");
                setError("");
                setForm({rating: "", description : ""});
            } else {
                const data = await res.json();
                setError(JSON.stringify(data));
                setSuccess("")
            }
        } catch (err){
            setError("Wystąpił błąd podczas tworzenia opinii")
            setSuccess("")
        }
    }
    return (
        <form onSubmit={handleSubmit} className={'mt-4'}>
            <h5>Byłes u nas w obiekcie? Zostaw opinie!</h5>
            <div>
                <label className={'form-label'}>Ilość gwiazdek</label>
              <input
                  key={'rating'}
                  id={'rating'}
                  type={'number'}
                  name={'rating'}
                  title={'Rating'}
                  placeholder={'rating'}
                  value={form.rating}
                  onChange={handleChange}
                  required
              />
            </div>

            <div>
                <label className={'form-label'}>Opis opinii</label>
                <textarea
                  name="description"
                  className="form-control"
                  rows="3"
                  value={form.description}
                  onChange={handleChange}
                  required
                />
            </div>
            {error && <div className={'alert alert-danger'}>{error}</div>}
            {success && <div className={'alert alert-success'}>{success}</div> }

            <div className={'text-end'}>
                <button type={'submit'} className={'btn btn-primary'}>Dodaj opinie</button>
            </div>
        </form>
    )
}

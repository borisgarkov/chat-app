import * as React from "react";
import { navigate } from 'gatsby';
import { BACKEND_URL, LOGIN_ENDPOINT, ACCESS_TOKEN, CHAT_URL, USER_ID } from "../components/constants";

export default function Home() {
    const [credentials, setCredentials] = React.useState({
        username: '',
        password: '',
    })

    const updateCredentials = (e) => {
        setCredentials({
            ...credentials,
            [e.currentTarget.id]: e.target.value
        })
    };

    const handleSubmit = async (e) => {
        e.preventDefault()

        let formData = [];
        for (let property in credentials) {
            let encodedKey = encodeURIComponent(property);
            let encodedValue = encodeURIComponent(credentials[property]);
            formData.push(encodedKey + "=" + encodedValue);
        }
        formData = formData.join("&");

        const response = await fetch(BACKEND_URL + LOGIN_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        })

        if (response.ok === false) {
            alert('invalid credentials')
            return
        };

        const access_token = await response.json();

        localStorage.setItem(ACCESS_TOKEN, access_token['access_token'])
        localStorage.setItem(USER_ID, access_token['user_id'])
        navigate(CHAT_URL)
    }

    return (
        <>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input id="username" type="text" value={credentials.username} onChange={updateCredentials} />

                <label htmlFor="password">Password</label>
                <input id="password" type="password" value={credentials.password} onChange={updateCredentials} />

                <input type="submit" value="Submit" />
            </form>
        </>
    )
}
import * as React from 'react';
import { ACCESS_TOKEN, BACKEND_URL, CHAT_URL, REGISTER_ENDPOINT, USER_ID } from './constants';
import { navigate } from 'gatsby';

export default function Register() {
    const [credentials, setCredentials] = React.useState({
        username: '',
        password: '',
    })

    const updateCredentials = (e) => {
        setCredentials({
            ...credentials,
            [e.currentTarget.id.replace('_register', '')]: e.target.value
        })
    };

    const handleSubmit = async (e) => {
        e.preventDefault()

        const response = await fetch(BACKEND_URL + REGISTER_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentials),
        })

        if (response.ok === false) {
            alert('invalid registration, try again')
            return
        };

        const access_token = await response.json();

        localStorage.setItem(ACCESS_TOKEN, access_token['access_token'])
        localStorage.setItem(USER_ID, access_token['user_id'])
        navigate(CHAT_URL)
    }

    return (
        <>
            <h1>Register</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username_register">Username</label>
                <input id="username_register" type="text" value={credentials.username} onChange={updateCredentials} />

                <label htmlFor="password_register">Password</label>
                <input id="password_register" type="password" value={credentials.password} onChange={updateCredentials} />

                <input type="submit" value="Submit" />
            </form>
        </>
    )
}
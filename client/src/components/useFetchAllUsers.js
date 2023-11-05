import * as React from "react";
import { BACKEND_URL, GET_ALL_USERS_ENDPOINT, UNAUTHENTICATED_URL } from './constants';
import { navigate } from "gatsby";


export default function useFetchAllUsers() {
    const [users, setUsers] = React.useState([]);

    const fetchAllUsers = async () => {
        const response = await fetch(BACKEND_URL + GET_ALL_USERS_ENDPOINT, { credentials: 'include' });
        console.log(response)
        if (response.status === 401) {
            navigate(UNAUTHENTICATED_URL)
        }

        if (response.ok === false) {
            alert('Error while fetching users')
            return
        }

        const results = await response.json();

        setUsers(results);
    }

    React.useEffect(() => { fetchAllUsers() }, []);

    return users
}
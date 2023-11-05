import * as React from 'react';
import { BACKEND_URL, GET_CHAT_HISTORY_ENDPOINT, ACCESS_TOKEN } from './constants';

export default function useFetchChatHistory(recipient_id) {
    const [history, setHistory] = React.useState([]);

    const fetchHistory = async () => {
        const response = await fetch(
            BACKEND_URL
            + GET_CHAT_HISTORY_ENDPOINT
            + "?"
            + "recipient_id=" + recipient_id
            + "&"
            + "token=" + localStorage.getItem(ACCESS_TOKEN)
        );

        if (response.ok === false) {
            alert('Error while chat history')
            return
        }

        const results = await response.json();

        setHistory(results);
    }

    React.useEffect(() => { fetchHistory() }, [])

    return history
}
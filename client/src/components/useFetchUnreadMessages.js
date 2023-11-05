import * as React from 'react';
import { BACKEND_URL, GET_UNREAD_MESSAGES_ENDPOINT } from './constants';

export default function useFetchUnreadMessages(recipient_id) {
    const [unreadMessages, setUnreadMessages] = React.useState([]);

    const fetchHistory = async () => {
        const response = await fetch(BACKEND_URL + GET_UNREAD_MESSAGES_ENDPOINT + `?recipient_id=${recipient_id}`);

        if (response.ok === false) {
            alert('Error while unread chats')
            return
        }

        const results = await response.json();

        setUnreadMessages(results['number_of_unread_messages']);
    }

    React.useEffect(() => { fetchHistory() }, [])

    return unreadMessages
}
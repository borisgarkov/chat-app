import * as React from "react";
import { Link, navigate } from "gatsby";

import { AUTHENTICATED, CHAT_URL, HOME_URL, USER_ID } from "../../components/constants";
import useFetchAllUsers from "../../components/useFetchAllUsers";
import useFetchUnreadMessages from "../../components/useFetchUnreadMessages";

export default function Chat() {
    const users = useFetchAllUsers();
    // const unreadMessages = useFetchUnreadMessages(localStorage.getItem(USER_ID));

    if ([false, null].includes(localStorage.getItem(AUTHENTICATED))) { navigate(HOME_URL) };

    if (!users) { return <h2>Loading active users</h2> };

    return (
        <>
            <h1>Chat</h1>

            {/* <h2 style={{ color: 'red' }}>Unread Messages: {unreadMessages}</h2> */}

            <h2>List of active users</h2>
            {
                users.map(user => {
                    return (
                        <Link key={user.id} to={CHAT_URL + `/${user.id}`} >
                            <p>{user.username}</p>
                        </Link>
                    )
                })
            }

            <h4
                style={{
                    textDecoration: 'underline',
                    cursor: 'pointer'
                }}
                onClick={() => {
                    localStorage.clear()
                    navigate(HOME_URL)
                }}
            >
                Logout
            </h4>
        </>
    )
}
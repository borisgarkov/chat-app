import * as React from "react";
import { Link } from "gatsby";
import { CHAT_URL, WEBSOCKET_URL, ACCESS_TOKEN, SENDER, RECIPIENT, USER_ID } from "../../components/constants";
import useFetchChatHistory from "../../components/useFetchChatHistory";

function Message({ user, message }) {
    return (
        <h5
            style={{
                textAlign: user === SENDER ? 'right' : 'left',
                border: '1px solid black',
                borderRadius: '10px',
                padding: '5px',
                alignSelf: user === SENDER ? 'flex-end' : 'flex-start',
            }}
        >
            {message}
        </h5>
    )
}

export default function PrivateChat(props) {
    const [message, setMessage] = React.useState('');
    const updateMessage = (e) => {
        setMessage(e.target.value)
    }

    const [chat, setChat] = React.useState([]);
    const updateChat = (newMessage) => {
        setChat((prev) => [...prev, newMessage])
    }

    const chatHistory = useFetchChatHistory(props.id);

    const [ws, setWs] = React.useState();

    React.useEffect(() => {
        const websocket = new WebSocket(WEBSOCKET_URL + props.id);
        setWs(websocket)

        websocket.onopen = () => { websocket.send(localStorage.getItem(ACCESS_TOKEN)) }
        websocket.onmessage = (e) => { updateChat(<Message user={RECIPIENT} message={e.data} />) }
        websocket.onclose = () => { console.log('closing websocket') }

        return () => { websocket.close() }
    }, [chat])

    const sendMessage = (e) => {
        e.preventDefault()
        const messageSent = message.trim()
        if (messageSent === '') { return }

        if (ws.readyState !== WebSocket.OPEN) {
            console.log('connection is not opened')
            return
        }

        ws.send(messageSent)
        updateChat(<Message user={SENDER} message={messageSent} />)
        setMessage('')
    };

    return (
        <>
            <h1>Private Chat with {props.id}</h1>
            <Link to={CHAT_URL} >Go back to main chat room</Link>

            <div style={{
                display: 'flex',
                flexDirection: 'column',
                maxWidth: '500px',
                maxHeight: '400px',
                overflowY: 'scroll',
            }}>
                {
                    chatHistory.map(record => {
                        return (
                            <React.Fragment key={record.id}>
                                <Message
                                    user={record.sender_id === parseInt(localStorage.getItem(USER_ID)) ? SENDER : RECIPIENT}
                                    message={record.message}
                                />
                            </React.Fragment>
                        )
                    })
                }
                {
                    chat.map((message, indx) => <React.Fragment key={indx + message}>{message}</React.Fragment>)
                }

            </div>

            <form style={{ marginTop: '100px' }} onSubmit={sendMessage}>
                <label htmlFor="message">Message</label>
                <input id='message' value={message} onChange={updateMessage} />
                <input type="submit" value="Submit" />
            </form>
        </>
    )
}
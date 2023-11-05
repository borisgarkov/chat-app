// BACKEND URLS
const BACKEND_URL = 'http://localhost:9000/';
const LOGIN_ENDPOINT = 'login/';
const REGISTER_ENDPOINT = 'register/';
const GET_ALL_USERS_ENDPOINT = 'users/';
const GET_CHAT_HISTORY_ENDPOINT = 'chat-history/';
const GET_UNREAD_MESSAGES_ENDPOINT = 'unread-messages/';

const WEBSOCKET_URL = 'ws://localhost:9000/ws/';

// FRONTEND URLS
const CHAT_URL = '/chat';
const HOME_URL = '/';
const UNAUTHENTICATED_URL = '/error';

// TOKENS
const AUTHENTICATED = 'AUTHENTICATED';
const USER_ID = 'user_id';

// CHAT MESSAGES
const SENDER = 'sender';
const RECIPIENT = 'recipient';

export {
    // BACKEND URLS
    BACKEND_URL,
    REGISTER_ENDPOINT,
    LOGIN_ENDPOINT,
    GET_ALL_USERS_ENDPOINT,
    WEBSOCKET_URL,
    GET_CHAT_HISTORY_ENDPOINT,
    GET_UNREAD_MESSAGES_ENDPOINT,
    // FRONTEND URLS
    CHAT_URL,
    HOME_URL,
    UNAUTHENTICATED_URL,
    // LOCAL STORAGE
    AUTHENTICATED,
    USER_ID,
    // CHAT MESSAGES
    SENDER,
    RECIPIENT
}
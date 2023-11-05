import * as React from 'react';
import { navigate } from 'gatsby';
import { HOME_URL } from '../components/constants';

export default function NotAuthenticated() {
    return (
        <>
            <h1>
                Your session has expired
            </h1>
            <h4
                onClick={() => navigate(HOME_URL)}
                style={{ textDecoration: 'underline', color: 'blue', cursor: 'pointer' }}
            >
                Log in again
            </h4>
        </>
    )
}
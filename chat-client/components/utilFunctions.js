const serverHost = 'http://127.0.0.1:5001';

async function makeRequest(endPoint, httpMethod, httpHeaders, requestBody) {
    try {
        const response = await fetch(serverHost + endPoint, {
            method: httpMethod,
            headers: httpHeaders,
            body: JSON.stringify(requestBody)
        });

        if (response.ok != true) {
            const error = await response.json();
            throw new Error(error.message);
        }

        const result = await response.json();

        return result

    } catch (error) {
        console.log(error.message);
    }
};

export { makeRequest };
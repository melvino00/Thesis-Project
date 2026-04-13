import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 20 }, // Warm-up period
        { duration: '2m', target: 20 },  // Plateau phase
        { duration: '30s', target: 0 },  // Ramp-down
    ],
};

export function setup() {
    const res = http.post('http://localhost:8000/auth', JSON.stringify({}));
    return { token: res.body };
}

    export default function (data) {
    const url = 'http://localhost:8000/users';
    const params = {
        headers: {
            'Authorization': data.token,
        },
    };
    
    http.get(url, params);
    sleep(0.1);
}
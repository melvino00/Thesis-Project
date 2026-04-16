import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
    stages: [
        //change target 10/50 for switching load testing
        { duration: '30s', target: 50 }, // Warm-up period
        { duration: '2m', target: 50 },  // Plateau phase
        { duration: '30s', target: 0 },  // Ramp-down
    ],
};

export function setup() {
    const res = http.post('http://localhost:8000/auth');
    const body = JSON.parse(res.body);
    return { token: body.token };
}

    export default function (data) {

    // Change between /single/chained for different scenarios
    // Change between /small/medium/large for different payloads
    const url = 'http://localhost:8000/chained/large'; 
    const params = {
        headers: {
            'Authorization': `Bearer ${data.token}`,
        },
    };
    
    http.get(url, params);
    sleep(1);
}
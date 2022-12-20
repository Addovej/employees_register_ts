import axios from "axios";

export default axios.create({
    baseURL: "http://localhost:8070/api",
    headers: {
        "Content-type": "application/json"
    }
});
import http from "../http-common";

class EmployeeDataService {
    getAll() {
        return http.get("/v1/employees/");
    }

    get(id) {
        return http.get(`/v1/employees/${id}/`);
    }

    create(data) {
        return http.post("/v1/employees/", data);
    }

    update(id, data) {
        return http.put(`/v1/employees/${id}/`, data);
    }

    delete(id) {
        return http.delete(`/v1/employees/${id}/`);
    }
}

export default new EmployeeDataService();
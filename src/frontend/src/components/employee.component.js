import React, {Component} from "react";
import EmployeeDataService from "../services/employee.service";
import {withRouter} from '../common/with-router';
import {getCurrentDate} from "../common/utils";

class Employee extends Component {
    constructor(props) {
        super(props);
        this.onChangeChiefId = this.onChangeChiefId.bind(this);
        this.onChangeFirstName = this.onChangeFirstName.bind(this);
        this.onChangeLastName = this.onChangeLastName.bind(this);
        this.onChangeMiddleName = this.onChangeMiddleName.bind(this);
        this.onChangePosition = this.onChangePosition.bind(this);
        this.onChangeSalary = this.onChangeSalary.bind(this);
        this.onChangeHireDate = this.onChangeHireDate.bind(this);

        this.getEmployee = this.getEmployee.bind(this);
        this.updatePublished = this.updatePublished.bind(this);
        this.updateEmployee = this.updateEmployee.bind(this);
        this.deleteEmployee = this.deleteEmployee.bind(this);

        this.state = {
            currentEmployee: {
                id: null,
                chief_id: null,
                first_name: "",
                last_name: "",
                middle_name: "",
                position: "",
                salary: null,
                hire_date: getCurrentDate(),
            },
            message: ""
        };
    }

    componentDidMount() {
        this.getEmployee(this.props.router.params.id);
    }

    onChangeChiefId(e) {
        const chief_id = e.target.value;

        this.setState(function (prevState) {
            return {
                currentEmployee: {
                    ...prevState.currentEmployee,
                    chief_id: chief_id
                }
            };
        });
    }

    onChangeFirstName(e) {
        const first_name = e.target.value;

        this.setState(function (prevState) {
            return {
                currentEmployee: {
                    ...prevState.currentEmployee,
                    first_name: first_name
                }
            };
        });
    }

    onChangeLastName(e) {
        const last_name = e.target.value;

        this.setState(function (prevState) {
            return {
                currentEmployee: {
                    ...prevState.currentEmployee,
                    last_name: last_name
                }
            };
        });
    }

    onChangeMiddleName(e) {
        const middle_name = e.target.value;

        this.setState(function (prevState) {
            return {
                currentEmployee: {
                    ...prevState.currentEmployee,
                    middle_name: middle_name
                }
            };
        });
    }

    onChangePosition(e) {
        const position = e.target.value;

        this.setState(function (prevState) {
            return {
                currentEmployee: {
                    ...prevState.currentEmployee,
                    position: position
                }
            };
        });
    }

    onChangeSalary(e) {
        const salary = e.target.value;

        this.setState(function (prevState) {
            return {
                currentEmployee: {
                    ...prevState.currentEmployee,
                    salary: salary
                }
            };
        });
    }

    onChangeHireDate(e) {
        const hire_date = e.target.value;

        this.setState(function (prevState) {
            return {
                currentEmployee: {
                    ...prevState.currentEmployee,
                    hire_date: hire_date
                }
            };
        });
    }

    getEmployee(id) {
        EmployeeDataService.get(id).then(response => {
            this.setState({
                currentEmployee: response.data
            });
            console.log(response.data);
        }).catch(e => {
            console.log(e);
        });
    }

    updatePublished(status) {
        var data = {
            id: this.state.currentEmployee.id,
            chief_id: this.state.currentEmployee.chief_id,
            first_name: this.state.currentEmployee.first_name,
            last_name: this.state.currentEmployee.last_name,
            middle_name: this.state.currentEmployee.middle_name,
            position: this.state.currentEmployee.position,
            salary: this.state.currentEmployee.salary,
            hire_date: this.state.currentEmployee.hire_date,
        };

        EmployeeDataService.update(
            this.state.currentEmployee.id, data
        ).then(response => {
            this.setState(prevState => ({
                currentEmployee: {
                    ...prevState.currentEmployee,
                    published: status
                }
            }));
            console.log(response.data);
        }).catch(e => {
            console.log(e);
        });
    }

    updateEmployee() {
        EmployeeDataService.update(
            this.state.currentEmployee.id,
            this.state.currentEmployee
        ).then(response => {
            console.log(response.data);
            this.setState({
                message: "The employee was updated successfully!"
            });
        }).catch(e => {
            console.log(e);
        });
    }

    deleteEmployee() {
        EmployeeDataService.delete(this.state.currentEmployee.id).then(response => {
            console.log(response.data);
            this.props.router.navigate('/');
        }).catch(e => {
            console.log(e);
        });
    }

    render() {
        const {currentEmployee} = this.state;

        return (
            <div>
                {currentEmployee ? (
                    <div className="edit-form">
                        <h4>Employee</h4>
                        <form>
                            <div className="form-group">
                                <label htmlFor="first_name">First Name</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="first_name"
                                    value={currentEmployee.first_name}
                                    onChange={this.onChangeFirstName}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="last_name">Last Name</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="last_name"
                                    value={currentEmployee.last_name}
                                    onChange={this.onChangeLastName}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="middle_name">Middle Name</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="middle_name"
                                    value={currentEmployee.middle_name}
                                    onChange={this.onChangeMiddleName}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="position">Position</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="position"
                                    value={currentEmployee.position}
                                    onChange={this.onChangePosition}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="salary">Salary</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="salary"
                                    value={currentEmployee.salary}
                                    onChange={this.onChangeSalary}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="hire_date">Hire Date</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="hire_date"
                                    value={currentEmployee.hire_date}
                                    onChange={this.onChangeHireDate}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="chief_id">Chief ID</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="chief_id"
                                    value={currentEmployee.chief_id}
                                    onChange={this.onChangeChiefId}
                                />
                            </div>

                            <div className="form-group">
                                <label>
                                    <strong>Status:</strong>
                                </label>
                                {currentEmployee.published ? "Published" : "Pending"}
                            </div>
                        </form>

                        <button
                            className="badge badge-danger mr-2"
                            onClick={this.deleteEmployee}
                        >
                            Delete
                        </button>

                        <button
                            type="submit"
                            className="badge badge-success"
                            onClick={this.updateEmployee}
                        >
                            Update
                        </button>
                        <p>{this.state.message}</p>
                    </div>
                ) : (
                    <div>
                        <br/>
                        <p>Please click on a Employee...</p>
                    </div>
                )}
            </div>
        );
    }
}

export default withRouter(Employee);
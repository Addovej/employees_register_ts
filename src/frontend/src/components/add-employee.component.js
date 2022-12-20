import React, {Component} from "react";
import EmployeeDataService from "../services/employee.service";
import {getCurrentDate} from "../common/utils";

export default class AddEmployee extends Component {
    constructor(props) {
        super(props);
        this.onChangeChiefId = this.onChangeChiefId.bind(this);
        this.onChangeFirstName = this.onChangeFirstName.bind(this);
        this.onChangeLastName = this.onChangeLastName.bind(this);
        this.onChangeMiddleName = this.onChangeMiddleName.bind(this);
        this.onChangePosition = this.onChangePosition.bind(this);
        this.onChangeSalary = this.onChangeSalary.bind(this);
        this.onChangeHireDate = this.onChangeHireDate.bind(this);

        this.saveEmployee = this.saveEmployee.bind(this);
        this.newEmployee = this.newEmployee.bind(this);

        this.state = {
            id: null,
            chief_id: null,
            first_name: "",
            last_name: "",
            middle_name: "",
            position: "",
            salary: null,
            hire_date: getCurrentDate(),

            submitted: false
        };
    }

    onChangeChiefId(e) {
        this.setState({
            chief_id: e.target.value
        });
    }

    onChangeFirstName(e) {
        this.setState({
            first_name: e.target.value
        });
    }

    onChangeLastName(e) {
        this.setState({
            last_name: e.target.value
        });
    }

    onChangeMiddleName(e) {
        this.setState({
            middle_name: e.target.value
        });
    }

    onChangePosition(e) {
        this.setState({
            position: e.target.value
        });
    }

    onChangeSalary(e) {
        this.setState({
            salary: e.target.value
        });
    }

    onChangeHireDate(e) {
        this.setState({
            hire_date: e.target.value
        });
    }

    saveEmployee() {
        var data = {
            chief_id: this.state.chief_id,
            first_name: this.state.first_name,
            last_name: this.state.last_name,
            middle_name: this.state.middle_name,
            position: this.state.position,
            salary: this.state.salary,
            hire_date: this.state.hire_date,
        };

        EmployeeDataService.create(data).then(response => {
            this.setState({
                id: response.data.id,
                chief_id: response.data.chief_id,
                first_name: response.data.first_name,
                last_name: response.data.last_name,
                middle_name: response.data.middle_name,
                position: response.data.position,
                salary: response.data.salary,
                hire_date: response.data.hire_date,

                submitted: true
            });
            console.log(response.data);
        }).catch(e => {
            console.log(e);
        });
    }

    newEmployee() {
        this.setState({
            id: null,
            chief_id: null,
            first_name: "",
            last_name: "",
            middle_name: "",
            position: "",
            salary: null,
            hire_date: getCurrentDate(),

            submitted: false
        });
    }

    render() {
        return (
            <div className="submit-form">
                {this.state.submitted ? (
                    <div>
                        <h4>You submitted successfully!</h4>
                        <button className="btn btn-success" onClick={this.newEmployee}>
                            Add
                        </button>
                    </div>
                ) : (
                    <div>
                        <div className="form-group">
                            <label htmlFor="first_name">First Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="first_name"
                                required
                                value={this.state.first_name}
                                onChange={this.onChangeFirstName}
                                name="first_name"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="last_name">Last Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="last_name"
                                required
                                value={this.state.last_name}
                                onChange={this.onChangeLastName}
                                name="last_name"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="middle_name">Middle Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="middle_name"
                                required
                                value={this.state.middle_name}
                                onChange={this.onChangeMiddleName}
                                name="middle_name"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="position">Position</label>
                            <input
                                type="text"
                                className="form-control"
                                id="position"
                                required
                                value={this.state.position}
                                onChange={this.onChangePosition}
                                name="position"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="salary">Salary</label>
                            <input
                                type="text"
                                className="form-control"
                                id="salary"
                                required
                                value={this.state.salary}
                                onChange={this.onChangeSalary}
                                name="salary"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="hire_date">Hire Date</label>
                            <input
                                type="text"
                                className="form-control"
                                id="hire_date"
                                required
                                value={this.state.hire_date}
                                onChange={this.onChangeHireDate}
                                name="hire_date"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="chief_id">Chief ID</label>
                            <input
                                type="text"
                                className="form-control"
                                id="chief_id"
                                required
                                value={this.state.chief_id}
                                onChange={this.onChangeChiefId}
                                name="chief_id"
                            />
                        </div>

                        <button onClick={this.saveEmployee} className="btn btn-success">
                            Save
                        </button>
                    </div>
                )}
            </div>
        );
    }
}